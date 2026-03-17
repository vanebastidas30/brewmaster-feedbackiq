import psycopg2
import json
import time
from datetime import datetime, timezone
from openai import OpenAI
from prompts import analysis_prompt

client = OpenAI()

def get_connection(): 
    return psycopg2.connect(
        host="localhost",
        database="brewmaster",
        user="katherin"
    )

def analyze_review(text, rating):

    prompt = analysis_prompt(text, rating)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "Eres un analista de reseñas de cafeterías."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message.content
        print("LLM raw response:", content) #Debug
        data = json.loads(content)

        return data

    except Exception as e:

        print("Error con OpenAI:", e)
        return {
            "sentiment": "neutral",
            "categories": ["otro"],
            "summary": text[:100],
            "urgency": 2
        }

def run_analysis():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT ur.id, ur.text, ur.rating
        FROM unified_reviews ur
        LEFT JOIN review_analysis ra
        ON ur.id = ra.unified_review_id
        WHERE ra.unified_review_id IS NULL
    """)
    reviews = cursor.fetchall()

    for review_id, text, rating in reviews:

        result = analyze_review(text, rating)
        cursor.execute("""
            INSERT INTO review_analysis
            (unified_review_id, sentiment, categories, summary, urgency, created_at)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (
            review_id,
            result["sentiment"],
            ",".join(result["categories"]),
            result["summary"],
            result["urgency"],
            datetime.now(timezone.utc)
        ))
        time.sleep(0.3)  # evitar rate limits

    conn.commit()
    cursor.close()
    conn.close()
    print("Análisis completado")

if __name__ == "__main__":
    run_analysis()
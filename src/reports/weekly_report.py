from openai import OpenAI
from src.analysis.prompts import summary_prompt
import json
import psycopg2

client = OpenAI()

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="brewmaster",
        user="katherin"
    )

'''Total de reseñas semanales'''
def get_total_reviews(cursor):

    query = """SELECT COUNT(*)
        FROM unified_reviews
        WHERE created_at >= (
            SELECT MAX(created_at) - INTERVAL '7 days'
            FROM unified_reviews
        )"""

    cursor.execute(query)
    result = cursor.fetchone()
    return result[0]

'''Distribución de sentimientos'''
def get_sentiment_distribution(cursor):

    query = """SELECT ra.sentiment, COUNT(*)
        FROM review_analysis ra
        JOIN unified_reviews ur
            ON ra.unified_review_id = ur.id
        WHERE ur.created_at >= (
            SELECT MAX(created_at) - INTERVAL '7 days'
            FROM unified_reviews
        )
        GROUP BY ra.sentiment """

    cursor.execute(query)
    results = cursor.fetchall()
    return results

def calculate_percent(sentiment_counts, total):

    percentages = {}

    for sentiment, count in sentiment_counts:
        percentages[sentiment] = round((count / total) * 100, 2)

    return percentages

'''Los 3 locales con mejor calificación'''
def get_top_locations(cursor):

    query = """SELECT location_id, ROUND(AVG(rating), 2) as avg_rating
        FROM unified_reviews
        WHERE created_at >= (
            SELECT MAX(created_at) - INTERVAL '7 days'
            FROM unified_reviews
        )
        GROUP BY location_id
        ORDER BY avg_rating DESC
        LIMIT 3"""

    cursor.execute(query)
    results = cursor.fetchall()
    return results

'''Locales con más reseñas negativas'''
def get_problem_locations(cursor):

    query = """SELECT ur.location_id, COUNT(*) as negative_count
        FROM review_analysis ra
        JOIN unified_reviews ur
            ON ra.unified_review_id = ur.id
        WHERE ra.sentiment = 'negative'
        AND ur.created_at >= (
            SELECT MAX(created_at) - INTERVAL '7 days'
            FROM unified_reviews
        )
        GROUP BY ur.location_id
        ORDER BY negative_count DESC
        LIMIT 3"""

    cursor.execute(query)
    results = cursor.fetchall()
    return results

'''Categorías más mencionadas'''
def get_top_categories(cursor):

    query = """SELECT TRIM(category) as category, COUNT(*) as count
        FROM (
            SELECT unnest(string_to_array(categories, ',')) as category
            FROM review_analysis ra
            JOIN unified_reviews ur
                ON ra.unified_review_id = ur.id
            WHERE ur.created_at >= (
                SELECT MAX(created_at) - INTERVAL '7 days'
                FROM unified_reviews
            )
        ) sub
        GROUP BY category
        ORDER BY count DESC
        LIMIT 5"""

    cursor.execute(query)
    results = cursor.fetchall()
    return results

'''Función para generar el reporte'''
def generate_summary(total, sentiment, top_locations, problem_locations, categories):

    prompt = summary_prompt(
        total,
        sentiment,
        top_locations,
        problem_locations,
        categories
    )
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.3,
            messages=[
                {"role": "system", "content": "Eres un analista senior de datos."},
                {"role": "user", "content": prompt}
            ]
        )
        summary = response.choices[0].message.content
        return summary

    except Exception as e:
        print("Error con LLM:", e)
        return "No se pudo generar el resumen."

def generate_html_report(total, sentiment, top_locations, problem_locations, categories, summary):

    html = f"""
    <html>
    <head>
        <title>Weekly Report</title>
        <style>
            body {{ font-family: Arial; margin: 40px; }}
            h1 {{ color: #333; }}
            h2 {{ color: #555; }}
        </style>
    </head>
    <body>
    <h1>Reporte Semanal - BrewMaster</h1>
    <h2>Total de reseñas</h2>
    <p>{total}</p>
    <h2>Distribución de sentimiento (%)</h2>
    <ul>{''.join([f"<li>{x}: {y}%</li>" for x,y in sentiment.items()])}</ul>
    <h2>Top 3 locales mejor valorados</h2>
    <ul>{''.join([f"<li>Local {local}: {rating}</li>" for local, rating in top_locations])}</ul>
    <h2>Top 3 locales con más problemas</h2>
    <ul>{''.join([f"<li>Local {local}: {count} negativas</li>" for local, count in problem_locations])}</ul>
    <h2>Categorías más mencionadas</h2>
    <ul>{''.join([f"<li>{categorie}: {count}</li>" for categorie, count in categories])}</ul>
    <h2>Resumen Ejecutivo</h2>
    <p>{summary}</p>
    </body>
    </html>
    """

    with open("docs/weekly_report.html", "w") as f:
        f.write(html)
    print("\nReporte generado en: docs/weekly_report.html")

def run_report():

    conn = get_connection()
    cursor = conn.cursor()

    total = get_total_reviews(cursor)
    print("Total de reseñas:", total)

    sentiment_counts = get_sentiment_distribution(cursor)
    sentiment_percent = calculate_percent(sentiment_counts, total)
    print("Distribución de sentimiento (%):")
    print(sentiment_percent)

    top_locations = get_top_locations(cursor)
    print("\nTop 3 locales mejor valorados:")
    for local, rating in top_locations:
        print(f"Local {local} : {rating}")

    problem_locations = get_problem_locations(cursor)
    print("\nTop 3 locales con más problemas:")
    for local, count in problem_locations:
        print(f"Local {local} : {count} reseñas negativas")
    
    categories = get_top_categories(cursor)
    print("\nCategorías más mencionadas:")
    for categorie, count in categories:
        print(f"{categorie} : {count}")

    summary = generate_summary(
        total,
        sentiment_percent,
        top_locations,
        problem_locations,
        categories)
    print("\nResumen Ejecutivo:")
    print(summary)

    generate_html_report(
    total,
    sentiment_percent,
    top_locations,
    problem_locations,
    categories,
    summary)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    run_report()

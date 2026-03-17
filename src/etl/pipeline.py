from extractors import get_all_reviews_from_api, get_surveys_from_db
from transformers import merge_data
import psycopg2

def load_unified_reviews(reviews):
    conn = psycopg2.connect(
        host="localhost",
        database="brewmaster",
        user="katherin"
    )

    cursor = conn.cursor()
    query = """
        INSERT INTO unified_reviews (
            source,
            source_review_id,
            location_id,
            rating,
            text,
            author,
            created_at,
            ingested_at
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (source, source_review_id) 
        DO NOTHING
    """

    for r in reviews:
        cursor.execute(
            query,
            (
                r["source"],
                r["source_review_id"],
                r["location_id"],
                r["rating"],
                r["text"],
                r["author"],
                r["created_at"],
                r["ingested_at"]
            )
        )

    conn.commit()
    cursor.close()
    conn.close()

def run_pipeline():

    print("Extrayendo datos...")
    api_data = get_all_reviews_from_api()
    survey_data = get_surveys_from_db()

    print("Transformando datos...")
    unified = merge_data(api_data, survey_data)

    print("Cargando datos...")
    load_unified_reviews(unified)

    print("Pipeline completado")

if __name__ == "__main__":
    run_pipeline()
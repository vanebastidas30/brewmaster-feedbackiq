import requests
import psycopg2
from datetime import datetime, timedelta

base_url = "http://127.0.0.1:8081/api/reviews"

def get_reviews_from_api(location_id, since=None):
    
    params = {"location_id": location_id}

    if since:
        params["since"] = since
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        raise Exception("Error al obtener datos de la API")
    return response.json()

def get_api_max_date():
    
    max_date = None

    for location_id in range(1, 16):
        reviews = get_reviews_from_api(location_id)
        for r in reviews:
            review_date = datetime.fromisoformat(
                r["created_at"].replace("Z", "+00:00")
            )
            if not max_date or review_date > max_date:
                max_date = review_date
    return max_date

def get_all_reviews_from_api():

    all_reviews = []
    max_date = get_api_max_date()
    since = (max_date - timedelta(days=7)).isoformat()

    for location_id in range(1, 16):
        reviews = get_reviews_from_api(location_id, since)
        print(f"Location {location_id}: {len(reviews)} reviews")
        all_reviews.extend(reviews)
    return all_reviews

def get_surveys_from_db():
    conn = psycopg2.connect(
        host="localhost",
        database="brewmaster",
        user="katherin"
    )

    cursor = conn.cursor()
    query = """
        SELECT
            id,
            location_id,
            rating,
            comments,
            created_at,
            customer_email
        FROM customer_surveys
        WHERE created_at >= (
            SELECT MAX(created_at) - INTERVAL '7 days'
            FROM customer_surveys
        )
    """

    cursor.execute(query)
    columns = [desc[0] for desc in cursor.description]

    rows = [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

    cursor.close()
    conn.close()

    return rows

'''Probar el extractor'''
if __name__ == "__main__":

    print("Probando extracción desde API...")
    api_reviews = get_all_reviews_from_api()
    print(f"Total reviews API: {len(api_reviews)}")

    print("\nPrimeras 3 reviews de la API:")
    print(api_reviews[:3])


    print("\nProbando extracción desde PostgreSQL...")
    surveys = get_surveys_from_db()
    print(f"Total surveys DB: {len(surveys)}")

    print("\nPrimeras 3 encuestas:")
    print(surveys[:3])
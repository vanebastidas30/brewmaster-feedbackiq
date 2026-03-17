from datetime import datetime, timezone

def transformer_api_reviews(api_reviews):

    transformed = []

    for review in api_reviews:
        item = {
            "source": "api",
            "source_review_id": review["review_id"],
            "location_id": review["location_id"],
            "rating": review["rating"],
            "text": review["text"],
            "author": review["author"],
            "created_at": datetime.fromisoformat(
                review["created_at"].replace("Z", "+00:00")
            ),
            "ingested_at": datetime.now(timezone.utc)
        }
        transformed.append(item)
    return transformed

def transformer_surveys(db_rows):

    transformed = []

    for row in db_rows:
        item = {
            "source": "survey",
            "source_review_id": str(row["id"]),
            "location_id": row["location_id"],
            "rating": row["rating"],
            "text": row["comments"],
            "author": None,
            "created_at": row["created_at"],
            "ingested_at": datetime.now(timezone.utc)
        }
        transformed.append(item)
    return transformed

def merge_data(api_reviews, survey_rows):

    api_data = transformer_api_reviews(api_reviews)
    survey_data = transformer_surveys(survey_rows)
    unified = api_data + survey_data
    return unified

''' Para probar el tranformer'''
if __name__ == "__main__":

    from etl.extractors import get_all_reviews_from_api, get_surveys_from_db

    api_data = get_all_reviews_from_api()
    db_data = get_surveys_from_db()

    unified = merge_data(api_data, db_data)

    print("Total registros:", len(unified))
    print(unified[:3])
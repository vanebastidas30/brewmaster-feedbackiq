from src.etl.transformers import transformer_api_reviews, transformer_surveys

def test_transform_api_reviews():
    sample = [
        {
            "review_id": "r1",
            "location_id": 1,
            "rating": 5,
            "text": "Buen café",
            "author": "Test",
            "created_at": "2026-03-01T10:00:00Z"
        }
    ]
    result = transformer_api_reviews(sample)

    assert len(result) == 1
    assert result[0]["source"] == "api"
    assert result[0]["rating"] == 5
    assert result[0]["location_id"] == 1

def test_transform_surveys():
    sample = [
        {
            "id": 1,
            "location_id": 2,
            "rating": 3,
            "comments": "Normal",
            "created_at": "2026-03-01T10:00:00",
            "customer_email": "test@test.com"
        }
    ]
    result = transformer_surveys(sample)

    assert len(result) == 1
    assert result[0]["source"] == "survey"
    assert result[0]["rating"] == 3
    assert result[0]["location_id"] == 2
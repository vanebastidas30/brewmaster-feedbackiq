import psycopg2
from datetime import datetime, timezone

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="brewmaster",
        user="katherin"
    )

'''Detectar alertas críticas'''
def detect_critical_alerts(cursor):

    cursor.execute("""
        SELECT ra.unified_review_id, ur.location_id
        FROM review_analysis ra
        JOIN unified_reviews ur
        ON ur.id = ra.unified_review_id
        WHERE ra.urgency = 5
    """)

    results = cursor.fetchall()
    
    alerts = []

    for review_id, location_id in results:

        alerts.append({
            "severity": "CRITICA",
            "location_id": location_id,
            "message": f"Review crítica detectada (review_id={review_id})",
            "rule_code": "CRITICAL_URGENCY"
        })
    return alerts

def save_alerts(cursor, alerts):

    for alert in alerts:

        cursor.execute("""
            INSERT INTO alerts (severity, location_id, message, rule_code, created_at)
            VALUES (%s,%s,%s,%s,%s)
        """, (
            alert["severity"],
            alert["location_id"],
            alert["message"],
            alert["rule_code"],
            datetime.now(timezone.utc)
        ))


'''Detectar alertas altas'''
def detect_high_alerts(cursor):

    cursor.execute("""
        SELECT
            ur.location_id,
            COUNT(*) AS negative_count
        FROM review_analysis ra
        JOIN unified_reviews ur
            ON ur.id = ra.unified_review_id
        WHERE ra.sentiment = 'negative'
        AND ur.created_at >= (
            SELECT MAX(ur2.created_at) - INTERVAL '24 hours'
            FROM unified_reviews ur2
        )
        GROUP BY ur.location_id
        HAVING COUNT(*) >= 3;
    """)

    results = cursor.fetchall()
    
    alerts = []

    for location_id, count in results:

        alerts.append({
            "severity": "ALTA",
            "location_id": location_id,
            "message": f"{count} reseñas negativas en 24h",
            "rule_code": "HIGH_NEGATIVE_24H"
        })
    return alerts

'''Detectar alertas nivel medio'''
def detect_medium_alerts(cursor):

    cursor.execute("""
        SELECT
            ur.location_id,
            AVG(ur.rating) as avg_rating
        FROM unified_reviews ur
        WHERE ur.created_at >= (
            SELECT MAX(created_at) - INTERVAL '7 days'
            FROM unified_reviews
        )
        GROUP BY ur.location_id
        HAVING AVG(ur.rating) < 3.5
    """)

    results = cursor.fetchall()

    alerts = []

    for location_id, avg_rating in results:

        alerts.append({
            "severity": "MEDIA",
            "location_id": location_id,
            "message": f"Rating promedio semanal bajo: {avg_rating:.2f}",
            "rule_code": "LOW_WEEKLY_RATING"
        })
    return alerts

def run_detector():

    conn = get_connection()
    cursor = conn.cursor()

    alerts = []
    alerts += detect_critical_alerts(cursor)
    alerts += detect_high_alerts(cursor)
    alerts += detect_medium_alerts(cursor)
    save_alerts(cursor, alerts)

    conn.commit()
    cursor.close()
    conn.close()

    print(f"{len(alerts)} alertas generadas")

if __name__ == "__main__":
    run_detector()
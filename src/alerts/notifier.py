import json
from datetime import datetime, timezone
import psycopg2
from pathlib import Path

LOG_FILE = Path("alerts_log.json")

def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="brewmaster",
        user="katherin"
    )

def fetch_alerts():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT severity, location_id, message, rule_code, created_at
        FROM alerts
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    alerts = []

    for severity, location_id, message, rule_code, created_at in rows:
        alerts.append({
            "severity": severity,
            "location_id": location_id,
            "message": message,
            "rule_code": rule_code,
            "created_at": created_at.isoformat()
        })
    return alerts

def write_json_log(alerts):

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "alerts": alerts
    }

    with open(LOG_FILE, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"{len(alerts)} alertas registradas en {LOG_FILE}")

def run_notifier():

    alerts = fetch_alerts()

    write_json_log(alerts)

if __name__ == "__main__":
    run_notifier()
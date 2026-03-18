import subprocess

def run_command(command):
    print(f"\n▶ Ejecutando: {command}")
    subprocess.run(command, shell=True, check=True)

if __name__ == "__main__":

    print("🚀 Ejecutando sistema completo...")

    # ETL
    run_command("python src/etl/pipeline.py")
    # LLM
    run_command("python src/analysis/llm_analyzer.py")
    # Alerts
    run_command("python src/alerts/detector.py")
    # Notifier
    run_command("python src/alerts/notifier.py")
    # Weekly_report
    run_command("python -m src.reports.weekly_report")

    print("\n✅ Proceso completo finalizado")
BrewMaster FeedbackIQ 

Sistema de análisis de reseñas para una cadena de cafeterías.
El proyecto implementa un pipeline ETL que consolida reseñas desde dos distintas fuentes, analiza las reseñas y comentarios utilizando un LLM y genera alertas automáticas para problemas operativos.


-Reporte Semanal-

El sistema genera automáticamente un reporte semanal con métricas clave:

    - Total de reseñas procesadas
    - Distribución de sentimientos
    - Top 3 locales mejor valorados
    - Top 3 locales con más problemas
    - Categorías más mencionadas
    - Resumen ejecutivo generado por el LLM

El reporte se guarda en: docs/weekly_report.html


-Arquitectura del Sistema-

El flujo de datos es el siguiente:

    - API Reviews (FastAPI) + customer_surveys (PotsgreSQL)
    - ETL Pipeline
    - unified_reviews (table)
    - LLM Analysis
    - review_analysis (table)
    - Alerts Detector
    - alerts (table)
    - Notifier 
    - alerts_log.json
    - Weekly Report (HTML en docs/)


-Estructura del Proyecto-

brewmaster_feedbackiq
    api     
        main.py
    db
        seed.sql
    docs
        weekly_report.html
    src
        alerts
            detector.py
            notifier.py
        analysis
            llm_analyzer.py
            prompts.py
        etl
            extractors.py
            transformers.py
            pipeline.py
        reports
            weekly_report.py
    test  
        conftest.py
        test_analysis.py
        test_etl.py
    run.py
    README.md
    requirements.txt


-Requisitos-

    - Python 3.10+
    - PostgreSQL
    - API Key de OpenAI


-Configuración del Entorno Virtual-

Crear entorno virtual:
    python3 -m venv venv
    source venv/bin/activate

Instalar dependencias:
    pip install -r requirements.txt


-Variables del Entorno-

    Configurar la API Key de OpenAI:
        export OPENAI_API_KEY = "api_key_aqui"


-Configuración de la Base de Datos-

Crear la base:
    createdb brewmaster

Cargar datos de ejemplo:
    psql brewmaster < db/seed.sql
    (Crea la tabla de customer_surveys con datos de ejemplo)


-Ejecutar la API de Reseñas-

En una terminal separada, desde la carpeta del proyecto:
    uvicorn src.api.main:app --reload --port 8081

Endpoint disponible:
    GET /api/reviews?location_id={id}&since={date}


-Ejecutar Todo el Sistema-

Una vez configurado todo:
    python run.py

Este comando ejecuta:
    - ETL pipeline
    - Análisis con LLM
    - Generación de alertas
    - Notificación (archivo JSON)
    - Generación de reporte semanal (HTML en docs/)


-Tests-

Se incluyen tests básicos para validar:

    - Transformaciones del ETL
    - Estructura de prompts del LLM

Ejecutar tests:

    pytest


-Reglas de Alerta-

    - CRÍTICA: Reseñas con urgencia = 5
    - ALTA: 3+ reseñas negativas del mismo local en 24h
    - MEDIA: Rating promedio < 3.5 en la última semana


-Características Principales del Sistema-

    - Extracción de datos desde API y PostgreSQL (últimos 7 días)
    - Normalización de datos en un esquema unificado
    - Deduplicación con clave (source, source_review_id)
    - Pipeline idempotente
    - Análisis automático con LLM
    - Generación de alertas
    - Notificación mediante log estructurado JSON
    - Generación de reporte semanal automatizado


-Modelo LLM-

    - Se utiliza OpenAI gpt-4o-mini para:
    - Análisis de sentimiento
    - Clasificación por categorías
    - Generación de resumen
    - Cálculo de nivel de urgencia
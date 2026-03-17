def analysis_prompt(text, rating=None):

    rating_context = f"\nRating del cliente: {rating}" if rating else ""
    prompt = f"""
        Eres un analista experto en feedback de clientes para una cadena de cafeterías.
        Tu tarea es analizar reseñas de clientes y extraer información estructurada.
        Debes devolver SOLO un JSON válido con esta estructura:
        {{
        "sentiment": "positive | negative | neutral",
        "categories": ["producto | servicio | ambiente | precio | limpieza | otro"],
        "summary": "máximo 100 caracteres",
        "urgency": 1-5
        }}

        Reglas de clasificación:

        SENTIMENT
        positive → cliente satisfecho o experiencia positiva
        negative → queja, problema o experiencia negativa
        neutral → comentario informativo o mixto sin emoción fuerte

        CATEGORIES (Selecciona máximo 2 categorías relevantes)
        producto → calidad del café o comida
        servicio → atención del personal, rapidez, trato
        ambiente → ruido, comodidad, espacio, clima del local
        precio → costo o percepción de caro/barato
        limpieza → higiene del local o baños
        otro → si no encaja en las anteriores

        URGENCY
        1 → comentario positivo o sin problema
        2 → sugerencia menor
        3 → problema moderado
        4 → queja clara que requiere atención
        5 → problema grave o crítico (higiene, salud, mala atención severa)

        Ejemplos:

        Review: "El cappuccino estuvo delicioso"
        Output:
        {{"sentiment":"positive","categories":["producto"],"summary":"Cliente satisfecho con el cappuccino","urgency":1}}
        
        Review: "El servicio fue muy lento"
        Output:
        {{"sentiment":"negative","categories":["servicio"],"summary":"Cliente reporta servicio lento","urgency":3}}
        
        Review: "El baño estaba muy sucio"
        Output:
        {{"sentiment":"negative","categories":["limpieza"],"summary":"Cliente reporta mala higiene en el baño","urgency":5}}

        Ahora analiza la siguiente reseña: {text}
        Rating del cliente: {rating_context}
        """
    return prompt

def summary_prompt(total, sentiment, top_locations, problem_locations, categories):

    return f"""Eres un analista senior de negocio para una cadena de cafeterías.
    Genera un resumen ejecutivo claro y profesional (máx 120 palabras)
    basado en estos datos:

    Total de reseñas: {total}
    Distribución de sentimiento: {sentiment}
    Mejores locales: {top_locations}
    Locales con más problemas: {problem_locations}
    Categorías más mencionadas:b{categories}

    El resumen debe:
    - Ser claro y accionable
    - Destacar problemas importantes 
    - Identificar oportunidades
    - Tener tono ejecutivo"""
from fastapi import FastAPI
from typing import Optional
from datetime import datetime

app = FastAPI()

reviews = [
{"review_id":"r1","location_id":1,"rating":5,"text":"El cappuccino es excelente","author":"Laura","created_at":"2026-03-01T09:00:00Z"},
{"review_id":"r2","location_id":2,"rating":4,"text":"Buen café pero el servicio fue un poco lento","author":"Carlos","created_at":"2026-03-01T10:00:00Z"},
{"review_id":"r3","location_id":3,"rating":3,"text":"El lugar estaba lleno pero el café estaba bien","author":"Ana","created_at":"2026-03-01T11:00:00Z"},
{"review_id":"r4","location_id":4,"rating":2,"text":"El café llegó frío","author":"Miguel","created_at":"2026-03-01T12:00:00Z"},
{"review_id":"r5","location_id":5,"rating":5,"text":"Me encanta el ambiente de esta cafetería","author":"Luisa","created_at":"2026-03-01T13:00:00Z"},
{"review_id":"r6","location_id":6,"rating":4,"text":"Buen lugar para trabajar un rato","author":"Daniel","created_at":"2026-03-01T14:00:00Z"},
{"review_id":"r7","location_id":7,"rating":3,"text":"Nada especial, café normal","author":"Jorge","created_at":"2026-03-01T15:00:00Z"},
{"review_id":"r8","location_id":8,"rating":1,"text":"El baño estaba muy sucio","author":"Paula","created_at":"2026-03-01T16:00:00Z"},
{"review_id":"r9","location_id":9,"rating":5,"text":"El cappuccino es excelente","author":"Andrés","created_at":"2026-03-01T17:00:00Z"},
{"review_id":"r10","location_id":10,"rating":4,"text":"Buen café pero el servicio fue un poco lento","author":"Sara","created_at":"2026-03-01T18:00:00Z"},

{"review_id":"r11","location_id":11,"rating":3,"text":"El lugar estaba lleno pero el café estaba bien","author":"Mateo","created_at":"2026-03-02T09:00:00Z"},
{"review_id":"r12","location_id":12,"rating":2,"text":"El café llegó frío","author":"Lucía","created_at":"2026-03-02T10:00:00Z"},
{"review_id":"r13","location_id":13,"rating":5,"text":"Me encanta el ambiente de esta cafetería","author":"Pedro","created_at":"2026-03-02T11:00:00Z"},
{"review_id":"r14","location_id":14,"rating":4,"text":"Buen lugar para trabajar un rato","author":"Sofía","created_at":"2026-03-02T12:00:00Z"},
{"review_id":"r15","location_id":15,"rating":3,"text":"Nada especial, café normal","author":"David","created_at":"2026-03-02T13:00:00Z"},
{"review_id":"r16","location_id":1,"rating":1,"text":"El baño estaba muy sucio","author":"Elena","created_at":"2026-03-02T14:00:00Z"},
{"review_id":"r17","location_id":2,"rating":5,"text":"Excelente atención y café delicioso","author":"Camila","created_at":"2026-03-02T15:00:00Z"},
{"review_id":"r18","location_id":3,"rating":4,"text":"Los croissants estaban muy frescos","author":"Luis","created_at":"2026-03-02T16:00:00Z"},
{"review_id":"r19","location_id":4,"rating":3,"text":"Un sitio tranquilo para conversar","author":None,"created_at":"2026-03-02T17:00:00Z"},
{"review_id":"r20","location_id":5,"rating":2,"text":"Demasiado ruido para trabajar","author":"Andrea","created_at":"2026-03-02T18:00:00Z"},

{"review_id":"r21","location_id":6,"rating":5,"text":"Muy buen latte","author":"Juan","created_at":"2026-03-03T09:00:00Z"},
{"review_id":"r22","location_id":7,"rating":4,"text":"La atención fue amable","author":"Valentina","created_at":"2026-03-03T10:00:00Z"},
{"review_id":"r23","location_id":8,"rating":3,"text":"Café normal, nada fuera de lo común","author":"Oscar","created_at":"2026-03-03T11:00:00Z"},
{"review_id":"r24","location_id":9,"rating":1,"text":"Me cobraron dos veces el mismo café","author":"Natalia","created_at":"2026-03-03T12:00:00Z"},
{"review_id":"r25","location_id":10,"rating":5,"text":"Excelente música y ambiente","author":"Esteban","created_at":"2026-03-03T13:00:00Z"},
{"review_id":"r26","location_id":11,"rating":4,"text":"El espresso estaba muy bueno","author":"María","created_at":"2026-03-03T14:00:00Z"},
{"review_id":"r27","location_id":12,"rating":3,"text":"Servicio promedio","author":"Ricardo","created_at":"2026-03-03T15:00:00Z"},
{"review_id":"r28","location_id":13,"rating":2,"text":"Tardaron mucho en traer el pedido","author":"Carolina","created_at":"2026-03-03T16:00:00Z"},
{"review_id":"r29","location_id":14,"rating":5,"text":"El cappuccino es excelente","author":"Fernando","created_at":"2026-03-03T17:00:00Z"},
{"review_id":"r30","location_id":15,"rating":4,"text":"Buen café pero el servicio fue un poco lento","author":"Laura","created_at":"2026-03-03T18:00:00Z"},

{"review_id":"r31","location_id":1,"rating":3,"text":"El lugar estaba lleno pero el café estaba bien","author":"Carlos","created_at":"2026-03-04T09:00:00Z"},
{"review_id":"r32","location_id":2,"rating":2,"text":"El café llegó frío","author":"Ana","created_at":"2026-03-04T10:00:00Z"},
{"review_id":"r33","location_id":3,"rating":5,"text":"Me encanta el ambiente de esta cafetería","author":"Miguel","created_at":"2026-03-04T11:00:00Z"},
{"review_id":"r34","location_id":4,"rating":4,"text":"Buen lugar para trabajar un rato","author":"Luisa","created_at":"2026-03-04T12:00:00Z"},
{"review_id":"r35","location_id":5,"rating":3,"text":"Nada especial, café normal","author":"Daniel","created_at":"2026-03-04T13:00:00Z"},
{"review_id":"r36","location_id":6,"rating":1,"text":"El baño estaba muy sucio","author":"Jorge","created_at":"2026-03-04T14:00:00Z"},
{"review_id":"r37","location_id":7,"rating":5,"text":"Muy buen servicio","author":"Paula","created_at":"2026-03-04T15:00:00Z"},
{"review_id":"r38","location_id":8,"rating":4,"text":"Las mesas estaban limpias","author":"Andrés","created_at":"2026-03-04T16:00:00Z"},
{"review_id":"r39","location_id":9,"rating":3,"text":"Un café normal","author":None,"created_at":"2026-03-04T17:00:00Z"},
{"review_id":"r40","location_id":10,"rating":2,"text":"El latte estaba demasiado dulce","author":"Sara","created_at":"2026-03-04T18:00:00Z"},

{"review_id":"r41","location_id":11,"rating":5,"text":"Excelente café y atención","author":"Mateo","created_at":"2026-03-05T09:00:00Z"},
{"review_id":"r42","location_id":12,"rating":4,"text":"Buen ambiente","author":"Lucía","created_at":"2026-03-05T10:00:00Z"},
{"review_id":"r43","location_id":13,"rating":3,"text":"Todo normal","author":"Pedro","created_at":"2026-03-05T11:00:00Z"},
{"review_id":"r44","location_id":14,"rating":1,"text":"Creo que el sándwich estaba en mal estado, me sentí mal después de comerlo","author":"Sofía","created_at":"2026-03-05T12:00:00Z"},
{"review_id":"r45","location_id":15,"rating":5,"text":"El cappuccino es excelente","author":"David","created_at":"2026-03-05T13:00:00Z"},
{"review_id":"r46","location_id":1,"rating":4,"text":"Buen café pero el servicio fue un poco lento","author":"Elena","created_at":"2026-03-05T14:00:00Z"},
{"review_id":"r47","location_id":2,"rating":3,"text":"El lugar estaba lleno pero el café estaba bien","author":"Camila","created_at":"2026-03-05T15:00:00Z"},
{"review_id":"r48","location_id":3,"rating":2,"text":"El café llegó frío","author":"Luis","created_at":"2026-03-05T16:00:00Z"},
{"review_id":"r49","location_id":4,"rating":5,"text":"Me encanta el ambiente de esta cafetería","author":"Andrea","created_at":"2026-03-05T17:00:00Z"},
{"review_id":"r50","location_id":5,"rating":4,"text":"Buen lugar para trabajar un rato","author":"Juan","created_at":"2026-03-05T18:00:00Z"},

{"review_id":"r51","location_id":6,"rating":3,"text":"Nada especial, café normal","author":"Valentina","created_at":"2026-03-06T09:00:00Z"},
{"review_id":"r52","location_id":7,"rating":1,"text":"El baño estaba muy sucio","author":"Oscar","created_at":"2026-03-06T10:00:00Z"},
{"review_id":"r53","location_id":8,"rating":5,"text":"Excelente café","author":"Natalia","created_at":"2026-03-06T11:00:00Z"},
{"review_id":"r54","location_id":9,"rating":4,"text":"Muy buen latte","author":"Esteban","created_at":"2026-03-06T12:00:00Z"},
{"review_id":"r55","location_id":10,"rating":3,"text":"Un sitio tranquilo","author":"María","created_at":"2026-03-06T13:00:00Z"},
{"review_id":"r56","location_id":11,"rating":2,"text":"El café sabía quemado","author":"Ricardo","created_at":"2026-03-06T14:00:00Z"},
{"review_id":"r57","location_id":12,"rating":5,"text":"Servicio rápido y amable","author":"Carolina","created_at":"2026-03-06T15:00:00Z"},
{"review_id":"r58","location_id":13,"rating":4,"text":"Muy buen espresso","author":"Fernando","created_at":"2026-03-06T16:00:00Z"},
{"review_id":"r59","location_id":14,"rating":3,"text":"Todo bien","author":None,"created_at":"2026-03-06T17:00:00Z"},
{"review_id":"r60","location_id":15,"rating":2,"text":"Muy demorado el pedido","author":"Laura","created_at":"2026-03-06T18:00:00Z"},

{"review_id":"r61","location_id":1,"rating":5,"text":"Excelente experiencia","author":"Carlos","created_at":"2026-03-07T09:00:00Z"},
{"review_id":"r62","location_id":2,"rating":4,"text":"Buen café","author":"Ana","created_at":"2026-03-07T10:00:00Z"},
{"review_id":"r63","location_id":3,"rating":3,"text":"Normal","author":"Miguel","created_at":"2026-03-07T11:00:00Z"},
{"review_id":"r64","location_id":4,"rating":2,"text":"La mesa estaba pegajosa","author":"Luisa","created_at":"2026-03-07T12:00:00Z"},
{"review_id":"r65","location_id":5,"rating":1,"text":"Encontré un insecto en la bebida","author":"Daniel","created_at":"2026-03-07T13:00:00Z"},
{"review_id":"r66","location_id":6,"rating":5,"text":"Excelente capuccino","author":"Jorge","created_at":"2026-03-07T14:00:00Z"},
{"review_id":"r67","location_id":7,"rating":4,"text":"Buen servicio","author":"Paula","created_at":"2026-03-07T15:00:00Z"},
{"review_id":"r68","location_id":8,"rating":3,"text":"Café normal","author":"Andrés","created_at":"2026-03-07T16:00:00Z"},
{"review_id":"r69","location_id":9,"rating":2,"text":"Muy caro para lo que ofrecen","author":"Sara","created_at":"2026-03-07T17:00:00Z"},
{"review_id":"r70","location_id":10,"rating":5,"text":"Muy buena experiencia","author":"Mateo","created_at":"2026-03-07T18:00:00Z"},

{"review_id":"r71","location_id":11,"rating":4,"text":"Buen ambiente","author":"Lucía","created_at":"2026-03-08T09:00:00Z"},
{"review_id":"r72","location_id":12,"rating":3,"text":"Todo normal","author":"Pedro","created_at":"2026-03-08T10:00:00Z"},
{"review_id":"r73","location_id":13,"rating":2,"text":"El café estaba tibio","author":"Sofía","created_at":"2026-03-08T11:00:00Z"},
{"review_id":"r74","location_id":14,"rating":1,"text":"El barista fue muy grosero","author":"David","created_at":"2026-03-08T12:00:00Z"},
{"review_id":"r75","location_id":15,"rating":5,"text":"Excelente café","author":"Elena","created_at":"2026-03-08T13:00:00Z"},
{"review_id":"r76","location_id":1,"rating":4,"text":"Muy buen latte","author":"Camila","created_at":"2026-03-08T14:00:00Z"},
{"review_id":"r77","location_id":2,"rating":3,"text":"Un sitio tranquilo","author":"Luis","created_at":"2026-03-08T15:00:00Z"},
{"review_id":"r78","location_id":3,"rating":2,"text":"Demasiado calor dentro del local","author":"Andrea","created_at":"2026-03-08T16:00:00Z"},
{"review_id":"r79","location_id":4,"rating":1,"text":"Creo que me intoxiqué después de tomar el café","author":"Juan","created_at":"2026-03-08T17:00:00Z"},
{"review_id":"r80","location_id":5,"rating":5,"text":"Muy buena atención","author":"Valentina","created_at":"2026-03-08T18:00:00Z"},

{"review_id":"r81","location_id":6,"rating":4,"text":"Buen café","author":"Oscar","created_at":"2026-03-09T09:00:00Z"},
{"review_id":"r82","location_id":7,"rating":3,"text":"Normal","author":"Natalia","created_at":"2026-03-09T10:00:00Z"},
{"review_id":"r83","location_id":8,"rating":2,"text":"Muy lento el servicio","author":"Esteban","created_at":"2026-03-09T11:00:00Z"},
{"review_id":"r84","location_id":9,"rating":1,"text":"El local estaba muy sucio","author":"María","created_at":"2026-03-09T12:00:00Z"},
{"review_id":"r85","location_id":10,"rating":5,"text":"Excelente ambiente","author":"Ricardo","created_at":"2026-03-09T13:00:00Z"},
{"review_id":"r86","location_id":11,"rating":4,"text":"Buen lugar","author":"Carolina","created_at":"2026-03-09T14:00:00Z"},
{"review_id":"r87","location_id":12,"rating":3,"text":"Café promedio","author":"Fernando","created_at":"2026-03-09T15:00:00Z"},
{"review_id":"r88","location_id":13,"rating":2,"text":"El pedido llegó equivocado","author":"Laura","created_at":"2026-03-09T16:00:00Z"},
{"review_id":"r89","location_id":14,"rating":1,"text":"Me cobraron de más en la cuenta","author":"Carlos","created_at":"2026-03-09T17:00:00Z"},
{"review_id":"r90","location_id":15,"rating":5,"text":"Muy buen café","author":"Ana","created_at":"2026-03-09T18:00:00Z"},

{"review_id":"r91","location_id":1,"rating":4,"text":"Buen ambiente","author":"Miguel","created_at":"2026-03-10T09:00:00Z"},
{"review_id":"r92","location_id":2,"rating":3,"text":"Todo bien","author":"Luisa","created_at":"2026-03-10T10:00:00Z"},
{"review_id":"r93","location_id":3,"rating":2,"text":"El café estaba frío","author":"Daniel","created_at":"2026-03-10T11:00:00Z"},
{"review_id":"r94","location_id":4,"rating":1,"text":"El baño olía muy mal","author":"Jorge","created_at":"2026-03-10T12:00:00Z"},
{"review_id":"r95","location_id":5,"rating":5,"text":"Excelente servicio","author":"Paula","created_at":"2026-03-10T13:00:00Z"},
{"review_id":"r96","location_id":6,"rating":4,"text":"Buen café","author":"Andrés","created_at":"2026-03-10T14:00:00Z"},
{"review_id":"r97","location_id":7,"rating":3,"text":"Normal","author":"Sara","created_at":"2026-03-10T15:00:00Z"},
{"review_id":"r98","location_id":8,"rating":2,"text":"Demasiado demorado","author":"Mateo","created_at":"2026-03-10T16:00:00Z"},
{"review_id":"r99","location_id":9,"rating":1,"text":"Encontré cabello en mi bebida","author":"Lucía","created_at":"2026-03-10T17:00:00Z"},
{"review_id":"r100","location_id":10,"rating":5,"text":"Excelente café y ambiente","author":"Pedro","created_at":"2026-03-10T18:00:00Z"}
]

@app.get("/api/reviews")
def get_reviews(location_id: int, since: Optional[str] = None):

    filtered_reviews = [
        r for r in reviews
        if r["location_id"] == location_id
    ]

    if since:
        since_date = datetime.fromisoformat(since.replace("Z", "+00:00"))

        filtered_reviews = [
            r for r in filtered_reviews
            if datetime.fromisoformat(r["created_at"].replace("Z", "+00:00")) >= since_date
        ]

    return filtered_reviews
# El grafo va a tener cuatro nodos. Cada uno es un agente especializado con un rol específico:

Nodo 1 — Clasificador: Recibe la consulta del usuario y determina el tipo de problema. Por ejemplo: reclamo, consulta técnica, consulta de envío, solicitud de reembolso, spam.

Nodo 2 — Buscador: Según la categoría, busca información relevante en una base de conocimiento. Por ahora va a ser un diccionario con respuestas predefinidas por categoría — después se puede conectar a una base de datos real.

Nodo 3 — Redactor: Toma la categoría y la información encontrada y redacta una respuesta profesional y empática para el cliente.

Nodo 4 — Revisor: Lee la respuesta redactada y verifica que sea correcta, completa y profesional antes de enviarla.
El estado compartido que viaja entre todos los nodos va a tener:

consulta — el mensaje original del cliente
categoria — lo que determinó el clasificador
informacion — lo que encontró el buscador
respuesta — lo que redactó el redactor
respuesta_final — lo que aprobó el revisor


estado.py porque es la base de todo el sistema — define qué información viaja entre los nodos.
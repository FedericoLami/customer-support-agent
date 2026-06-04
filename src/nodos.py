import anthropic
from dotenv import load_dotenv
from conocimiento import BASE_CONOCIMIENTO

load_dotenv()

client = anthropic.Anthropic()

def nodo_clasificador(estado):
    mensajes = [{"role" : "user", "content" : estado["consulta"]}]

    answer = client.messages.create(
        model = "claude-haiku-4-5",
        max_tokens = 1024,
        system = """"
                Sos un clasificador de consultas de atención al cliente.
                Respondé únicamente con una de estas categorías en texto plano, sin JSON ni explicaciones:
                reclamo, consulta_tecnica, consulta_envio, reembolso, spam
             """,
        messages = mensajes
    )

    estado["categoria"] = answer.content[0].text
    return estado 


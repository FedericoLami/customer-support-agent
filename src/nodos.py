import anthropic
from dotenv import load_dotenv
from src.conocimiento import BASE_CONOCIMIENTO

load_dotenv()

client = anthropic.Anthropic()

def nodo_clasificador(estado):
    mensajes = [{"role" : "user", "content" : estado["consulta"]}]

    answer = client.messages.create(
        model = "claude-haiku-4-5",
        max_tokens = 1024,
        system = """
                Sos un clasificador de consultas de atención al cliente.
                Respondé únicamente con una de estas categorías en texto plano, sin JSON ni explicaciones.

                Categorías y ejemplos:
                - reclamo: producto dañado, producto incorrecto, mal servicio recibido
                - consulta_tecnica: problemas de instalación, configuración, el producto no funciona
                - consulta_envio: dónde está mi pedido, número de seguimiento, demora en entrega
                - reembolso: quiero devolver, quiero que me devuelvan el dinero, cancelar compra
                - spam: mensajes sin sentido, publicidad, texto aleatorio, consultas que no tienen relación con compras o productos

                Respondé solo con la palabra de la categoría correspondiente.
                Si el mensaje contiene texto sin sentido, palabras aleatorias, o no tiene una consulta clara relacionada con compras o soporte, clasificalo como spam.
                - spam: texto sin sentido, palabras aleatorias, oraciones religiosas o poéticas sin relación con compras, lorem ipsum, mensajes que no son consultas de clientes.
             """,
        messages = mensajes
    )

    estado["categoria"] = answer.content[0].text
    return estado 


def nodo_buscador(estado):
    if estado["categoria"] in BASE_CONOCIMIENTO:
       estado["informacion"] = BASE_CONOCIMIENTO[estado["categoria"]]
    return estado


def nodo_redactor(estado):

    if estado["categoria"].strip() == "spam":
        estado["respuesta"] = "Tu mensaje no corresponde a una consulta válida. Si necesitás ayuda, escribinos con tu consulta."
        return estado

    mensajes = [{"role" : "user", "content" : f"Consulta del cliente: {estado['consulta']}\nInformación de política: {estado['informacion']}"}]

    answer = client.messages.create(
        model = "claude-haiku-4-5",
        max_tokens = 1024,
        system = """
                Sos un agente de atención al cliente profesional y empático.
                Redactá una respuesta directa al cliente basándote en su consulta y la información de política provista.
                Respondé en texto plano, sin JSON ni explicaciones adicionales.
                No hagas preguntas de seguimiento al final de la respuesta.
             """,
        messages = mensajes
    )

    estado["respuesta"] = answer.content[0].text
    return estado 

def nodo_revisor(estado):
    
    if estado["categoria"].strip() == "spam":
        estado["respuesta_final"] = estado["respuesta"]
        return estado
    
    mensajes = [{"role" : "user", "content" : f"Consulta original del cliente: {estado['consulta']}\nRespuesta a revisar: {estado['respuesta']}"}]

    answer = client.messages.create(
        model = "claude-haiku-4-5",
        max_tokens = 1024,
        system = """
                Sos un agente de revision de respuestas de atencion al cliente profesional.
                Redactá una respuesta final directa y empatica al cliente basándote en la respuesta que recibas teniendo en cuenta
                la información de política provista.
                Respondé en texto plano, sin JSON ni explicaciones adicionales.
                No hagas preguntas de seguimiento al final de la respuesta.
             """,
        messages = mensajes
    )
    estado["respuesta_final"] = answer.content[0].text
    return estado

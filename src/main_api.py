from pydantic import BaseModel
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.agente import grafo_app 


class MensajeRequest(BaseModel):
    mensaje:str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analizar")
def analizar_mensaje(request: MensajeRequest):
    try:
        resultado = grafo_app.invoke({"consulta": request.mensaje, "categoria": "", "informacion": "", "respuesta": "", "respuesta_final": ""})
        return {"respuesta": resultado["respuesta_final"], "categoria": resultado["categoria"]}
    except ValueError:
        raise HTTPException(status_code=500, detail="Error al procesar la respuesta de Claude")

# Customer Support Agent — Sistema Multi-Agente con LangGraph

Sistema de atención al cliente construido con **LangGraph** y **Claude AI** que procesa consultas en lenguaje natural a través de un pipeline de cuatro agentes especializados. Cada agente tiene un rol específico — clasificar, buscar, redactar y revisar — trabajando en secuencia para generar respuestas profesionales y empáticas sin intervención humana.

Pensado para empresas que quieren automatizar su primera línea de atención al cliente usando inteligencia artificial, con respuestas coherentes a su política comercial.

---

## Demo

![Demo del sistema](demo.gif)

---

## Tecnologías utilizadas

| Capa | Tecnología |
|------|-----------|
| Orquestación de agentes | LangGraph |
| Modelo de lenguaje | Claude Haiku (Anthropic API) |
| Backend / API REST | FastAPI + Uvicorn |
| Frontend | HTML · CSS · JavaScript vanilla |
| Configuración | python-dotenv |
| Entorno | Python 3.11 + venv |

---

## Arquitectura del sistema

```
customer-support-agent/
├── src/
│   ├── estado.py          # Definición del estado compartido del grafo
│   ├── conocimiento.py    # Base de conocimiento con políticas de la empresa
│   ├── nodos.py           # Funciones de los 4 agentes
│   ├── agente.py          # Construcción y compilación del grafo LangGraph
│   └── main_api.py        # API REST con FastAPI
├── index.html             # Interfaz web
├── .env                   # Variables de entorno (no se sube a GitHub)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ¿Cómo funciona el pipeline?

El sistema usa un grafo dirigido donde cada nodo es un agente especializado. El estado se comparte entre todos los nodos y se enriquece en cada paso.

```
consulta del cliente
        ↓
[1. Clasificador] — determina la categoría de la consulta
        ↓
[2. Buscador] — recupera la política comercial correspondiente
        ↓
[3. Redactor] — genera una respuesta profesional y empática
        ↓
[4. Revisor] — verifica calidad y coherencia antes de enviar
        ↓
respuesta final al cliente
```

**Estado compartido entre nodos:**

```python
class EstadoConsulta(TypedDict):
    consulta: str          # mensaje original del cliente
    categoria: str         # determinada por el clasificador
    informacion: str       # política recuperada por el buscador
    respuesta: str         # redactada por el redactor
    respuesta_final: str   # aprobada por el revisor
```

---

## Categorías de consultas

| Categoría | Descripción |
|-----------|------------|
| `reclamo` | Producto dañado, incorrecto o mal servicio |
| `consulta_envio` | Seguimiento, demoras o problemas con el envío |
| `reembolso` | Devoluciones y cancelaciones de compra |
| `consulta_tecnica` | Problemas de instalación o configuración |
| `spam` | Mensajes no válidos o sin relación con compras |

Las respuestas para spam se cortocircuitan antes del redactor — no consumen tokens de Claude innecesariamente.

---

## Personalización

La base de conocimiento en `src/conocimiento.py` es el único archivo que necesita modificarse para adaptar el sistema a una empresa específica. Contiene las políticas comerciales por categoría que el agente usa para redactar sus respuestas.

```python
BASE_CONOCIMIENTO = {
    "reclamo": "Los reclamos se gestionan en 48 horas hábiles...",
    "reembolso": "Los reembolsos se procesan en 5 a 10 días hábiles...",
    ...
}
```

---

## Endpoint de la API

### `POST /analizar`

Recibe una consulta en lenguaje natural y devuelve la respuesta del agente junto con la categoría detectada.

**Request:**
```json
{
  "mensaje": "Mi pedido llegó roto y nadie me responde"
}
```

**Response:**
```json
{
  "respuesta": "Entiendo tu frustración...",
  "categoria": "reclamo"
}
```

---

## Instalación y uso

### Requisitos previos

- Python 3.11
- API Key de Anthropic ([console.anthropic.com](https://console.anthropic.com))

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/FedericoLami/customer-support-agent.git
cd customer-support-agent

# 2. Crear y activar entorno virtual
py -3.11 -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
# Crear archivo .env en la raíz del proyecto:
ANTHROPIC_API_KEY=tu-api-key-aquí

# 5. Iniciar el servidor
uvicorn src.main_api:app --reload
```

### Interfaz web

Con el servidor corriendo, abrí `index.html` directamente en el navegador.

### Documentación interactiva de la API

```
http://127.0.0.1:8000/docs
```

---

## Trabajo futuro

- Conectar la base de conocimiento a una base de datos real para actualizaciones sin tocar el código
- Agregar autenticación en la API para uso en producción
- Implementar rate limiting para detección automática de spam por frecuencia de requests
- Agregar un nodo de escalamiento que derive consultas complejas a un agente humano
- Persistencia de conversaciones para seguimiento de casos

---

## Autor

**Federico Lami**
[LinkedIn](https://www.linkedin.com/in/federicolami/) · [GitHub](https://github.com/FedericoLami/customer-support-agent)
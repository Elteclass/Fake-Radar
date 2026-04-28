# uvicorn main:app --reload, that's the command to run this backend server in development mode. It will auto-reload on code changes.

import logging
import os
from datetime import datetime
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
import json

# Importacion de modelos y servicio de AI
from models import AnalyzeRequest, AnalyzeResponse
from services.ai_service import generate_response
from services.beto_service import analyze_style

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Se crea la instancia de FastAPI
app = FastAPI(
    title="Fake Radar API",
    description="API para detección de desinformación. Motor Stateless.",
    version="1.2.1"
)

# Configuración de CORS: Esto es vital para que el Frontend (React) 
# y la extension de Chrome puedan hablar con este backend sin que el navegador los bloquee.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint de prueba para verificar que el backend está funcionando correctamente. Devuelve un mensaje simple en formato JSON.
@app.get("/")
async def root():
    return {"message": "El backend de Fake Radar esta en linea."}

# EL ENDPOINT PRINCIPAL: /analyze
@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_news(request: AnalyzeRequest):

    # Se ejecuta el análisis de estilo con BETO
    beto_data = analyze_style(request.text)
    
    # Se construye el prompt para gemini, incluyendo el texto de la noticia y las instrucciones claras para el JSON valido
    prompt = f"""
    Eres un sistema experto en detección de desinformación y fact-checking periodístico.
    Tu tono es objetivo, frío y analítico. No emitas opiniones personales.

    Analiza la siguiente noticia utilizando los resultados de búsqueda web que tienes disponibles:

    {request.text}

    INSTRUCCIONES OBLIGATORIAS:
    - Debes usar los resultados de la búsqueda web proporcionada para contrastar y verificar la noticia.
    - Devuelve la respuesta en formato JSON sin ningún marcador Markdown como ```json.
    - NO incluyas texto antes ni después del JSON.
    - NO uses markdown, bloques de código ni ningún otro formato.
    - El campo "references" debe contener únicamente los enlaces reales que consultaste durante la búsqueda web, no inventes URLs.
    - Si no encuentras fuentes reales, devuelve "references" como lista vacía [].
    - Si no puedes cumplir el formato, responde con un JSON válido con valores por defecto.

    REGLAS DE VALORES:
    - global_assessment: "Verdadero" | "Dudoso" | "Falso"
    - verdict: "Verificado" | "Falso" | "Engañoso" | "Requiere verificación" | "No verificable"
    - reasoning: resumen de 2-3 líneas explicando por qué tomaste esa decisión, basado en lo que encontraste en la web
    - references: lista de máximo 5 fuentes reales consultadas durante la búsqueda, o []

    FORMATO OBLIGATORIO (responde SOLO esto, sin ningún texto adicional):
    {{
      "global_assessment": "Falso",
      "fact_check_analysis": {{
        "engine": "Gemini API + Web Search",
        "verdict": "Falso",
        "reasoning": "Explicación basada en los resultados de búsqueda web aquí",
        "references": [
          {{
            "title": "Título de la fuente real consultada",
            "url": "https://url-real-consultada.com/articulo",
            "domain": "url-real-consultada.com"
          }}
        ]
      }}
    }}
    """
    
    # Se llama a la funcion que se comunica con gemini API
    raw_response = generate_response(prompt)
    
    # Validacion y manejo de errores para asegurar que el backend siempre devuelve un JSON con la estructura correcta, incluso si Gemini falla o devuelve algo inesperado.
    if isinstance(raw_response, dict):
        if "error" in raw_response:
            gemini_data = {
                "global_assessment": "Error en el servidor de IA",
                "fact_check_analysis": {
                    "engine": "Gemini API", "verdict": "Error", "reasoning": raw_response["error"], "references": []
                }
            }
        else:
            # generate_response returned a dict directly — use it as-is
            gemini_data = raw_response
    elif isinstance(raw_response, str):
        try:
            gemini_data = json.loads(raw_response)
        except json.JSONDecodeError:
            gemini_data = {
                "global_assessment": "Error de formato",
                "fact_check_analysis": {
                    "engine": "Gemini API", "verdict": "Error", "reasoning": "La IA no devolvió un JSON válido.", "references": []
                }
            }
    else:
        # None or unexpected type
        gemini_data = {
            "global_assessment": "Error en el servidor de IA",
            "fact_check_analysis": {
                "engine": "Gemini API", "verdict": "Error", "reasoning": f"Tipo de respuesta inesperado: {type(raw_response)}", "references": []
            }
        }

    # Fusion de los resultados de BETO y gemini en una respuesta final.
    final_response = {
        "status": "success",
        "global_assessment": gemini_data.get("global_assessment", "Desconocido"),
        "analysis": {
            "style_analysis": beto_data,
            "fact_check_analysis": gemini_data.get("fact_check_analysis", {})
        }
    }
    
    return final_response

# Health check endpoint para monitoreo y logs de acceso.
@app.get("/gemini-status")
async def gemini_status(request: Request, response: Response):
    """Gemini API endpoint for monitoring."""

    timestamp = datetime.now().strftime("%H:%M:%S")
    client_ip = request.client.host

    api_key = os.getenv("GEMINI_API_KEY")
    gemini_status = "Up" if api_key else "Down"
    
    logger.info(f"[{timestamp}] | IP: {client_ip} | Gemini: {gemini_status} | Status: {'OK' if api_key else 'Error'}")
    
    if not api_key:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "Error", "message": "GEMINI_API_KEY is not set. Gemini API is down."}
    
    return {"status": "OK", "message": "API is operational"}
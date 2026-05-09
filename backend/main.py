# uvicorn main:app --reload          →  desarrollo (auto-reload)
# uvicorn main:app --host 0.0.0.0 --port 8000  →  producción / Docker

import logging
import os
import json
from datetime import datetime
from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware

from models import AnalyzeRequest, AnalyzeResponse
from services.ai_service import generate_response
from services.fake_radar_service import analyze_style   # Motor V5 (RoBERTa)
# beto_service.py se conserva en services/ como referencia histórica [DEPRECATED]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# =============================================================================
# INSTANCIA FASTAPI
# =============================================================================
app = FastAPI(
    title="Fake Radar API",
    description="API para detección de desinformación. Motor Stateless.",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    return {"message": "Fake Radar API v2.0 en línea. Motor: FakeRadar V5 + Gemini."}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_news(request: AnalyzeRequest):
    
    """
    Endpoint principal de análisis.
    Combina dos motores:
      1. FakeRadar V5 (RoBERTa) — análisis de estilo y probabilidad de falsedad
      2. Gemini API + Web Search — verificación de hechos con fuentes reales
    """

    # ------------------------------------------------------------------
    # MOTOR 1: FakeRadar V5 — análisis local (rápido, sin API externa)
    # ------------------------------------------------------------------
    model_data = analyze_style(request.text)

    # ------------------------------------------------------------------
    # MOTOR 2: Gemini — fact-checking con búsqueda web
    # Incluimos el score del modelo en el prompt para que Gemini tenga
    # contexto adicional al momento de razonar sobre la noticia.
    # ------------------------------------------------------------------
    fake_score_context = ""
    if model_data.get("fake_probability_score") is not None:
        fake_score_context = (
            f"\nNOTA DE CONTEXTO (no menciones esto en tu respuesta): "
            f"Un modelo de ML especializado en fake news analizó el estilo de esta noticia "
            f"y le asignó un {model_data['fake_probability_score']}% de probabilidad de haber sido manipulada lingüísticamente. "
            f"Usa este dato como señal adicional, no como conclusión definitiva."
        )

    source_url_context = ""
    if request.source_url:
        source_url_context = (
            "\nURL DE LA FUENTE (para contexto, no citar como referencia): "
            f"{request.source_url.strip()}"
        )

    prompt = f"""
        Eres un sistema experto en detección de desinformación y fact-checking periodístico.
        Tu tono es objetivo, frío y analítico. No emitas opiniones personales.

        Analiza la siguiente noticia utilizando los resultados de búsqueda web que tienes disponibles:

        {request.text}
        {source_url_context}
        {fake_score_context}

        INSTRUCCIONES OBLIGATORIAS:
        - Usa los resultados de la búsqueda web para contrastar y verificar la noticia.
        - Devuelve la respuesta en formato JSON sin ningún marcador Markdown como ```json.
        - NO incluyas texto antes ni después del JSON.
        - El campo "references" debe ser siempre una lista vacía []. Las referencias reales se inyectan automáticamente desde el grounding metadata.
        - No cites ni incluyas como referencia la URL de la fuente proporcionada por el usuario.

        REGLAS DE VALORES:
        - global_assessment: "Verdadero" | "Dudoso" | "Falso"
        - verdict: "Verificado" | "Falso" | "Engañoso" | "Requiere verificación" | "No verificable"
        - reasoning: 2-3 líneas explicando la decisión basada en lo encontrado en la web.
        - references: [] (siempre vacío)

        FORMATO OBLIGATORIO (responde SOLO esto):
        {{
        "global_assessment": "Falso",
        "fact_check_analysis": {{
            "engine": "Gemini API + Web Search",
            "verdict": "Falso",
            "reasoning": "Explicación basada en búsqueda web aquí",
            "references": []
        }}
        }}
    """

    raw_response = generate_response(prompt, source_url=request.source_url)

    # ------------------------------------------------------------------
    # PARSEO DE RESPUESTA GEMINI
    # ------------------------------------------------------------------
    if isinstance(raw_response, dict):
        gemini_data = raw_response if "error" not in raw_response else {
            "global_assessment": "Error en el servidor de IA",
            "fact_check_analysis": {
                "engine":    "Gemini API",
                "verdict":   "Error",
                "reasoning": raw_response["error"],
                "source_url": request.source_url,
                "references": [],
            },
        }
    elif isinstance(raw_response, str):
        try:
            gemini_data = json.loads(raw_response)
        except json.JSONDecodeError:
            gemini_data = {
                "global_assessment": "Error de formato",
                "fact_check_analysis": {
                    "engine":    "Gemini API",
                    "verdict":   "Error",
                    "reasoning": "La IA no devolvió un JSON válido.",
                    "source_url": request.source_url,
                    "references": [],
                },
            }
    else:
        gemini_data = {
            "global_assessment": "Error en el servidor de IA",
            "fact_check_analysis": {
                "engine":    "Gemini API",
                "verdict":   "Error",
                "reasoning": f"Tipo de respuesta inesperado: {type(raw_response)}",
                "source_url": request.source_url,
                "references": [],
            },
        }

    # ------------------------------------------------------------------
    # VEREDICTO GLOBAL COMBINADO
    # Si Gemini devuelve error → el veredicto del modelo local es el fallback.
    # Si ambos coinciden → mayor confianza.
    # Gemini tiene prioridad cuando funciona (tiene acceso a fuentes reales).
    # ------------------------------------------------------------------
    gemini_assessment = gemini_data.get("global_assessment", "Desconocido")
    model_verdict     = model_data.get("verdict", "Desconocido")

    if "Error" in gemini_assessment:
        global_assessment = model_verdict
    else:
        global_assessment = gemini_assessment

    if "fact_check_analysis" not in gemini_data or not isinstance(gemini_data["fact_check_analysis"], dict):
        gemini_data["fact_check_analysis"] = {}
    gemini_data["fact_check_analysis"]["source_url"] = request.source_url

    # ------------------------------------------------------------------
    # RESPUESTA FINAL — fusión de ambos motores
    # ------------------------------------------------------------------
    final_response = {
        "status":            "success",
        "global_assessment": global_assessment,
        "analysis": {
            "style_analysis":      model_data,
            "fact_check_analysis": gemini_data.get("fact_check_analysis", {}),
        },
    }

    return final_response


@app.get("/health")
async def health_check():
    """Estado general de la API (para Docker healthcheck y monitoreo)."""
    return {
        "status":    "OK",
        "version":   "2.0.0",
        "model":     "FakeRadar V5 (RoBERTa)",
        "timestamp": datetime.now().isoformat(),
    }


@app.get("/gemini-status")
async def gemini_status(request: Request, response: Response):
    """Estado de la conexión con Gemini API."""
    timestamp  = datetime.now().strftime("%H:%M:%S")
    client_ip  = request.client.host
    api_key    = os.getenv("GEMINI_API_KEY")
    up         = bool(api_key)

    logger.info(f"[{timestamp}] IP: {client_ip} | Gemini: {'Up' if up else 'Down'}")

    if not up:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "Error", "message": "GEMINI_API_KEY no configurada."}

    return {"status": "OK", "message": "Gemini API operativa."}
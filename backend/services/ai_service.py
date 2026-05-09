import logging
import re
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_MODEL

logger = logging.getLogger(__name__)

client = genai.Client(api_key=GEMINI_API_KEY)

def _extract_json(text: str) -> str:
    """
    Extrae el primer bloque JSON del texto de Gemini.
    Con google_search activo, Gemini puede devolver el JSON
    envuelto en markdown o precedido de texto explicativo.
    """
    if not text:
        return text

    # 1. Extraer bloque ```json ... ``` o ``` ... ```
    match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # 2. Extraer el primer objeto { ... } que aparezca en el texto
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0).strip()

    # 3. Si no encuentra nada, devolver el texto tal cual
    return text.strip()


def generate_response(prompt, source_url: str | None = None):
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[
                    types.Tool(
                        google_search=types.GoogleSearch()
                    )
                ],
            ),
        )

        raw_text = response.text
        logger.info(f"Respuesta cruda de Gemini (primeros 300 chars): {raw_text[:300]}")

        # Limpiar y extraer el JSON antes de devolver
        parsed = _extract_json(raw_text)

        # Extraer referencias reales desde grounding_metadata
        real_references = []
        normalized_source_url = None
        if source_url:
            normalized_source_url = source_url.strip().rstrip("/")
        try:
            chunks = response.candidates[0].grounding_metadata.grounding_chunks
            for chunk in chunks:
                web = chunk.web
                if web and web.uri:
                    normalized_uri = web.uri.rstrip("/")
                    if normalized_source_url and normalized_uri == normalized_source_url:
                        continue
                    from urllib.parse import urlparse
                    domain = urlparse(web.uri).netloc
                    real_references.append({
                        "title": web.title or domain,
                        "url": web.uri,
                        "domain": domain
                    })
        except Exception as meta_err:
            logger.warning(f"No se pudo extraer grounding_metadata: {meta_err}")

        # Sobrescribir referencias inventadas con las reales
        try:
            import json
            data = json.loads(parsed)
            data["fact_check_analysis"]["references"] = real_references[:5]
            return json.dumps(data, ensure_ascii=False)
        except Exception:
            return parsed

    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return '{"global_assessment":"Dudoso","fact_check_analysis":{"engine":"Gemini API","verdict":"No verificable","reasoning":"No se pudo generar una respuesta con Gemini.","references":[]}}'
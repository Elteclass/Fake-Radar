from pydantic import BaseModel, Field
from typing import List, Optional

# --- Lo que se recibe del Frontend/Extension ---

class AnalyzeRequest(BaseModel):
    # Noticia completa o fragmento de texto a analizar
    text: str = Field(..., description="El texto de la noticia a analizar")
    # URL de la noticia, para que la IA pueda buscar referencias y contexto (opcional pero recomendado)
    source_url: Optional[str] = Field(None, description="URL opcional de la noticia")


# --- Partes del JSON de salida ---

class ShapFlag(BaseModel):
    # La palabra sospechosa que se detectó en el análisis de estilo
    word: str
    # Qué tanto peso tuvo esa palabra para marcarla como falsa (ej. del 0 al 1)
    impact_score: float

class StyleAnalysis(BaseModel):
    engine: str = "FakeRadar V5 (RoBERTa)"
    # Del 0 al 100, qué tan manipulado se ve el estilo de redacción (None si hubo error)
    fake_probability_score: Optional[float] = None
    # Veredicto del motor local: "Falso" | "Dudoso" | "Verdadero" | "No disponible"
    verdict: Optional[str] = None
    # Lista de las palabras sospechosas detectadas
    shap_flags: List[ShapFlag] = []
    # Mensaje de error (solo presente si el motor falló)
    error: Optional[str] = None

class Reference(BaseModel):
    # Titulo de la nota real
    title: str
    # El link directo para que el usuario vaya a leer la verdad
    url: str
    # El dominio principal (ej. animalpolitico.com)
    domain: str

class FactCheckAnalysis(BaseModel):
    engine: str = "Gemini API + Web Search"
    # URL proporcionada por el usuario (si existe)
    source_url: Optional[str] = None
    # El veredicto rápido: Falso, Verdadero, Desinformación
    verdict: str
    # El resumen de 2 líneas de por qué la IA tomó esa decisión
    reasoning: str
    # Los links oficiales que desmienten o confirman la nota
    references: List[Reference]

class AnalysisResult(BaseModel):
    # Juntamos el análisis de la forma (BETO) y el del fondo (Gemini)
    style_analysis: StyleAnalysis
    fact_check_analysis: FactCheckAnalysis

class AnalyzeResponse(BaseModel):
    # Para que el frontend sepa rápido que la petición no falló (ej. "success")
    status: str
    # El color del semáforo general para la extensión (Falso, Verdadero, Dudoso)
    global_assessment: str
    # Todo el desglose de los análisis que armamos arriba
    analysis: AnalysisResult
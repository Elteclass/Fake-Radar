<div align="center">

![Fake Radar](assets/FakeRadarImage.png)

# Fake Radar

![Versión](https://img.shields.io/badge/Versi%C3%B3n-2.0.0-blue)
![Build Status](https://img.shields.io/badge/Build-passing-brightgreen)

_Un sistema de Inteligencia Artificial para la detección de desinformación (Fake News) en Baja California, México._

</div>

## Tabla de Contenidos

- [Acerca del Proyecto](#acerca-del-proyecto)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Créditos y Colaboradores](#créditos-y-colaboradores)
- [Licencia](#licencia)

## Acerca del Proyecto

### ¿Qué es?

Fake Radar es una plataforma integral diseñada para identificar, analizar y combatir la desinformación y las noticias falsas que circulan en medios digitales, con un enfoque particular en la región de Baja California, México.

### ¿Por qué?

La desinformación representa un riesgo creciente para la sociedad, polarizando comunidades y afectando la toma de decisiones informada. Este proyecto nace de la necesidad de proveer a los ciudadanos y periodistas de una herramienta confiable y rápida para verificar la veracidad de los contenidos que consumen diariamente.

### ¿Cómo funciona?

El sistema utiliza modelos de Procesamiento de Lenguaje Natural (NLP) avanzados para analizar la estructura, semántica y estilo de redacción de una noticia. A través de nuestra extensión de navegador o panel web, los usuarios pueden enviar textos que son procesados en tiempo real por nuestro motor de inferencias, el cual clasifica el grado de fiabilidad de la información.

## Tecnologías Utilizadas

Este proyecto está construido con un stack moderno y escalable:

- ![React](https://img.shields.io/badge/React-20232A?style=flat-square&logo=react&logoColor=61DAFB)
- ![Vite](https://img.shields.io/badge/Vite-B73BFE?style=flat-square&logo=vite&logoColor=FFD62E)
- ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
- ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
- ![Google Cloud Storage](https://img.shields.io/badge/Google_Cloud_Storage-4285F4?style=flat-square&logo=google-cloud&logoColor=white)
- ![Google Colab](https://img.shields.io/badge/Google_Colab-F9AB00?style=flat-square&logo=googlecolab&logoColor=white)

## Estructura del Proyecto

El repositorio está organizado en los siguientes módulos principales:

```text
fake-radar/
├── frontend/    # Interfaz de usuario (React + Vite)
├── backend/     # API y Motor de inferencias (FastAPI)
├── extension/   # Extensión para navegador web
└── ai-model/    # Modelos base y scripts de entrenamiento (Baseline)
```

## Créditos y Colaboradores

Este proyecto ha sido posible gracias al esfuerzo y dedicación del equipo de desarrollo. Agradecemos profundamente a cada uno de los colaboradores por su invaluable contribución en la investigación, desarrollo e implementación del modelo fundacional y la plataforma.

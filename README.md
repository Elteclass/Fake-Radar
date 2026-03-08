# 📡 Fake Radar
**Sistema Inteligente de Detección de Desinformación mediante NLP**

Este repositorio contiene el código fuente del proyecto "Fake Radar", desarrollado para la materia de Inteligencia Artificial (Enero - Junio 2026). El sistema estima la probabilidad de que una noticia sea desinformación utilizando modelos de lenguaje (BETO) y una arquitectura sin estado (stateless).

## 📂 Estructura del Monorepo

El proyecto está dividido en módulos independientes. Cada integrante debe trabajar únicamente en la carpeta asignada a su rol:

* 🤖 `/ai-model`: Scripts de experimentación, notebooks (Google Colab) y fine-tuning del modelo BETO.
* ⚙️ `/backend`: API REST desarrollada en Python (FastAPI). Orquesta la lógica y el servicio de NLP.
* 🌐 `/frontend`: Interfaz web interactiva desarrollada con React y Vite.
* 🔌 `/extension`: Extensión para Google Chrome (Manifest V3) para análisis de noticias en tiempo real.
* 📚 `/docs`: Documentación técnica, diagramas de arquitectura, etc.

## 👥 Equipo de Desarrollo y Roles

* **Aaron Casildo:** Product Owner / Desarrollo Backend
* **Jaime Alvarez:** Scrum Master / Líder Técnico / DevOps
* **Brisa Aguayo:** Ingeniera IA / NLP
* **Erik Aboytes:** Desarrollo Backend
* **José Bautista:** Desarrollo Frontend Web
* **Roberto Bernal:** Desarrollo Frontend / Extensión
* **Jocelyn Álvarez:** UI/UX / Desarrollo Frontend
* **Iker Alonso:** Ingeniero de Pruebas (QA)

## 🚀 Flujo de Trabajo (Git Flow)

1. **Nunca** hacer commits directos a la rama `main`.
2. Todo desarrollo nuevo debe hacerse en una rama derivada (ej. `feature/nombre-de-la-tarea`).
3. Al terminar la tarea, abrir un Pull Request (PR) para revisión del Líder Técnico antes de integrar.

# Modelos de Inteligencia Artificial (Baseline)

![Google Colab](https://img.shields.io/badge/Google_Colab-F9AB00?style=flat-square&logo=googlecolab&logoColor=white)
![Hugging Face](https://img.shields.io/badge/Hugging_Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black)

Este directorio documenta el trabajo de investigación y el desarrollo de los modelos de Procesamiento de Lenguaje Natural (NLP) utilizados para detectar desinformación. Aquí se conserva la historia y evolución del motor principal de Fake Radar.

## Prueba de Concepto: El Modelo Baseline

En sus inicios, este proyecto requería validar la hipótesis de que un modelo de NLP podía captar los matices de las noticias falsas regionales.

Para esta fase inicial, desarrollamos un **Modelo Baseline** fundamentado en la arquitectura **BETO** (Spanish BERT). Este modelo fundacional fue entrenado y afinado por nuestra compañera **Brisa**, utilizando un dataset inicial de **676 noticias** curadas manualmente.

Este esfuerzo pionero sirvió como una exitosa _Prueba de Concepto (PoC)_, permitiendo al equipo validar la arquitectura técnica del sistema, probar la integración entre el frontend y el backend, y establecer las métricas base para futuras iteraciones. Los notebooks y scripts de este trabajo original se mantienen en este directorio como referencia.

## Evolución a V5

A medida que el proyecto maduró y las exigencias de precisión aumentaron, el sistema evolucionó para soportar un volumen y complejidad de datos mucho mayor.

El modelo final a grado de producción (V5) representó un salto arquitectónico:

- Fue migrado a una arquitectura **XLM-RoBERTa**.
- Se aplicaron técnicas avanzadas de **Transfer Learning**.
- Fue entrenado con un corpus masivo y diverso de **4,900 noticias**.

Esta evolución permitió capturar con mayor eficacia las sutilezas lingüísticas, el sesgo emocional y la estructura semántica característica de las campañas de desinformación modernas.

### Repositorio del Modelo V5

El código fuente, los scripts de entrenamiento y los pipelines de datos del modelo RoBERTa viven en su propio repositorio dedicado para mantener una mejor separación de responsabilidades:

> [👉 **[Enlace al Repositorio del Modelo RoBERTa V5]**](https://github.com/Elteclass/fake-radar-ai-engine.git)

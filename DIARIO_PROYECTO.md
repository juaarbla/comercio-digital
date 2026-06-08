# Diario del Proyecto

## 2026-06-08

- Problema: la web `juanarmada.com` publicó una noticia del día que no aparecía en el pipeline por desfase del RSS.
- Solución: se añadió fallback de fuente `wordpress_api` en `feeds.json` usando `wp-json/wp/v2/posts`.
- Implementación: `news_aggregator.py` ahora soporta `source: "wordpress_api"`, normaliza posts WP, mapea categorías y evalúa recencia con fechas ISO.
- Estabilidad: se dejó `generar_web.py` con una sola implementación activa (sin duplicados heredados).
- Validación: ejecución completa OK (`news_aggregator.py` -> `clasificador_ra.py` -> `generar_web.py`) y publicación confirmada en portada y sección IA.

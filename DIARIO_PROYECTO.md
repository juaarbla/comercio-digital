# Diario del Proyecto

## 2026-06-08

- Problema: la web `juanarmada.com` publicó una noticia del día que no aparecía en el pipeline por desfase del RSS.
- Solución: se añadió fallback de fuente `wordpress_api` en `feeds.json` usando `wp-json/wp/v2/posts`.
- Implementación: `news_aggregator.py` ahora soporta `source: "wordpress_api"`, normaliza posts WP, mapea categorías y evalúa recencia con fechas ISO.
- Estabilidad: se dejó `generar_web.py` con una sola implementación activa (sin duplicados heredados).
- Validación: ejecución completa OK (`news_aggregator.py` -> `clasificador_ra.py` -> `generar_web.py`) y publicación confirmada en portada y sección IA.

## Checklist diaria

1. Activar entorno virtual (`venv`).
2. Ejecutar agregación: `python news_aggregator.py`.
3. Revisar salida: confirmar noticias nuevas detectadas y sin errores de fuente.
4. Ejecutar clasificación: `python clasificador_ra.py`.
5. Ejecutar generación web: `python generar_web.py`.
6. Verificar en `docs/index.html` que aparezcan titulares del día.
7. Verificar al menos una sección temática (por ejemplo, IA) en `docs/ia-marketing.html`.
8. Si hubo cambios funcionales, registrar entrada nueva en este diario.

## Plantilla de nueva entrada

```md
## AAAA-MM-DD

- Problema/objetivo:
- Causa (si aplica):
- Cambios realizados:
- Validación ejecutada:
- Resultado final:
- Pendientes:
```

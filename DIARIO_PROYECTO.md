# Diario del Proyecto

## 2026-06-09

- Problema/objetivo: simplificar la ejecución diaria del agregador y evitar tener que lanzar varios scripts manualmente.
- Causa: el flujo dependía de ejecutar por separado `news_aggregator.py`, `clasificador_ra.py`, `imagen_destacada.py` y `generar_web.py`.
- Cambios realizados: se ha creado `run_pipeline.py`, que ejecuta todo el pipeline en orden.
- Validación ejecutada: ejecución local con `python run_pipeline.py`.
- Resultado final: la web local se ha actualizado correctamente.
- Pendientes: subir cambios a GitHub y comprobar la publicación en `https://comerciodigital.net`.

## 2026-06-08

- Problema: la web `juanarmada.com` publicó una noticia del día que no aparecía en el pipeline por desfase del RSS.
- Solución: se añadió fallback de fuente `wordpress_api` en `feeds.json` usando `wp-json/wp/v2/posts`.
- Implementación: `news_aggregator.py` ahora soporta `source: "wordpress_api"`, normaliza posts WP, mapea categorías y evalúa recencia con fechas ISO.
- Estabilidad: se dejó `generar_web.py` con una sola implementación activa (sin duplicados heredados).
- Validación: ejecución completa OK (`news_aggregator.py` -> `clasificador_ra.py` -> `generar_web.py`) y publicación confirmada en portada y sección IA.

## Checklist diaria

1. Activar entorno virtual (`venv`).
2. Ejecutar el pipeline completo: `python run_pipeline.py`.
3. Revisar salida en consola y confirmar que no hay errores.
4. Verificar en `docs/index.html` que aparezcan titulares actualizados.
5. Verificar al menos una sección temática, por ejemplo `docs/ia-marketing.html`.
6. Subir cambios a GitHub.
7. Comprobar la publicación en `https://comerciodigital.net`.
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

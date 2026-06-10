# Diario del Proyecto

## 2026-06-09

- Problema/objetivo: añadir una capa docente a las noticias para que el agregador no sea solo informativo, sino también útil para el aula.
- Causa: las noticias estaban clasificadas por módulo y RA, pero no incluían una propuesta directa de uso didáctico.
- Cambios realizados: se ha creado `enriquecer_docente.py`, que añade `pregunta_aula`, `conceptos_clave` y `actividad_breve` a cada noticia. Se ha actualizado `generar_web.py` para mostrar el bloque “Uso en el aula” como acordeón desplegable en las páginas de sección. Se ha actualizado `docs/assets/style.css`.
- Validación ejecutada: prueba del enriquecimiento docente sobre noticias clasificadas y generación local con `python generar_web.py`.
- Resultado final: las páginas de sección muestran el bloque “Uso en el aula” desplegable, mientras que la portada se mantiene limpia sin cajas docentes.
- Pendientes: integrar `enriquecer_docente.py` en `run_pipeline.py`, ejecutar el pipeline completo y subir cambios a GitHub.

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
6. Abrir una noticia de sección y comprobar, si procede, el acordeón “Uso en el aula”.
7. Subir cambios a GitHub.
8. Comprobar la publicación en `https://comerciodigital.net`.
9. Si hubo cambios funcionales, registrar entrada nueva en este diario.

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

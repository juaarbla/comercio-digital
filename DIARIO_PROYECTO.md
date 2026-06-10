# Diario del Proyecto

## 2026-06-09

- Problema/objetivo: separar la autoría del contenido propio de la clasificación docente por módulo y RA.
- Causa: algunos artículos propios de `juanarmada.com`, aunque estaban correctamente clasificados por módulo y RA, no aparecían en la sección “Del Autor” porque la sección web se calculaba a partir del módulo asignado.
- Cambios realizados: se ha actualizado `generar_web.py` para que cualquier noticia o artículo cuya URL contenga `juanarmada.com` se muestre editorialmente en la sección “Del Autor”.
- Validación prevista: ejecutar `python generar_web.py` y comprobar que los contenidos propios aparecen en `docs/del-autor.html` o en el bloque “Del Autor” de la portada, manteniendo sus datos docentes de módulo, RA y “Uso en el aula”.
- Resultado final:
- Pendientes: probar la generación local y subir cambios a GitHub si el resultado es correcto.

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

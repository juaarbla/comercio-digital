# Diario del Proyecto

## 2026-06-10

- Problema/objetivo: ajustar la presencia de los contenidos propios en la web sin sobrecargar la portada.
- Causa: al clasificar los artículos de `juanarmada.com` como “Del Autor”, el bloque generado en portada ocupaba demasiado espacio para un único contenido y rompía el equilibrio visual de la página.
- Cambios realizados:
  - Se mantiene la detección de contenidos propios mediante el dominio `juanarmada.com`.
  - Los artículos propios siguen apareciendo en la sección `Del Autor`.
  - Se mantiene la página `docs/del-autor.html`.
  - Se mantiene la clasificación docente por módulo y RA.
  - Se mantiene el acordeón “Uso en el aula”.
  - Se ha eliminado el bloque “Del Autor” de la portada.
- Validación ejecutada: generación local con `python generar_web.py` y revisión visual de `docs/index.html` y `docs/del-autor.html`.
- Resultado final: la portada queda más limpia y equilibrada, mientras que los contenidos propios siguen accesibles desde el menú y desde su página específica.
- Pendientes: ejecutar `python run_pipeline.py`, revisar la web publicada y subir los cambios a GitHub.

## 2026-06-09 — Capa docente

- Problema/objetivo: añadir una capa docente a las noticias para que el agregador no sea solo informativo, sino también útil para el aula.
- Causa: las noticias estaban clasificadas por módulo y RA, pero no incluían una propuesta directa de uso didáctico.
- Cambios realizados:
  - Se ha creado `enriquecer_docente.py`.
  - Cada noticia puede incorporar `pregunta_aula`, `conceptos_clave` y `actividad_breve`.
  - Se ha actualizado `generar_web.py` para mostrar el bloque “Uso en el aula”.
  - El bloque docente se muestra como acordeón desplegable mediante HTML nativo `<details>` y `<summary>`.
  - Se ha actualizado `docs/assets/style.css`.
  - La portada no muestra cajas docentes.
- Validación ejecutada:
  - Prueba del enriquecimiento sobre `noticias_clasificadas.json`.
  - Gestión correcta de un error puntual de JSON generado por Ollama mediante fallback docente.
  - Generación local con `python generar_web.py`.
  - Ejecución completa con `python run_pipeline.py`.
- Resultado final: las páginas de sección muestran recursos docentes desplegables y la portada se mantiene limpia.
- Pendientes: revisar periódicamente la calidad de preguntas, conceptos y actividades generadas.

## 2026-06-09 — Pipeline unificado

- Problema/objetivo: simplificar la ejecución diaria del agregador y evitar tener que lanzar varios scripts manualmente.
- Causa: el flujo dependía de ejecutar por separado `news_aggregator.py`, `clasificador_ra.py`, `imagen_destacada.py` y `generar_web.py`.
- Cambios realizados:
  - Se ha creado `run_pipeline.py`.
  - Se ha integrado `enriquecer_docente.py` en el flujo.
- Flujo actual:

```text
news_aggregator.py
   ↓
clasificador_ra.py
   ↓
enriquecer_docente.py
   ↓
imagen_destacada.py
   ↓
generar_web.py
```

- Validación ejecutada: ejecución local con `python run_pipeline.py`.
- Resultado final: pipeline completado correctamente y web local actualizada.
- Pendientes: mantener actualizado `env.example` cuando se añadan nuevas variables de configuración.

## 2026-06-08

- Problema: la web `juanarmada.com` publicó una noticia del día que no aparecía en el pipeline por desfase del RSS.
- Solución: se añadió fallback de fuente `wordpress_api` en `feeds.json` usando `wp-json/wp/v2/posts`.
- Implementación: `news_aggregator.py` ahora soporta `source: "wordpress_api"`, normaliza posts de WordPress, mapea categorías y evalúa recencia con fechas ISO.
- Estabilidad: se dejó `generar_web.py` con una sola implementación activa, sin duplicados heredados.
- Validación: ejecución completa correcta y publicación confirmada en portada y sección IA.

## Checklist diaria

1. Activar el entorno virtual (`venv`).
2. Ejecutar el pipeline completo:

```bash
python run_pipeline.py
```

3. Revisar la salida en consola y confirmar que no hay errores.
4. Verificar `docs/index.html`.
5. Verificar al menos una sección temática, por ejemplo `docs/ia-marketing.html`.
6. Comprobar una noticia con el acordeón “Uso en el aula”.
7. Verificar que `docs/del-autor.html` se genera cuando existen contenidos propios.
8. Confirmar que la portada no muestra el bloque “Del Autor”.
9. Subir los cambios a GitHub.
10. Comprobar la publicación en `https://comerciodigital.net`.
11. Si hubo cambios funcionales, registrar una nueva entrada en este diario.

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

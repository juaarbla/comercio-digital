# Comercio Digital — Agregador de noticias para FP

Proyecto en Python para recopilar noticias de actualidad, resumirlas con IA, clasificarlas por módulos/RA de Formación Profesional y generar una web estática publicable en GitHub Pages.

Web pública:

```text
https://comerciodigital.net
```

## Objetivo del proyecto

El proyecto no busca crear solo un agregador automático de noticias, sino una herramienta de actualidad para FP de Comercio y Marketing.

La idea es conectar noticias reales con:

- módulos profesionales,
- resultados de aprendizaje,
- tendencias del sector,
- posibles usos en el aula.

## Flujo general

```text
feeds.json
   ↓
news_aggregator.py
   ↓
noticias_resumidas.json
   ↓
clasificador_ra.py
   ↓
noticias_clasificadas.json
   ↓
imagen_destacada.py
   ↓
generar_web.py
   ↓
docs/
   ↓
GitHub Pages
```

## Ejecución recomendada

Desde la carpeta raíz del proyecto:

```bash
python run_pipeline.py
```

Este comando ejecuta en orden:

1. `news_aggregator.py`
2. `clasificador_ra.py`
3. `imagen_destacada.py`
4. `generar_web.py`

## Ejecución manual por pasos

También se puede ejecutar el flujo manualmente:

```bash
python news_aggregator.py
python clasificador_ra.py
python imagen_destacada.py
python generar_web.py
```

## Archivos principales

- `feeds.json`: fuentes RSS y WordPress API.
- `news_aggregator.py`: obtiene noticias nuevas y las resume.
- `clasificador_ra.py`: clasifica las noticias por módulo y RA.
- `imagen_destacada.py`: intenta obtener imagen destacada.
- `generar_web.py`: genera la web estática en `docs/`.
- `run_pipeline.py`: ejecuta todo el flujo de generación en un solo comando.
- `historial.json`: guarda noticias ya procesadas.
- `noticias_resumidas.json`: noticias resumidas.
- `noticias_clasificadas.json`: noticias clasificadas.
- `DIARIO_PROYECTO.md`: registro de cambios y validaciones.

## Fuentes

Las fuentes se configuran en `feeds.json`.

Actualmente el proyecto puede trabajar con:

- feeds RSS,
- artículos propios,
- podcast,
- entradas de WordPress mediante API REST,
- fuentes externas de comercio electrónico, marketing digital, digitalización y ciberseguridad.

## Checklist diaria

1. Activar el entorno virtual.
2. Ejecutar:

```bash
python run_pipeline.py
```

3. Revisar que la consola no muestre errores.
4. Revisar `docs/index.html`.
5. Revisar una sección temática, por ejemplo `docs/ia-marketing.html`.
6. Subir cambios a GitHub.
7. Comprobar la publicación en `https://comerciodigital.net`.

## Publicación

La carpeta `docs/` contiene la web estática generada.

GitHub Pages debe estar configurado para publicar desde:

```text
/docs
```

## Próximas mejoras previstas

- Añadir una capa docente por noticia: pregunta para el aula, conceptos clave y actividad breve.
- Separar mejor módulo de origen, módulo asignado y sección visible de la web.
- Generar `sitemap.xml` y `robots.txt`.
- Crear una página `sobre.html` explicando el proyecto.
- Mejorar el filtrado de fuentes técnicas para evitar exceso de ruido.

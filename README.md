# Comercio Digital — Agregador de noticias para FP

Proyecto en Python para recopilar noticias de actualidad, resumirlas con IA, clasificarlas por módulos/RA de Formación Profesional, enriquecerlas con una capa docente y generar una web estática publicable en GitHub Pages.

Web pública:

```text
https://comerciodigital.net
```

## Objetivo del proyecto

El proyecto no busca crear solo un agregador automático de noticias, sino una herramienta de actualidad para FP de Comercio y Marketing.

La idea es conectar noticias reales con módulos profesionales, resultados de aprendizaje, tendencias del sector y posibles usos en el aula.

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
enriquecer_docente.py
   ↓
imagen_destacada.py
   ↓
generar_web.py
   ↓
generar_aula.py
   ↓
generar_seo.py
   ↓
docs/
   ↓
GitHub Pages
```

## Ejecución recomendada

```bash
python run_pipeline.py
```

## Ejecución manual

```bash
python news_aggregator.py
python clasificador_ra.py
python enriquecer_docente.py --forzar
python imagen_destacada.py
python generar_web.py
python generar_aula.py --max-noticias 25
python generar_seo.py
```

## Archivos principales

- `feeds.json`: fuentes RSS y WordPress API.
- `news_aggregator.py`: obtiene noticias nuevas y las resume.
- `clasificador_ra.py`: clasifica las noticias por módulo y RA.
- `enriquecer_docente.py`: añade capa docente, `score_docente`, selección de aula y newsletter.
- `imagen_destacada.py`: intenta obtener imagen destacada.
- `generar_web.py`: genera la web estática principal en `docs/`.
- `generar_aula.py`: genera `docs/aula.html`.
- `generar_seo.py`: añade metadatos SEO y genera `sitemap.xml` y `robots.txt`.
- `run_pipeline.py`: ejecuta el flujo completo.
- `DIARIO_PROYECTO.md`: registro de cambios y validaciones.

## Archivos generados localmente

Normalmente no se suben a GitHub:

- `historial.json`
- `noticias_resumidas.json`
- `noticias_clasificadas.json`
- `noticias_clasificadas.backup_*.json`

La publicación pública se realiza desde:

```text
docs/
```

## Página de aula

`docs/aula.html` muestra noticias seleccionadas por valor docente y utiliza:

```text
docs/assets/style.css
```

## Checklist diaria

1. Activar el entorno virtual.
2. Ejecutar `python run_pipeline.py`.
3. Revisar `docs/index.html`.
4. Revisar `docs/aula.html`.
5. Revisar una sección temática, por ejemplo `docs/ia-marketing.html`.
6. Comprobar `docs/sitemap.xml` y `docs/robots.txt`.
7. Subir cambios a GitHub.
8. Comprobar `https://comerciodigital.net`.
9. Comprobar `https://comerciodigital.net/aula.html`.

## Próximas mejoras previstas

- Generar fichas Markdown a partir de noticias con mayor `score_docente`.
- Crear newsletter docente desde `seleccion_newsletter = true`.
- Crear una página `sobre.html`.
- Mejorar el filtrado de fuentes técnicas.
- Añadir introducciones SEO permanentes en páginas de sección.

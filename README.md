# Comercio Digital — Agregador de noticias para FP

Proyecto en Python para recopilar noticias de actualidad, resumirlas con IA, clasificarlas por módulos y resultados de aprendizaje de Formación Profesional, enriquecerlas con una capa docente y generar una web estática publicable en GitHub Pages.

Web pública:

```text
https://comerciodigital.net
```

## Objetivo

El objetivo no es crear únicamente un agregador automático de noticias, sino una herramienta docente para FP de Comercio y Marketing.

La idea es conectar noticias reales con:

- módulos profesionales;
- resultados de aprendizaje;
- tendencias del sector;
- actividades de aula;
- fichas docentes reutilizables;
- materiales Markdown para Aules/Moodle.

## Estructura general del flujo

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
generar_fichas_aula.py
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

```powershell
python run_pipeline.py
```

También puede ejecutarse desde el panel:

```powershell
.\arrancar.bat
```

Opción habitual para actualizar la web pública:

```text
2. Proceso completo + publicar SOLO web docs/
```

## Ejecución manual

```powershell
python news_aggregator.py
python clasificador_ra.py
python enriquecer_docente.py --forzar
python imagen_destacada.py
python generar_web.py
python generar_fichas_aula.py --max-fichas 10 --limpiar
python generar_aula.py --max-noticias 25
python generar_seo.py
```

## Archivos principales

| Archivo | Función |
|---|---|
| `feeds.json` | Fuentes RSS y WordPress API. |
| `news_aggregator.py` | Obtiene noticias nuevas y las resume. |
| `clasificador_ra.py` | Clasifica noticias por módulo y RA. |
| `enriquecer_docente.py` | Añade capa docente, score, selección de aula y newsletter. |
| `imagen_destacada.py` | Obtiene imagen destacada desde RSS/OG o OpenAI. |
| `generar_web.py` | Genera portada y páginas de secciones en `docs/`. |
| `generar_fichas_aula.py` | Genera fichas docentes HTML/Markdown y material conjunto. |
| `generar_aula.py` | Genera `docs/aula.html`. |
| `generar_seo.py` | Añade metadatos SEO, `sitemap.xml` y `robots.txt`. |
| `run_pipeline.py` | Ejecuta el flujo completo. |
| `arrancar.bat` | Panel de control en Windows. |
| `DIARIO_PROYECTO.md` | Registro de cambios, incidencias y decisiones. |

## Salida pública

La web publicada se genera en:

```text
docs/
```

Páginas principales:

```text
docs/index.html
docs/comercio-electronico.html
docs/internacional.html
docs/digitalizacion.html
docs/ia-marketing.html
docs/marketing.html
docs/aula.html
docs/del-autor.html
docs/fichas-aula/
docs/sitemap.xml
docs/robots.txt
```

## Página Aula

`docs/aula.html` muestra una selección de noticias con valor docente.

Cada noticia puede mostrar:

- módulo;
- RA;
- tipo de uso;
- pregunta detonadora;
- actividad breve;
- conceptos clave;
- justificación curricular;
- enlace a la noticia original;
- enlace a ficha docente HTML;
- enlace a ficha Markdown.

Los campos internos como `score_docente`, `valor_docente` y `seleccion_newsletter` se usan para ordenar y seleccionar, pero no deben mostrarse en la web pública.

## Fichas docentes

`generar_fichas_aula.py` genera:

```text
docs/fichas-aula/001-titulo-noticia.html
docs/fichas-aula/001-titulo-noticia.md
docs/fichas-aula/material-aula.md
docs/fichas-aula/index_fichas.json
```

Criterio para generar ficha:

```text
generar_ficha = true
```

o bien:

```text
valor_docente = alto
score_docente >= 25
tiene pregunta_aula
tiene actividad_breve
tiene ra_asignado
```

Por defecto se limita a 10 fichas por ejecución.

## Imágenes destacadas

`imagen_destacada.py` intenta completar `imagen_url` en `noticias_clasificadas.json`.

Modos disponibles mediante `.env`:

```env
IMAGE_PROVIDER=rss
IMAGE_PROVIDER=openai
OPENAI_API_KEY=...
OPENAI_IMG_SIZE=1024x1024
OPENAI_IMG_MODEL=dall-e-3
```

Con `rss`, intenta obtener `og:image` o `twitter:image` de la página original.

Usa caché local:

```text
cache_imagenes.json
```

## Archivos generados localmente

Normalmente no se suben a GitHub:

```text
historial.json
noticias_resumidas.json
noticias_clasificadas.json
noticias_clasificadas.backup_*.json
cache_imagenes.json
deprecated/
_deprecated/
```

Sí se suben normalmente:

```text
*.py
*.md
arrancar.bat
docs/
```

## Comandos útiles

### Ejecutar pipeline completo

```powershell
python run_pipeline.py
```

### Generar solo web principal

```powershell
python generar_web.py
```

### Generar fichas docentes

```powershell
python generar_fichas_aula.py --max-fichas 10 --limpiar
```

### Generar página Aula

```powershell
python generar_aula.py --max-noticias 25
```

### Ejecutar SEO técnico

```powershell
python generar_seo.py
```

### Comprobar enlaces de Aula

```powershell
Select-String -Path docs\index.html -Pattern "aula.html"
Select-String -Path docs\aula.html -Pattern "Descargar Markdown"
Select-String -Path docs\aula.html -Pattern "Descargar material de aula MD"
```

### Comprobar Del Autor

```powershell
Select-String -Path docs\*.html -Pattern "autor.html"
Select-String -Path docs\*.html -Pattern "del-autor.html"
```

`autor.html` no debería aparecer. La ruta correcta es `del-autor.html`.

## Checklist diaria

1. Ejecutar `python run_pipeline.py`.
2. Revisar `docs/index.html`.
3. Revisar que la portada no se rompe en bloques de 3 noticias.
4. Revisar `docs/aula.html`.
5. Comprobar una ficha docente.
6. Comprobar `docs/fichas-aula/material-aula.md`.
7. Comprobar `docs/sitemap.xml` y `docs/robots.txt`.
8. Publicar en GitHub.
9. Revisar `https://comerciodigital.net`.
10. Revisar `https://comerciodigital.net/aula.html`.

## Documentación complementaria

- `README_AULA.md`: funcionamiento de Aula y fichas docentes.
- `README_IMAGENES.md`: funcionamiento de imágenes destacadas.
- `README_PASO1_DOCENTE.md`: capa docente, score y criterios de selección.
- `README_INSTALACION.md`: instalación rápida y publicación.
- `DIARIO_PROYECTO.md`: histórico del proyecto.

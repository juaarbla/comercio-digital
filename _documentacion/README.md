# Comercio Digital — Agregador de noticias para FP

Proyecto en Python para recopilar noticias de actualidad, resumirlas con IA, clasificarlas por módulos y resultados de aprendizaje de Formación Profesional, enriquecerlas con una capa docente, generar una web estática publicable en GitHub Pages y consultar/reutilizar el contenido mediante MCP.

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
- materiales Markdown para Aules/Moodle;
- newsletter docente en HTML/Markdown para distribución externa;
- herramientas MCP para consultar y reutilizar el contenido desde IA.

## Estructura general del flujo

```text
feeds.json
   ↓
news_aggregator.py
   ↓
data/processed/noticias_resumidas.json
   ↓
clasificador_ra.py
   ↓
data/processed/noticias_clasificadas.json
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
generar_newsletter.py
   ↓
generar_seo.py
   ↓
docs/
   ↓
GitHub Pages
```

## Estructura actual de datos

```text
data/
├─ processed/
│  ├─ noticias_resumidas.json
│  └─ noticias_clasificadas.json
│
├─ cache/
│  ├─ cache_clasificacion.json
│  └─ cache_imagenes.json
│
└─ backups/
   └─ noticias_clasificadas.backup_*.json
```

## Ejecución recomendada

```powershell
python run_pipeline.py
```

También puede ejecutarse desde el panel:

```powershell
.\arrancar.bat
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
python generar_newsletter.py --periodicidad quincenal --force
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
| `generar_newsletter.py` | Genera newsletter docente en HTML/Markdown en `docs/newsletter/`. |
| `generar_brief_newsletter.py` | Genera un brief Markdown para podcast a partir de la selección de newsletter. |
| `generar_seo.py` | Añade metadatos SEO, `sitemap.xml` y `robots.txt`. |
| `run_pipeline.py` | Ejecuta el flujo completo. |
| `arrancar.bat` | Panel de control en Windows. |
| `generar_brief_podcast.bat` | Lanza la generación del brief de podcast con log local. |
| `paths.py` | Centraliza rutas del proyecto. |
| `mcp_servers/comercio_digital/server.py` | Servidor MCP local del agregador. |
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
docs/aula.html
docs/newsletter/index.html
docs/newsletter/newsletter-AAAA-WSS.html
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

## Fichas docentes públicas

`generar_fichas_aula.py` genera:

```text
docs/fichas-aula/001-titulo-noticia.html
docs/fichas-aula/001-titulo-noticia.md
docs/fichas-aula/material-aula.md
docs/fichas-aula/index_fichas.json
```

Estas fichas forman parte de la web pública generada en `docs/`.

## Newsletter docente

`generar_newsletter.py` crea una selección periódica de noticias para compartir como boletín docente.

Genera:

```text
docs/newsletter/newsletter-AAAA-WSS.html
docs/newsletter/newsletter-AAAA-WSS.md
docs/newsletter/index.html
```

Uso recomendado:

```powershell
python generar_newsletter.py --periodicidad quincenal --force
```

o, si se quiere una edición semanal:

```powershell
python generar_newsletter.py --periodicidad semanal --force
```

La newsletter no se genera cada día de forma automática. Se crea únicamente cuando se ejecuta el script.

Como salida complementaria, puede generarse un brief Markdown para podcast:

```powershell
python generar_brief_newsletter.py --periodicidad quincenal
```

Tambien puede lanzarse con:

```powershell
generar_brief_podcast.bat
```

El brief se guarda en:

```text
outputs/podcast/
```

Este archivo sirve como base revisable para `comercIAaliza.online`. El agregador no genera audio ni publica el podcast.

El agregador no gestiona suscriptores ni realiza envíos de correo. La distribución debe hacerse mediante una herramienta externa o envío manual del enlace público:

```text
https://comerciodigital.net/newsletter/
```

Procedimiento recomendado para distribuir por email:

1. Generar la newsletter.
2. Publicar los cambios en GitHub Pages.
3. Comprobar que la edición se ve correctamente en la web.
4. Enviar un correo breve desde Gmail, Brevo, Mailchimp, Substack, MailerLite u otra herramienta externa.
5. Incluir el enlace a la edición o al índice de newsletters.

## MCP Comercio Digital

El proyecto incluye un servidor MCP local para consultar el agregador desde herramientas compatibles con Model Context Protocol.

Ruta:

```text
mcp_servers/comercio_digital/
```

Archivos principales:

```text
mcp_servers/comercio_digital/server.py
mcp_servers/comercio_digital/requirements.txt
mcp_servers/comercio_digital/README.md
```

El MCP lee:

```text
data/processed/noticias_clasificadas.json
```

Herramientas disponibles:

```text
estado_agregador()
buscar_noticias(texto, limite)
noticias_por_modulo(modulo, limite)
noticias_por_valor_docente(valor, limite)
noticias_newsletter(limite)
ficha_aula_basica(url_o_titulo)
generar_ficha_md(url_o_titulo)
```

La herramienta `generar_ficha_md` guarda fichas Markdown de trabajo en:

```text
outputs/aula/
```

Diferencia importante:

```text
docs/fichas-aula/  → fichas públicas generadas por el pipeline
outputs/aula/      → fichas locales de trabajo generadas desde MCP
```

## Imágenes destacadas

`imagen_destacada.py` intenta completar `imagen_url` en:

```text
data/processed/noticias_clasificadas.json
```

Usa caché local:

```text
data/cache/cache_imagenes.json
```

## Archivos generados localmente

Normalmente no se suben a GitHub:

```text
historial.json
data/cache/
data/backups/
outputs/aula/
deprecated/
_deprecated/
.env
```

La decisión actual sobre `data/processed/` es no ignorarla de momento, aunque sus archivos no se publican en GitHub Pages porque están fuera de `docs/`.

## Probar MCP con Inspector

```powershell
mcp dev mcp_servers\comercio_digital\server.py
```

Si el Inspector intenta usar `uv` y falla, configurar manualmente:

```text
Transport Type:
STDIO

Command:
C:\Users\Juan\Google Drive\00_CDI_press\.venv\Scripts\python.exe

Arguments:
"C:/Users/Juan/Google Drive/00_CDI_press/mcp_servers/comercio_digital/server.py"
```

## Documentación complementaria

- `README_AULA.md`: funcionamiento de Aula y fichas docentes.
- `README_NEWSLETTER.md`: generación, publicación y distribución externa de la newsletter.
- `README_IMAGENES.md`: funcionamiento de imágenes destacadas.
- `README_PASO1_DOCENTE.md`: capa docente, score y criterios de selección.
- `README_INSTALACION.md`: instalación rápida y publicación.
- `mcp_servers/comercio_digital/README.md`: documentación específica del MCP.
- `REESTRUCTURACION_Y_MCP_COMERCIO_DIGITAL.md`: reestructuración y MCP.
- `DIARIO_PROYECTO.md`: histórico del proyecto.

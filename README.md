# Comercio Digital — Agregador de noticias para FP

Agregador de noticias educativas para Formación Profesional de la familia de **Comercio y Marketing**.

El proyecto recopila noticias de actualidad, las resume con IA, las clasifica por módulos y resultados de aprendizaje, añade una capa docente y genera una web estática publicable en GitHub Pages.

Web pública:

```text
https://comerciodigital.net
```

---

## Objetivo

El objetivo no es crear solo un agregador automático de noticias, sino una herramienta docente para conectar la actualidad con el aula.

El proyecto permite generar:

- una web estática de noticias clasificadas;
- una página específica de materiales de aula;
- fichas docentes en HTML y Markdown;
- una newsletter docente en HTML/Markdown;
- materiales reutilizables para Aules/Moodle;
- una base consultable desde herramientas compatibles con MCP.

---

## Estado actual

El agregador ya permite:

- leer fuentes RSS y WordPress API;
- resumir noticias;
- clasificar por módulos y resultados de aprendizaje;
- enriquecer cada noticia con criterios docentes;
- generar páginas HTML públicas en `docs/`;
- generar fichas de aula individuales;
- generar una página `aula.html`;
- generar newsletters docentes;
- aplicar SEO técnico básico;
- publicar la web en GitHub Pages;
- consultar el contenido desde un servidor MCP local.

---

## Flujo general

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

---

## Instalación rápida

Clonar el repositorio:

```powershell
git clone https://github.com/juaarbla/comercio-digital.git
cd comercio-digital
```

Crear y activar un entorno virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instalar dependencias:

```powershell
pip install -r requirements.txt
```

Crear el archivo `.env` a partir de `env.example` si se van a usar servicios externos o claves API.

---

## Ejecución recomendada

Ejecutar el pipeline completo:

```powershell
python run_pipeline.py
```

También puede usarse el panel de control en Windows:

```powershell
.\arrancar.bat
```

---

## Ejecución manual por pasos

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

---

## Estructura principal

```text
.
├─ data/
│  ├─ processed/
│  ├─ cache/
│  └─ backups/
│
├─ docs/
│  ├─ assets/
│  ├─ fichas-aula/
│  ├─ newsletter/
│  ├─ index.html
│  ├─ aula.html
│  ├─ sitemap.xml
│  └─ robots.txt
│
├─ mcp_servers/
│  └─ comercio_digital/
│
├─ outputs/
│  └─ aula/
│
├─ _documentacion/
│
├─ feeds.json
├─ run_pipeline.py
├─ arrancar.bat
├─ paths.py
└─ DIARIO_PROYECTO.md
```

---

## Archivos principales

| Archivo | Función |
|---|---|
| `feeds.json` | Fuentes RSS y WordPress API. |
| `news_aggregator.py` | Obtiene noticias y genera resúmenes. |
| `clasificador_ra.py` | Clasifica noticias por módulo y RA. |
| `enriquecer_docente.py` | Añade valor docente, actividad, conceptos y criterios de selección. |
| `imagen_destacada.py` | Completa imágenes destacadas cuando es posible. |
| `generar_web.py` | Genera portada y secciones HTML. |
| `generar_fichas_aula.py` | Genera fichas docentes HTML y Markdown. |
| `generar_aula.py` | Genera la página `docs/aula.html`. |
| `generar_newsletter.py` | Genera newsletters docentes en HTML y Markdown. |
| `generar_seo.py` | Añade metadatos SEO, sitemap y robots. |
| `run_pipeline.py` | Ejecuta el flujo completo. |
| `arrancar.bat` | Panel de control local para Windows. |
| `paths.py` | Centraliza rutas del proyecto. |
| `mcp_servers/comercio_digital/server.py` | Servidor MCP local. |

---

## Salida pública

La web se genera en la carpeta:

```text
docs/
```

Esta carpeta es la que GitHub Pages publica como sitio web.

Páginas principales:

```text
docs/index.html
docs/comercio-electronico.html
docs/internacional.html
docs/digitalizacion.html
docs/ia-marketing.html
docs/aula.html
docs/newsletter/index.html
docs/del-autor.html
docs/fichas-aula/
docs/sitemap.xml
docs/robots.txt
```

---

## Aula y fichas docentes

La página `docs/aula.html` muestra una selección de noticias con utilidad didáctica.

Cada noticia puede incluir:

- módulo relacionado;
- resultado de aprendizaje;
- tipo de uso en clase;
- pregunta detonadora;
- actividad breve;
- conceptos clave;
- justificación curricular;
- enlace a la noticia original;
- enlace a ficha docente HTML;
- enlace a ficha Markdown.

Las fichas públicas se generan en:

```text
docs/fichas-aula/
```

El material conjunto se genera en:

```text
docs/fichas-aula/material-aula.md
```

---

## Newsletter docente

La newsletter se genera en:

```text
docs/newsletter/
```

Ejemplo de generación quincenal:

```powershell
python generar_newsletter.py --periodicidad quincenal --force
```

El agregador no gestiona suscriptores ni envía correos. Solo genera la edición HTML/Markdown. La distribución debe hacerse con una herramienta externa o mediante envío manual del enlace público:

```text
https://comerciodigital.net/newsletter/
```

---

## MCP Comercio Digital

El proyecto incluye un servidor MCP local para consultar y reutilizar el contenido del agregador desde herramientas compatibles con Model Context Protocol.

Ruta:

```text
mcp_servers/comercio_digital/
```

El MCP lee el archivo:

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

Las fichas Markdown creadas desde MCP se guardan en:

```text
outputs/aula/
```

Diferencia importante:

```text
docs/fichas-aula/  → fichas públicas generadas por el pipeline
outputs/aula/      → fichas locales de trabajo generadas desde MCP
```

---

## Publicación en GitHub Pages

Tras generar la web:

```powershell
git status
git add .
git commit -m "Actualiza agregador"
git push
```

GitHub Pages publica el contenido de `docs/`.

Comprobaciones recomendadas:

```text
https://comerciodigital.net
https://comerciodigital.net/aula.html
https://comerciodigital.net/newsletter/
```

---

## Archivos locales y generados

Normalmente no se publican en la web:

```text
.env
data/cache/
data/backups/
outputs/aula/
_deprecated/
historial.json
```

Los archivos de `data/processed/` contienen datos internos del agregador. No forman parte de la web pública porque están fuera de `docs/`.

---

## Documentación complementaria

La documentación detallada está separada para mantener este README como entrada principal del repositorio.

```text
_documentacion/README_AULA.md
_documentacion/README_NEWSLETTER.md
_documentacion/README_IMAGENES.md
_documentacion/README_INSTALACION.md
_documentacion/README_PASO1_DOCENTE.md
_documentacion/REESTRUCTURACION_Y_MCP_COMERCIO_DIGITAL.md
mcp_servers/comercio_digital/README.md
DIARIO_PROYECTO.md
```

---

## Filosofía del proyecto

Este repositorio combina automatización, inteligencia artificial y criterio docente.

La IA ayuda a resumir, clasificar y enriquecer noticias, pero el valor del proyecto está en convertir la actualidad en materiales útiles para clase, conectados con módulos profesionales, resultados de aprendizaje y actividades reales de aula.

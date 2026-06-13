# Diario del Proyecto

## 2026-06-13 — Página de aula integrada y capa docente v3.2

- Problema/objetivo: consolidar la capa docente y generar una página específica de aula visualmente integrada con el resto de la web.
- Causa: la primera versión de `aula.html` funcionaba correctamente, pero usaba una plantilla visual distinta, con estilos incrustados y aspecto diferente al resto de `Comercio Digital`.
- Cambios realizados:
  - Se ha validado que `noticias_clasificadas.json` incluye `score_docente`.
  - Se mantiene `noticias_clasificadas.json` como archivo generado localmente e ignorado por Git.
  - Se ha actualizado `generar_aula.py`.
  - `docs/aula.html` se genera usando la hoja de estilos principal.
  - La página enlaza con `assets/style.css`.
  - La página utiliza las clases visuales generales del sitio:
    - `masthead`
    - `site-title`
    - `subtitle-bar`
    - `container`
    - `sec-header`
    - `seccion-lista`
    - `noticia-full`
    - `docente-box`
  - Se incorpora la sección `Aula` al menú superior.
  - Se mantienen los bloques de uso docente:
    - pregunta para el aula,
    - actividad breve,
    - conceptos clave,
    - RA,
    - justificación,
    - `score_docente`,
    - etiqueta `Newsletter`.
- Validación ejecutada:
  - Comprobado que `docs/aula.html` contiene `assets/style.css`.
  - Comprobado que `docs/aula.html` ya no contiene estilos incrustados propios de la plantilla antigua.
  - Revisión visual local de la página.
- Resultado final: `aula.html` queda integrada visualmente con el resto de la web y mantiene su finalidad docente.
- Pendientes:
  - Publicar cambios en GitHub.
  - Comprobar `https://comerciodigital.net/aula.html` tras el despliegue.
  - Valorar la creación de fichas Markdown a partir de las noticias con mayor `score_docente`.
  - Valorar la generación de newsletter docente desde `seleccion_newsletter = true`.

## 2026-06-13 — Ordenación de archivos generados y versiones de prueba

- Problema/objetivo: limpiar la carpeta raíz del proyecto para distinguir archivos activos, archivos generados y versiones de prueba.
- Causa: durante las pruebas de la capa docente se generaron versiones intermedias como `noticias_clasificadas_docente.json`, `noticias_clasificadas_v2.json`, `noticias_clasificadas_v3.json`, backups y documentación temporal.
- Cambios realizados:
  - Se movieron versiones antiguas y backups a carpeta de archivo/deprecated.
  - Se decidió no subir a Git los JSON generados localmente.
  - Se revisó `.gitignore` para mantener fuera de Git:
    - `noticias_resumidas.json`
    - `noticias_clasificadas.json`
    - `historial.json`
    - backups `noticias_clasificadas.backup_*.json`
    - carpetas `deprecated/` y `_deprecated/`.
- Validación ejecutada:
  - `git status`.
  - Comprobación de que `noticias_clasificadas.json` no aparece como modificado por estar ignorado.
  - Comprobación directa de `score_docente` mediante `Select-String`.
- Resultado final: la raíz queda más limpia y Git se centra en scripts, documentación y salida estática en `docs/`.
- Pendientes:
  - Mantener la política de no versionar JSON generados salvo decisión expresa.
  - Revisar periódicamente que los backups no queden en raíz.

## 2026-06-13 — Validación de capa docente v3

- Problema/objetivo: corregir el exceso de noticias marcadas como `alto` y la selección excesiva para newsletter.
- Causa: las versiones iniciales de la capa docente eran demasiado generosas. Muchas noticias quedaban como `valor_docente = alto` y prácticamente todas se marcaban para newsletter.
- Cambios realizados:
  - Se introdujo `score_docente`.
  - Se aplicaron pesos positivos por relevancia docente.
  - Se añadieron penalizaciones para eventos, boletines, jornadas o contenidos con menor valor directo.
  - Se limitó `seleccion_newsletter` por defecto.
  - Se priorizó la selección por score, presencia de imagen, fecha y diversidad de módulos.
- Validación ejecutada:
  - Ejecución de `python enriquecer_docente.py --forzar`.
  - Comprobación de que `noticias_clasificadas.json` contiene `score_docente`.
  - Generación de `docs/aula.html` con `python generar_aula.py --max-noticias 25`.
- Resultado final: el JSON principal queda enriquecido localmente con puntuación docente y la página de aula se genera correctamente.
- Pendientes:
  - Seguir revisando si los umbrales de `score_docente` deben ajustarse.
  - Mejorar la representación de CDI si queda infrarrepresentado.
  - Crear fichas Markdown solo a partir de noticias seleccionadas.

## 2026-06-12 — SEO técnico básico

- Problema/objetivo: mejorar la visibilidad técnica de la web en buscadores y evitar que todas las páginas compartan los mismos metadatos.
- Causa: la web disponía de títulos y descripciones básicos, pero no generaba metadatos SEO específicos por sección, `sitemap.xml`, `robots.txt` ni etiquetas sociales completas.
- Cambios realizados:
  - Se ha creado `generar_seo.py`.
  - El script procesa los archivos HTML generados en `docs/`.
  - Se añaden títulos SEO específicos por sección.
  - Se añaden meta descriptions diferenciadas.
  - Se actualizan las etiquetas canonical.
  - Se añaden metadatos Open Graph.
  - Se añaden etiquetas Twitter Card.
  - Se genera `docs/sitemap.xml`.
  - Se genera `docs/robots.txt`.
  - Se ha actualizado `run_pipeline.py` para ejecutar `generar_seo.py` después de la generación de páginas.
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
   ↓
generar_aula.py
   ↓
generar_seo.py
```

- Validación prevista:
  - Ejecutar `python generar_seo.py`.
  - Comprobar `docs/sitemap.xml` y `docs/robots.txt`.
  - Revisar el `<head>` de `docs/index.html` y de una página de sección.
  - Ejecutar después `python run_pipeline.py`.
- Resultado final: pendiente de validación final tras publicación.
- Pendientes:
  - Validar la salida local.
  - Publicar los cambios en GitHub.
  - Comprobar `https://comerciodigital.net/sitemap.xml`.
  - Comprobar `https://comerciodigital.net/robots.txt`.
  - Crear una página `sobre.html`.
  - Añadir introducciones SEO permanentes en las páginas de sección.

## 2026-06-10 — Ajuste de contenidos propios “Del Autor”

- Problema/objetivo: ajustar la presencia de los contenidos propios en la web sin sobrecargar la portada.
- Causa: al clasificar los artículos de `juanarmada.com` como “Del Autor”, el bloque generado en portada ocupaba demasiado espacio para un único contenido y rompía el equilibrio visual de la página.
- Cambios realizados:
  - Se mantiene la detección de contenidos propios mediante el dominio `juanarmada.com`.
  - Los artículos propios siguen apareciendo en la sección `Del Autor`.
  - Se mantiene la página `docs/del-autor.html`.
  - Se mantiene la clasificación docente por módulo y RA.
  - Se mantiene el acordeón “Uso en el aula”.
  - Se ha eliminado el bloque “Del Autor” de la portada.
- Validación ejecutada:
  - Generación local con `python generar_web.py`.
  - Revisión visual de `docs/index.html`.
  - Revisión visual de `docs/del-autor.html`.
- Resultado final: la portada queda más limpia y equilibrada, mientras que los contenidos propios siguen accesibles desde el menú y desde su página específica.
- Pendientes:
  - Ejecutar `python run_pipeline.py`.
  - Revisar la web publicada.
  - Subir los cambios a GitHub.

## 2026-06-09 — Capa docente inicial

- Problema/objetivo: añadir una capa docente a las noticias para que el agregador no sea solo informativo, sino también útil para el aula.
- Causa: las noticias estaban clasificadas por módulo y RA, pero no incluían una propuesta directa de uso didáctico.
- Cambios realizados:
  - Se ha creado `enriquecer_docente.py`.
  - Cada noticia puede incorporar:
    - `pregunta_aula`
    - `conceptos_clave`
    - `actividad_breve`
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
- Pendientes:
  - Revisar periódicamente la calidad de preguntas, conceptos y actividades generadas.
  - Mejorar la selección editorial de noticias realmente útiles para el aula.

## 2026-06-09 — Pipeline unificado

- Problema/objetivo: simplificar la ejecución diaria del agregador y evitar tener que lanzar varios scripts manualmente.
- Causa: el flujo dependía de ejecutar por separado `news_aggregator.py`, `clasificador_ra.py`, `imagen_destacada.py` y `generar_web.py`.
- Cambios realizados:
  - Se ha creado `run_pipeline.py`.
  - Se ha integrado `enriquecer_docente.py` en el flujo.
- Flujo en ese momento:

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

- Validación ejecutada:
  - Ejecución local con `python run_pipeline.py`.
- Resultado final: pipeline completado correctamente y web local actualizada.
- Pendientes:
  - Mantener actualizado `env.example` cuando se añadan nuevas variables de configuración.
  - Integrar nuevos pasos posteriores cuando se creen.

## 2026-06-08 — Fuente WordPress API y publicación de contenidos propios

- Problema: la web `juanarmada.com` publicó una noticia del día que no aparecía en el pipeline por desfase del RSS.
- Solución:
  - Se añadió fallback de fuente `wordpress_api` en `feeds.json` usando `wp-json/wp/v2/posts`.
- Implementación:
  - `news_aggregator.py` ahora soporta `source: "wordpress_api"`.
  - Normaliza posts de WordPress.
  - Mapea categorías.
  - Evalúa recencia con fechas ISO.
- Estabilidad:
  - Se dejó `generar_web.py` con una sola implementación activa, sin duplicados heredados.
- Validación:
  - Ejecución completa correcta.
  - Publicación confirmada en portada y sección IA.
- Resultado final: los contenidos propios pueden entrar en el flujo junto con noticias externas.
- Pendientes:
  - Revisar periódicamente que los artículos propios no saturen la portada.
  - Mantener la sección `Del Autor` como espacio específico.

## 2026-06-08 — Configuración de dominio y GitHub Pages

- Problema/objetivo: publicar el agregador en un dominio propio usando GitHub Pages.
- Causa: el dominio `comerciodigital.net` necesitaba configuración DNS correcta para apuntar al repositorio de GitHub Pages.
- Cambios realizados:
  - Configuración de registros A para GitHub Pages:
    - `185.199.108.153`
    - `185.199.109.153`
    - `185.199.110.153`
    - `185.199.111.153`
  - Configuración de CNAME para `www` apuntando a `juaarbla.github.io`.
  - Verificación del archivo `CNAME`.
  - Activación de HTTPS en GitHub Pages.
- Validación ejecutada:
  - Corrección de errores de DNS.
  - Verificación del dominio personalizado.
  - Comprobación de publicación en `https://comerciodigital.net`.
- Resultado final: dominio propio funcionando con GitHub Pages y HTTPS activo.
- Pendientes:
  - Documentar el proceso para futuras referencias.
  - Mantener la configuración DNS sin modificar salvo necesidad.

## Checklist diaria

1. Activar el entorno virtual (`venv`).
2. Ejecutar el pipeline completo:

```bash
python run_pipeline.py
```

3. Revisar la salida en consola y confirmar que no hay errores.
4. Verificar `docs/index.html`.
5. Verificar al menos una sección temática, por ejemplo `docs/ia-marketing.html`.
6. Verificar `docs/aula.html`.
7. Comprobar una noticia con el acordeón “Uso en el aula”.
8. Verificar que `docs/del-autor.html` se genera cuando existen contenidos propios.
9. Confirmar que la portada no muestra el bloque “Del Autor”.
10. Verificar que existen `docs/sitemap.xml` y `docs/robots.txt`.
11. Revisar que la portada y una página de sección tienen:
    - `title`
    - `meta description`
    - `canonical`
    - Open Graph
12. Subir los cambios a GitHub.
13. Comprobar la publicación en `https://comerciodigital.net`.
14. Comprobar `https://comerciodigital.net/aula.html`.
15. Comprobar `https://comerciodigital.net/sitemap.xml`.
16. Comprobar `https://comerciodigital.net/robots.txt`.
17. Si hubo cambios funcionales, registrar una nueva entrada en este diario.

## Comandos útiles

### Ejecutar pipeline completo

```powershell
python run_pipeline.py
```

### Generar solo la web principal

```powershell
python generar_web.py
```

### Generar solo la página de aula

```powershell
python generar_aula.py --max-noticias 25
```

### Ejecutar SEO técnico

```powershell
python generar_seo.py
```

### Comprobar que `aula.html` usa el CSS global

```powershell
Select-String -Path docs\aula.html -Pattern "assets/style.css"
Select-String -Path docs\aula.html -Pattern "<style>"
```

Resultado esperado:

```text
assets/style.css  → aparece
<style>           → no aparece
```

### Comprobar que el JSON local contiene `score_docente`

```powershell
Select-String -Path noticias_clasificadas.json -Pattern "score_docente"
```

## Política de archivos generados

No subir normalmente a GitHub:

```text
historial.json
noticias_resumidas.json
noticias_clasificadas.json
noticias_clasificadas.backup_*.json
deprecated/
_deprecated/
```

Sí subir normalmente:

```text
*.py
README.md
README_AULA_V32.md
README_PASO1_DOCENTE_V3.md
DIARIO_PROYECTO.md
docs/
```

## Plantilla de nueva entrada

```md
## AAAA-MM-DD — Título breve

- Problema/objetivo:
- Causa (si aplica):
- Cambios realizados:
- Validación ejecutada:
- Resultado final:
- Pendientes:
```

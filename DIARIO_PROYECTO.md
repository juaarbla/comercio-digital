# Diario del Proyecto

## 2026-06-16 — Ordenación documental e imágenes destacadas

- Problema/objetivo:
  - Ordenar los README y actualizar el diario tras la consolidación de Aula, fichas docentes, material Markdown e imagen destacada.
- Causa:
  - Durante las mejoras se habían acumulado varios README de parche (`README_AULA_V32.md`, `README_PASO1_DOCENTE_V3.md`, `README_INSTALACION.md`) y convenía unificar el criterio documental.
- Cambios realizados:
  - Se reorganiza `README.md` como documento principal del proyecto.
  - Se crea/actualiza documentación específica para:
    - Aula y fichas docentes.
    - Capa docente.
    - Imágenes destacadas.
    - Instalación y publicación.
  - Se documenta el flujo definitivo del pipeline:
    ```text
    news_aggregator.py
    clasificador_ra.py
    enriquecer_docente.py
    imagen_destacada.py
    generar_web.py
    generar_fichas_aula.py
    generar_aula.py
    generar_seo.py
    ```
  - Se documenta que `imagen_destacada.py` puede usar:
    - `IMAGE_PROVIDER=rss`
    - `IMAGE_PROVIDER=openai`
  - Se documenta el uso de `cache_imagenes.json`.
- Validación ejecutada:
  - Revisión de los README existentes.
  - Revisión de `imagen_destacada.py`.
  - Consolidación de decisiones recientes sobre Aula, fichas y Markdown.
- Resultado final:
  - Documentación más clara y separada por finalidad.
- Pendientes:
  - Sustituir los README antiguos por los documentos ordenados.
  - Revisar `git status`.
  - Publicar los cambios si procede.

## 2026-06-16 — Recuperación de recursos docentes en Aula

- Problema/objetivo:
  - `aula.html` había quedado visualmente correcto, pero algunas noticias habían perdido información útil para trabajar en clase.
- Causa:
  - Algunas versiones intermedias de `generar_aula.py` mostraban solo la pregunta para el aula o recuperaban campos internos como `Score` y `Newsletter`.
- Cambios realizados:
  - Se elimina de la interfaz pública:
    - `score_docente`
    - `valor_docente`
    - `seleccion_newsletter`
  - Se recupera la ficha docente completa:
    - módulo;
    - RA;
    - pregunta detonadora;
    - actividad breve;
    - conceptos clave;
    - justificación de encaje con el RA.
  - Se añaden enlaces por noticia:
    - `Ver ficha docente`;
    - `Descargar Markdown`;
    - `Leer noticia completa`.
  - Se genera `docs/fichas-aula/material-aula.md`.
  - Se añade enlace a `Descargar material de aula MD`.
- Validación ejecutada:
  - Revisión visual de `docs/aula.html`.
  - Comprobación de que no aparecen duplicados de `Volver a portada`.
  - Comprobación de enlaces a Markdown y fichas.
- Resultado final:
  - Aula vuelve a tener valor docente práctico sin mostrar campos internos.
- Pendientes:
  - Revisar la calidad de las actividades generadas.
  - Valorar filtros por módulo/RA en Aula.

## 2026-06-16 — Corrección de portada, menú y Del Autor

- Problema/objetivo:
  - La portada se rompía en algunos bloques de tres noticias.
  - `Aula` desaparecía del menú en alguna regeneración.
  - Algunos enlaces buscaban `autor.html` en lugar de `del-autor.html`.
- Causa:
  - Algunas tarjetas de portada cortaban resúmenes con etiquetas HTML como `<em>`, rompiendo el DOM.
  - `Aula` dependía de la lógica de secciones en algunas versiones del generador.
  - Existían referencias antiguas a `autor.html`.
- Cambios realizados:
  - `generar_web.py` usa texto plano seguro en tarjetas de portada.
  - El menú incluye siempre `Aula`.
  - Se fija la ruta correcta:
    ```text
    del-autor.html
    ```
  - Se evita el uso de:
    ```text
    autor.html
    ```
- Validación ejecutada:
  - Revisión visual de portada.
  - Revisión de menú.
  - Búsqueda de `autor.html`.
- Resultado final:
  - Portada estable, menú correcto y enlaces de autor unificados.
- Pendientes:
  - Mantener esta versión como base y evitar aplicar parches antiguos.

## 2026-06-15 — Fichas docentes HTML y Markdown

- Problema/objetivo:
  - Convertir las noticias de Aula en materiales reutilizables.
- Cambios realizados:
  - Se crea `generar_fichas_aula.py`.
  - Se generan fichas HTML públicas.
  - Se generan fichas Markdown reutilizables.
  - Se limita la generación a un máximo de 10 fichas por ejecución.
  - Se genera `index_fichas.json` para enlazar fichas desde `aula.html`.
- Resultado final:
  - La estructura Aula → Ficha → Markdown queda operativa.
- Pendientes:
  - Mejorar criterios de selección por diversidad de módulos.

## 2026-06-13 — Página de aula integrada y capa docente v3.2

- Problema/objetivo:
  - Consolidar la capa docente y generar una página específica de aula visualmente integrada con el resto de la web.
- Cambios realizados:
  - `docs/aula.html` se genera usando `docs/assets/style.css`.
  - Se usan clases visuales generales del sitio:
    - `masthead`
    - `site-title`
    - `subtitle-bar`
    - `container`
    - `sec-header`
    - `seccion-lista`
    - `noticia-full`
    - `docente-box`
  - Se incorpora `Aula` al menú superior.
- Resultado final:
  - `aula.html` queda integrada visualmente con el resto de la web.
- Pendientes:
  - Seguir mejorando la calidad de las actividades docentes.

## 2026-06-13 — Ordenación de archivos generados

- Problema/objetivo:
  - Limpiar la raíz del proyecto y distinguir entre archivos activos y generados.
- Cambios realizados:
  - Se decide no subir a Git los JSON generados localmente.
  - Se revisa la política de `.gitignore`.
- Archivos generados que no se deben subir normalmente:
  ```text
  historial.json
  noticias_resumidas.json
  noticias_clasificadas.json
  noticias_clasificadas.backup_*.json
  cache_imagenes.json
  deprecated/
  _deprecated/
  ```

## 2026-06-13 — Validación de capa docente v3

- Problema/objetivo:
  - Evitar que demasiadas noticias aparezcan como `valor_docente = alto`.
- Cambios realizados:
  - Se introduce `score_docente`.
  - Se endurecen los criterios.
  - Se limita `seleccion_newsletter`.
- Resultado final:
  - El JSON principal queda enriquecido con puntuación docente.

## 2026-06-12 — SEO técnico básico

- Cambios realizados:
  - Se crea `generar_seo.py`.
  - Se generan o actualizan:
    - títulos SEO;
    - meta descriptions;
    - canonical;
    - Open Graph;
    - Twitter Card;
    - `sitemap.xml`;
    - `robots.txt`.

## 2026-06-10 — Ajuste de contenidos propios “Del Autor”

- Cambios realizados:
  - Se detectan contenidos propios mediante `juanarmada.com`.
  - Se genera `docs/del-autor.html`.
  - Se elimina el bloque “Del Autor” de portada para no sobrecargarla.

## 2026-06-09 — Capa docente inicial

- Cambios realizados:
  - Se crea `enriquecer_docente.py`.
  - Se añaden:
    - `pregunta_aula`;
    - `conceptos_clave`;
    - `actividad_breve`.
  - Se añade acordeón docente en páginas de sección.

## 2026-06-09 — Pipeline unificado

- Cambios realizados:
  - Se crea `run_pipeline.py`.
  - Se integran pasos principales del flujo.

## 2026-06-08 — Fuente WordPress API y publicación de contenidos propios

- Cambios realizados:
  - Se añade soporte para `wordpress_api` en `feeds.json`.
  - Se incorporan contenidos propios al flujo.

## 2026-06-08 — Configuración de dominio y GitHub Pages

- Cambios realizados:
  - Registros A para GitHub Pages:
    - `185.199.108.153`
    - `185.199.109.153`
    - `185.199.110.153`
    - `185.199.111.153`
  - CNAME:
    ```text
    www → juaarbla.github.io
    ```
  - HTTPS activo.

## Checklist diaria

1. Ejecutar:
   ```powershell
   python run_pipeline.py
   ```
2. Revisar:
   ```text
   docs/index.html
   docs/aula.html
   docs/fichas-aula/material-aula.md
   docs/sitemap.xml
   docs/robots.txt
   ```
3. Comprobar:
   ```powershell
   Select-String -Path docs\index.html -Pattern "aula.html"
   Select-String -Path docs\aula.html -Pattern "Descargar Markdown"
   Select-String -Path docs\*.html -Pattern "autor.html"
   ```
4. Publicar cambios.
5. Comprobar:
   ```text
   https://comerciodigital.net
   https://comerciodigital.net/aula.html
   ```

## Plantilla de nueva entrada

```md
## AAAA-MM-DD — Título breve

- Problema/objetivo:
- Causa:
- Cambios realizados:
- Validación ejecutada:
- Resultado final:
- Pendientes:
```

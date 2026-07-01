# Diario del Proyecto

## 2026-07-01 — Fase v0.5: control de calidad, seguimiento y coherencia visual

- Problema/objetivo:
  - Avanzar en la fase v0.5 del agregador `Comercio Digital` sin cambiar su arquitectura principal.
  - Mejorar el control de calidad, la trazabilidad del pipeline, la revisión editorial y la coherencia visual entre portada, Aula y Newsletter.
- Causa:
  - La publicación diaria ya estaba automatizada en Windows mediante el Programador de tareas.
  - La newsletter quincenal ya funcionaba como salida editorial.
  - La web había crecido con varias salidas (`index.html`, `aula.html`, `newsletter/`, fichas de aula), pero algunas partes tenían cabeceras y navegación ligeramente diferentes.
  - La fase v0.5 debía centrarse en observabilidad y mantenimiento, no en rediseño completo.
- Cambios realizados:
  - Se crea `_documentacion/ROADMAP_v0.5.md` para definir el alcance de la fase antes de tocar código.
  - Se crea `generar_informe_pipeline.py`, un script de solo lectura que genera:
    ```text
    logs/informe_pipeline_YYYY-MM-DD.md
    ```
  - El informe post-pipeline resume:
    ```text
    noticias resumidas
    noticias clasificadas
    fuentes configuradas
    fichas HTML/MD generadas
    newsletters disponibles
    distribución por módulo
    distribución por fuente
    valor docente
    tipo de uso
    alertas editoriales
    ```
  - Se integra el informe post-pipeline en `publicar_web_diaria.bat`.
  - Se decide que un fallo del informe no debe bloquear la publicación diaria.
  - Se añade al BAT diario un resumen Git antes del commit automático:
    ```powershell
    git status --short
    git diff --cached --stat
    ```
  - Se añade en portada un bloque “Última newsletter” enlazando a:
    ```text
    newsletter/index.html
    ```
  - Se corrige el favicon en las páginas de newsletter usando la ruta relativa correcta:
    ```html
    ../assets/favicon.svg
    ```
  - Se actualiza `feeds.json` para reforzar Marketing Digital, incluyendo HubSpot Marketing.
  - Se crea `web_ui_common.py` para centralizar elementos comunes de interfaz:
    ```text
    fecha larga
    head HTML
    favicon
    hoja de estilos
    cabecera
    navegación
    barra de subtítulo
    footer
    ```
  - Se adaptan `generar_web.py`, `generar_aula.py` y `generar_newsletter.py` para reutilizar los elementos comunes de interfaz.
- Validación ejecutada:
  - Se prueba manualmente `generar_informe_pipeline.py`.
  - Se confirma la generación del informe diario en `logs/`.
  - Se ejecutan los generadores principales:
    ```powershell
    python .\generar_web.py
    python .\generar_aula.py
    python .\generar_newsletter.py --force
    ```
  - Se revisan visualmente portada, Aula y Newsletter.
  - Se corrige la diferencia visual en cabeceras y navegación mediante el módulo común.
  - Se comprueba el estado de Git tras los cambios:
    ```powershell
    git status
    git diff --stat
    ```
  - El repositorio queda limpio tras los commits realizados.
- Decisiones tomadas:
  - Mantener la automatización diaria actual sin convertirla en un flujo en dos pasos.
  - Añadir trazabilidad al log diario sin romper el Programador de tareas.
  - No abordar Raspberry Pi en v0.5.
  - No crear panel de administración.
  - No cambiar la arquitectura ni introducir base de datos.
  - Unificar interfaz con un módulo común, pero sin rediseñar la web.
- Resultado final:
  - v0.5.0 cerrada: roadmap creado.
  - v0.5.1 cerrada: informe post-pipeline creado y probado.
  - v0.5.2 cerrada: informe integrado en publicación diaria.
  - v0.5.3 cerrada: resumen Git de cambios añadido al log diario.
  - v0.5.4 cerrada: bloque “Última newsletter” añadido en portada.
  - v0.5.5 cerrada: favicon corregido en newsletter.
  - v0.5.6 cerrada: revisión inicial de fuentes con incorporación de HubSpot Marketing.
  - v0.5.7 cerrada: cabecera, navegación y footer centralizados en `web_ui_common.py`.
- Pendientes:
  - Revisar una ejecución completa del pipeline diario programado.
  - Confirmar que el informe diario se genera correctamente en una ejecución automática real.
  - Revisar visualmente la versión publicada en GitHub Pages.
  - Si todo está correcto, cerrar la fase con etiqueta:
    ```powershell
    git tag v0.5
    git push origin v0.5
    ```

## 2026-06-24 — Fase v0.4: newsletter, selección docente y limpieza técnica controlada

- Problema/objetivo:
  - Iniciar la fase v0.4 del agregador `Comercio Digital` sin añadir complejidad innecesaria.
  - Mejorar la newsletter docente, afinar la selección de noticias y realizar una limpieza técnica prudente.
- Causa:
  - La v0.3 estaba cerrada, etiquetada y subida a GitHub.
  - El proyecto ya era estable: web publicada, Aula operativa, fichas docentes, SEO básico, documentación y pipeline funcionando.
  - La newsletter existía, pero funcionaba todavía como una lista plana de noticias destacadas.
- Cambios realizados:
  - Se revisa la hoja de ruta de la v0.4 antes de tocar código.
  - Se confirma que la newsletter debe seguir siendo una salida manual/quincenal y no una herramienta de envío de correos.
  - Se mejora `generar_newsletter.py` para transformar la newsletter en una pieza editorial:
    ```text
    Noticia destacada
    Selección docente de la quincena
    Breves para seguir la actualidad
    Propuesta rápida para clase
    Pregunta para debate
    ```
  - Se cambia la periodicidad por defecto a quincenal.
  - Se ajusta la selección a 6 noticias:
    ```text
    1 noticia destacada
    3 noticias docentes
    2 breves
    ```
  - Se mejora la selección docente de la newsletter usando campos ya existentes del JSON enriquecido:
    ```text
    seleccion_newsletter
    valor_docente
    generar_ficha
    actividad_breve
    pregunta_aula
    conceptos_clave
    ra_asignado
    score_docente
    tipo_uso
    modulo_relacionado
    ```
  - Se añade equilibrio por módulos para evitar newsletters demasiado repetitivas.
  - Se revisa el inventario inicial de scripts Python de la raíz.
  - Se decide no mover scripts ni reestructurar carpetas en esta fase.
  - Se documenta en `run_pipeline.py` que la newsletter queda fuera del pipeline principal y se genera manualmente cuando toque publicar edición.
- Validación ejecutada:
  - Se genera la newsletter quincenal en HTML y Markdown.
  - Se revisa la estructura de `docs/newsletter/newsletter-2026-06-Q2.md`.
  - Se confirma una selección equilibrada con comercio electrónico, digitalización, IA, logística, marketplaces y ciberseguridad.
  - Se ejecuta el pipeline completo:
    ```powershell
    python .
un_pipeline.py
    ```
  - Resultado de la prueba:
    ```text
    SEO aplicado a 29 páginas HTML.
    Pipeline completado correctamente.
    Duración aproximada: 0:02:43.
    ```
  - Se comprueba el estado de Git:
    ```powershell
    git status
    git status --short
    ```
  - El repositorio queda limpio tras la prueba:
    ```text
    nothing to commit, working tree clean
    ```
- Decisiones tomadas:
  - La newsletter se mantiene fuera del pipeline automático.
  - `generar_newsletter.py` se ejecutará manualmente cuando toque publicar una edición semanal o quincenal.
  - No se añaden campos nuevos al JSON en esta fase.
  - No se mueve ningún script de la raíz durante la v0.4.4.
  - La limpieza técnica se limita a documentación, validación y decisiones explícitas.
- Resultado final:
  - v0.4.1 cerrada: diseño funcional de newsletter.
  - v0.4.2 cerrada: estructura editorial de newsletter.
  - v0.4.3 cerrada: mejora de selección docente de newsletter.
  - v0.4.4 validada: limpieza técnica controlada y pipeline probado.
- Pendientes:
  - Valorar si se añade en portada un bloque de “Última newsletter”.
  - Revisar más adelante si conviene documentar un inventario completo de scripts.
  - Mantener la distribución de la newsletter como envío manual o herramienta externa hasta validar su uso real.

## 2026-06-19 — Newsletter docente integrada en el agregador

- Problema/objetivo:
  - Añadir una salida periódica del agregador en formato newsletter para compartir una selección breve de noticias con utilidad docente.
  - Evitar convertir el agregador en una herramienta de envío de correos o gestión de suscriptores.
- Causa:
  - Aula y fichas docentes ya generan materiales reutilizables, pero faltaba una pieza de curación periódica para distribuir por correo, departamentos, Aules/Moodle o redes.
- Cambios realizados:
  - Se crea `generar_newsletter.py`.
  - Se genera la carpeta pública:
    ```text
    docs/newsletter/
    ```
  - Cada edición genera:
    ```text
    docs/newsletter/newsletter-AAAA-WSS.html
    docs/newsletter/newsletter-AAAA-WSS.md
    docs/newsletter/index.html
    ```
  - Se añade soporte para periodicidad:
    ```powershell
    python generar_newsletter.py --periodicidad semanal
    python generar_newsletter.py --periodicidad quincenal
    ```
  - La newsletter se genera solo cuando se ejecuta el script; no se crea una edición diaria automáticamente.
  - Se integra `Newsletter` en el menú principal de portada, secciones, Aula, fichas docentes y newsletter.
  - Se ajusta el diseño visual en `docs/assets/style.css` para mantener coherencia con el estilo periódico del agregador.
- Decisión tomada:
  - El agregador no gestionará suscriptores ni enviará correos.
  - La distribución se hará con una herramienta externa o mediante envío manual del enlace público.
- Procedimiento de uso:
  ```powershell
  python generar_newsletter.py --periodicidad quincenal --force
  git add docs/newsletter docs/assets/style.css generar_newsletter.py
  git commit -m "Publica newsletter docente"
  git push
  ```
- Distribución recomendada:
  - Enviar por Gmail, Brevo, Mailchimp, Substack, MailerLite u otra herramienta externa.
  - El correo debe ser breve e incluir enlace a:
    ```text
    https://comerciodigital.net/newsletter/
    ```
- Resultado final:
  - Newsletter docente operativa como salida pública HTML/Markdown del agregador.
- Pendientes:
  - Decidir periodicidad estable: semanal o quincenal.
  - Añadir en portada un bloque de “Última newsletter”.
  - Valorar distribución externa con Brevo, Mailchimp, Substack o similar.

## 2026-06-18 — MCP Comercio Digital v0.2 y generación de fichas Markdown

- Problema/objetivo:
  - Avanzar desde un MCP de consulta hacia un MCP capaz de generar materiales docentes reutilizables.
- Causa:
  - La versión v0.1 permitía consultar noticias clasificadas, pero no generaba archivos persistentes.
- Cambios realizados:
  - Se consolida la estructura `mcp_servers/comercio_digital/`.
  - Se añade la herramienta MCP:
    ```text
    generar_ficha_md(url_o_titulo)
    ```
  - La herramienta busca una noticia por título o URL.
  - Genera una ficha de aula en Markdown.
  - Guarda la ficha en:
    ```text
    outputs/aula/
    ```
  - Se mantiene el MCP como herramienta segura:
    - no publica;
    - no modifica JSON;
    - no toca WordPress;
    - no ejecuta el pipeline;
    - no hace push a GitHub.
- Validación ejecutada:
  - Se inicia MCP Inspector.
  - Se conecta el servidor con transporte STDIO.
  - Se usa el Python del entorno virtual:
    ```text
    C:\Users\Juan\Google Drive\00_CDI_press\.venv\Scripts\python.exe
    ```
  - Se apunta al servidor:
    ```text
    C:/Users/Juan/Google Drive/00_CDI_press/mcp_servers/comercio_digital/server.py
    ```
  - Se comprueba que aparece `generar_ficha_md`.
  - Se ejecuta la herramienta con una noticia real.
  - Se confirma la creación del archivo Markdown en `outputs/aula/`.
- Resultado final:
  - MCP Comercio Digital v0.2 operativo.
- Pendientes:
  - Decidir si `outputs/aula/` se ignora en Git.
  - Actualizar documentación principal.
  - Valorar una v0.3 para generar newsletter docente.

## 2026-06-18 — Reestructuración de datos internos y MCP Comercio Digital v0.1

- Problema/objetivo:
  - Preparar el agregador para integraciones MCP sin mezclar datos internos, cachés y backups en la raíz del proyecto.
- Causa:
  - Los JSON principales, cachés y backups estaban en la raíz.
- Cambios realizados:
  - Se crea la estructura:
    ```text
    data/processed/
    data/cache/
    data/backups/
    outputs/aula/
    mcp_servers/comercio_digital/
    ```
  - Se mueven los JSON principales:
    ```text
    data/processed/noticias_resumidas.json
    data/processed/noticias_clasificadas.json
    ```
  - Se mueven las cachés:
    ```text
    data/cache/cache_clasificacion.json
    data/cache/cache_imagenes.json
    ```
  - Se mueven los backups:
    ```text
    data/backups/
    ```
  - Se crea `paths.py` para centralizar rutas.
  - Se actualizan scripts principales para usar las nuevas rutas.
  - Se crea MCP Comercio Digital v0.1 para consultar el agregador.
- Validación ejecutada:
  - Prueba de scripts individuales.
  - Ejecución de `python run_pipeline.py`.
  - Comprobación de que los JSON no reaparecen en la raíz.
  - Prueba de MCP con Inspector.
- Resultado final:
  - Pipeline funcionando.
  - Estructura interna más limpia.
  - MCP v0.1 operativo.
- Pendientes:
  - Continuar con generación de fichas Markdown.
  - Actualizar documentación.

## 2026-06-16 — Ordenación documental e imágenes destacadas

- Problema/objetivo:
  - Ordenar los README y actualizar el diario tras la consolidación de Aula, fichas docentes, material Markdown e imagen destacada.
- Cambios realizados:
  - Se reorganiza `README.md` como documento principal del proyecto.
  - Se crea/actualiza documentación específica para:
    - Aula y fichas docentes.
    - Capa docente.
    - Imágenes destacadas.
    - Instalación y publicación.
  - Se documenta el flujo definitivo del pipeline.
- Resultado final:
  - Documentación más clara y separada por finalidad.

## 2026-06-16 — Recuperación de recursos docentes en Aula

- Problema/objetivo:
  - `aula.html` había quedado visualmente correcto, pero algunas noticias habían perdido información útil para trabajar en clase.
- Cambios realizados:
  - Se elimina de la interfaz pública:
    - `score_docente`
    - `valor_docente`
    - `seleccion_newsletter`
  - Se recupera la ficha docente completa.
  - Se añaden enlaces por noticia:
    - `Ver ficha docente`;
    - `Descargar Markdown`;
    - `Leer noticia completa`.
  - Se genera `docs/fichas-aula/material-aula.md`.
- Resultado final:
  - Aula vuelve a tener valor docente práctico sin mostrar campos internos.

## 2026-06-15 — Fichas docentes HTML y Markdown

- Problema/objetivo:
  - Convertir las noticias de Aula en materiales reutilizables.
- Cambios realizados:
  - Se crea `generar_fichas_aula.py`.
  - Se generan fichas HTML públicas.
  - Se generan fichas Markdown reutilizables.
  - Se genera `index_fichas.json`.
- Resultado final:
  - La estructura Aula → Ficha → Markdown queda operativa.

## 2026-06-13 — Página de aula integrada y capa docente v3.2

- Cambios realizados:
  - `docs/aula.html` se genera usando `docs/assets/style.css`.
  - Se incorpora `Aula` al menú superior.
- Resultado final:
  - `aula.html` queda integrada visualmente con el resto de la web.

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

## 2026-06-09 — Pipeline unificado

- Cambios realizados:
  - Se crea `run_pipeline.py`.
  - Se integran pasos principales del flujo.

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
   docs/newsletter/index.html
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
   https://comerciodigital.net/newsletter/
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

---
project_name: Comercio Digital
project_slug: comercio-digital
project_type: software
ownership: propio
role: autor
status: activo
priority: media
current_phase: "v0.9 · Estabilización, observabilidad editorial y mantenimiento operativo"
next_action: Revisar las fuentes activas sin aportación histórica usando los informes recientes
next_review: 2026-08-11
repository: https://github.com/juaarbla/comercio-digital
production_url: https://comerciodigital.net
updated_at: 2026-07-27
---

# Estado del proyecto

## 1. Identificación

- **Nombre:** Comercio Digital
- **Nombre corto o slug:** `comercio-digital`
- **Descripción:** Agregador de noticias educativas para Formación Profesional de la familia de Comercio y Marketing. Resume y clasifica noticias, añade contexto docente y genera una web estática, fichas de aula y newsletters.
- **Tipo de proyecto:** Software con finalidad docente y editorial.
- **Propiedad:** Propio.
- **Responsable:** Creador del proyecto.
- **Mi función:** Creador y autor.
- **Estado general:** Activo en producción, con mantenimiento y observación editorial.
- **Prioridad:** Media-baja; normalizada como `media` en los metadatos.
- **Fecha de inicio:** 2026-06-08, primera fecha verificable en Git.
- **Fecha objetivo:** Pendiente de confirmar.
- **Última revisión:** 2026-07-27.

## 2. Objetivo

Comercio Digital conecta la actualidad de comercio, marketing y digitalización con el aula de Formación Profesional. Recopila noticias, las resume y clasifica por módulos y resultados de aprendizaje, y les añade una capa de utilidad docente.

El resultado esperado es una web educativa actualizada, con fichas, materiales y newsletters reutilizables. El proyecto tiene éxito cuando el pipeline funciona de forma estable, los contenidos publicados mantienen valor docente y las fuentes ofrecen diversidad suficiente sin alertas críticas.

## 3. Alcance actual

### Incluido

- Agregación desde RSS y WordPress API.
- Resumen y clasificación de noticias con apoyo de modelos de lenguaje.
- Enriquecimiento docente, conceptos, actividades e imágenes destacadas.
- Generación de web estática, fichas de aula, SEO y datos estructurados.
- Generación, revisión, publicación y envío controlado de newsletters.
- Publicación diaria automatizada desde un VPS.
- Consulta local del contenido mediante un servidor MCP.
- Observación y mantenimiento editorial de las fuentes.

### No incluido

- Publicación automática de newsletters sin aprobación editorial humana.
- Envío automático de newsletters desde tareas programadas.
- Scraping HTML de fuentes sin RSS o endpoint estable.
- Uso de `Article` o `NewsArticle` para noticias externas.
- Incorporación indiscriminada de nuevas fuentes sin validación técnica y editorial.

## 4. Estado actual

- La web pública, el aula, las fichas docentes, la newsletter y los recursos SEO están funcionando.
- El pipeline diario está automatizado en el VPS mediante systemd y publica cambios de `docs/` desde `main`.
- La generación quincenal crea un borrador privado; revisión, publicación y envío son decisiones manuales independientes.
- La migración operativa al VPS y su documentación están terminadas.
- La fase v0.8 de revisión de fuentes está completada; continúa la observación posterior identificada como v0.9.
- El informe del 2026-07-27 presenta estado AMARILLO, sin alertas críticas, con cuatro avisos y una recomendación.
- Permanecen 2 noticias sin resultado de aprendizaje y 2 sin conceptos clave.
- `ecommerce-news.es` concentra el 67,3 % del histórico clasificado.
- Seis fuentes activas no tienen aportación histórica y requieren revisión basada en datos.
- Las 3 pruebas existentes del lanzador de newsletters pasan correctamente.

## 5. Fase actual

- **Fase:** v0.9 · Estabilización, observabilidad editorial y mantenimiento operativo.
- **Estado de la fase:** En curso.
- **Resultado esperado de la fase:** Confirmar la utilidad y estabilidad de las fuentes activas, vigilar la concentración editorial y mantener el pipeline sin alertas críticas.

## 6. Próxima acción

- **Siguiente acción concreta:** Revisar las seis fuentes activas sin aportación histórica con los informes recientes y documentar si están correctamente configuradas, son de baja frecuencia o deben mantenerse en observación.
- **Responsable:** Creador y autor.
- **Condición para considerarla terminada:** Existe una decisión verificable por cada fuente basada en datos recientes, sin activar ni desactivar fuentes de forma automática.
- **Fecha prevista:** 2026-08-11.

## 7. Próximas tareas

| Prioridad | Tarea | Estado | Responsable | Dependencia | Fecha |
|---|---|---|---|---|---|
| media | Revisar las seis fuentes activas sin aportación histórica | pendiente | Creador y autor | Informes recientes del pipeline | 2026-08-11 |
| media | Revisar las 2 noticias sin RA y las 2 noticias sin conceptos clave | pendiente | Creador y autor | Datos procesados actuales | Pendiente de confirmar |
| baja | Seguir observando la concentración de `ecommerce-news.es` | en curso | Creador y autor | Nuevas ejecuciones con noticias | 2026-08-11 |

## 8. Bloqueos y riesgos

| Tipo | Descripción | Impacto | Acción prevista |
|---|---|---|---|
| riesgo potencial | Dependencia editorial elevada de `ecommerce-news.es`, con un 67,3 % del histórico clasificado | Reduce la diversidad de contenidos | Observar nuevas ejecuciones y evaluar las fuentes activas |
| riesgo potencial | Seis fuentes activas todavía no aportan contenido histórico | Pueden no mejorar la diversidad esperada | Comprobar configuración, frecuencia y utilidad editorial |
| deuda técnica | Existen 2 noticias sin RA y 2 sin conceptos clave | Calidad docente incompleta en casos puntuales | Revisar los registros afectados |
| dependencia externa | El pipeline depende del VPS, la VPN y el acceso privado a Ollama | Una incidencia puede detener la publicación diaria | Mantener preflight, logs y procedimientos de recuperación |
| dependencia externa | La publicación web depende de GitHub Pages y el envío de Mailgun | Puede afectar a publicación o distribución | Mantener validación y autorización manual |

No se han localizado bloqueos actuales ni alertas críticas.

## 9. Decisiones importantes

| Fecha | Decisión | Motivo | Consecuencia |
|---|---|---|---|
| 2026-07-07 | No representar noticias externas como `Article` ni `NewsArticle` | El sitio agrega, selecciona y contextualiza noticias que no publica como propias | Se usan colecciones y listas en los datos estructurados |
| 2026-07-09 | Corregir feeds válidos y desactivar temporalmente fuentes no fiables | Mejorar diversidad sin introducir scraping frágil | La v0.8 mantiene solo fuentes procesables de forma estable |
| 2026-07-18 | Introducir pesos para equilibrar las fuentes | Reducir la concentración editorial | El agregador calcula cupos por fuente |
| 2026-07-24 | Separar generación, aprobación, publicación y envío de newsletters | Evitar publicaciones o envíos no autorizados | Los borradores quedan privados y Mailgun requiere confirmación explícita |
| 2026-07-24 | Trasladar la operación principal al VPS con systemd | Centralizar y estabilizar la automatización | Las tareas equivalentes de Windows permanecen desactivadas |

## 10. Entregables

| Entregable | Estado | Ubicación | Observaciones |
|---|---|---|---|
| Web pública | completada | `docs/` y https://comerciodigital.net | Se actualiza mediante el pipeline diario |
| Página de aula | completada | `docs/aula.html` | Generada por el pipeline |
| Fichas docentes | completada | `docs/fichas-aula/` y `outputs/aula/` | 10 fichas HTML y 10 MD en el informe del 2026-07-27 |
| Newsletters públicas | completada | `docs/newsletter/` | 3 ediciones HTML y 3 MD detectadas |
| Servidor MCP local | completada | `mcp_servers/comercio_digital/` | Consulta local de contenidos |
| Automatización del VPS | completada | `deploy/systemd/` | Pipeline diario y borrador quincenal |
| Documentación operativa | completada | `OPERACION_VPS.md` | Procedimientos de operación y recuperación |

## 11. Tecnología e infraestructura

- **Lenguajes:** Python, HTML, CSS y shell.
- **Frameworks:** No localizado.
- **Base de datos:** No localizada; se utilizan archivos JSON y salidas estáticas.
- **Alojamiento:** VPS para ejecución y GitHub Pages para la web pública.
- **Dominio o URL:** https://comerciodigital.net
- **Repositorio:** https://github.com/juaarbla/comercio-digital
- **Despliegue:** Pipeline diario mediante systemd, con publicación de cambios de `docs/` desde `main`.
- **Servicios externos:** Ollama o Anthropic, Mailgun, GitHub Pages, Google Search Console y Bing Webmaster Tools.
- **Entorno local:** Python con entorno virtual; ejecución documentada para Windows y operación principal en Linux/VPS.

## 12. Rutas y enlaces importantes

| Recurso | Ubicación |
|---|---|
| Repositorio | https://github.com/juaarbla/comercio-digital |
| Documentación | `README.md`, `DIARIO_PROYECTO.md`, `OPERACION_VPS.md` y `_documentacion/` |
| Producción | https://comerciodigital.net |
| Pruebas | `tests/` |
| Copias de seguridad | `data/backups/`; las copias externas se describen sin ubicación en `OPERACION_VPS.md` |

## 13. Validación y calidad

- El pipeline genera un informe diario en `logs/informe_pipeline_YYYY-MM-DD.md`.
- Se comprueba la existencia de portada, aula, índice de newsletter y CSS principal.
- Existen 3 pruebas automatizadas para el lanzador quincenal de newsletters; pasan a fecha 2026-07-27.
- Antes de publicar una newsletter se revisan contenido, enlaces, fechas, imágenes, accesibilidad y aspecto HTML.
- Antes de preparar una publicación se revisan el estado de Git, el diff y `git diff --check`.
- El envío por Mailgun requiere una vista previa y dos opciones explícitas de confirmación.
- Criterios operativos actuales: pipeline sin alertas críticas, web generada correctamente y contenidos con clasificación y utilidad docente.
- Problemas conocidos: avisos puntuales de calidad docente, concentración histórica de una fuente y fuentes activas sin aportación.

## 14. Últimos avances

| Fecha | Avance |
|---|---|
| 2026-07-27 | Actualización diaria de la web publicada desde el pipeline. |
| 2026-07-26 | Documentación de la operación del VPS integrada en `main`. |
| 2026-07-24 | Migración operativa al VPS integrada en `main`. |
| 2026-07-24 | Preflight de Ollama reforzado y bloqueo de automatizaciones corregido. |
| 2026-07-24 | Flujo privado y seguro de borradores de newsletter implantado. |
| 2026-07-24 | Newsletter de julio Q2 publicada. |
| 2026-07-19 | Fuente Todo Digital incorporada y MaxMaxData evaluada sin incorporación. |
| 2026-07-18 | Pesos por fuente añadidos para mejorar el equilibrio editorial. |

## 15. Historial de actualizaciones del estado

| Fecha | Cambio en el estado | Próxima acción acordada |
|---|---|---|
| 2026-07-27 | Creación del resumen operativo; proyecto activo, automatizado en VPS y en fase de observación editorial v0.9 | Revisar las fuentes activas sin aportación histórica antes del 2026-08-11 |

## Reglas de mantenimiento

1. Actualizar `updated_at` después de cada sesión relevante.
2. Registrar únicamente avances reales y verificables.
3. Mantener una única próxima acción principal.
4. Marcar los bloqueos de forma explícita.
5. No borrar decisiones históricas importantes.
6. Mover las tareas terminadas al historial cuando dejen de ser útiles en la tabla activa.
7. No incluir secretos.
8. Mantener la información breve, operativa y verificable.

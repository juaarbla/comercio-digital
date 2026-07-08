# ROADMAP v0.7 · Actualización Bloque 7

## Tarea complementaria · Alta en buscadores

Estado: completado.

Acciones realizadas:

```text
- Sitio dado de alta en Google Search Console.
- Sitio dado de alta en Bing Webmaster Tools.
- Sitemap disponible para rastreo:
  https://comerciodigital.net/sitemap.xml
```

Objetivo:

```text
Empezar a recoger datos reales de rastreo, indexación, cobertura y rendimiento orgánico tras la incorporación progresiva de datos estructurados Schema.org.
```

Queda para una fase posterior:

```text
- Revisar cobertura de indexación.
- Revisar páginas descubiertas/no indexadas.
- Revisar errores de sitemap si aparecen.
- Valorar IndexNow para Bing si aporta valor.
```

---

## Bloque 7 · Schema para newsletter

Estado: preparado para implementación.

### Objetivo

Añadir datos estructurados JSON-LD a la newsletter generada en:

```text
docs/newsletter/index.html
docs/newsletter/newsletter-AAAA-MM-QX.html
```

### Enfoque

La newsletter se describe como una colección editorial de enlaces seleccionados, no como un conjunto de noticias propias.

Schemas previstos:

```text
CollectionPage
ItemList
ListItem
```

### Criterio editorial

Se mantiene la decisión tomada en el Bloque 6:

```text
No usar Article ni NewsArticle para noticias externas.
```

Motivo:

```text
Las noticias proceden de fuentes externas. Comercio Digital actúa como agregador educativo, curador y generador de contexto docente.
```

### Archivos implicados

```text
schema_utils.py
generar_newsletter.py
docs/newsletter/index.html
docs/newsletter/newsletter-*.html
```

### Cambios previstos en schema_utils.py

Añadir:

```text
- schema_newsletter_index()
- schema_newsletter_issue()
- _newsletter_item()
```

### Cambios previstos en generar_newsletter.py

Añadir:

```text
- import de insertar_jsonld
- import de schema_newsletter_index
- import de schema_newsletter_issue
- inserción de JSON-LD en render_index()
- inserción de JSON-LD en render_html()
```

### Fuera de alcance

```text
- No tocar sitemap recursivo.
- No tocar canonical en subcarpetas.
- No añadir Open Graph a newsletter.
- No marcar noticias externas como Article/NewsArticle.
- No modificar la selección editorial de newsletter.
```

### Validación

Ejecutar:

```powershell
python .\generar_newsletter.py
```

Comprobar índice:

```powershell
Select-String -Path .\docs\newsletter\index.html -Pattern "application/ld+json","CollectionPage","ItemList"
```

Comprobar edición:

```powershell
Select-String -Path .\docs\newsletter\newsletter-*.html -Pattern "application/ld+json","CollectionPage","ItemList","ListItem"
```

Resultado esperado:

```text
El índice de newsletter contiene CollectionPage.
Las ediciones individuales contienen CollectionPage e ItemList.
Las noticias incluidas se describen como ListItem, no como NewsArticle.
```

---

# Bloque final · Validación y cierre v0.7

Estado: completado.

## Objetivo

Cerrar la fase **v0.7 · SEO semántico y datos estructurados Schema.org** tras validar el pipeline, la generación web y la incorporación progresiva de JSON-LD en las páginas previstas.

## Bloques completados

```text
✅ Bloque 1 · Roadmap v0.7
✅ Bloque 2 · Diagnóstico SEO actual
✅ Bloque 3 · schema_utils.py
✅ Bloque 4 · Schema básico en portada
✅ Bloque 4b · Schema básico en páginas principales
✅ Bloque 6 · LearningResource en fichas de aula
✅ Tarea complementaria · Alta en Google Search Console y Bing Webmaster Tools
✅ Bloque 7 · Schema para newsletter
✅ Bloque final · Validación y cierre
```

## Implementación Schema.org realizada

### Portada

```text
docs/index.html
```

Schemas incorporados:

```text
Organization
WebSite
CollectionPage
```

### Páginas principales

```text
docs/comercio-electronico.html
docs/internacional.html
docs/digitalizacion.html
docs/ia-marketing.html
docs/aula.html
docs/del-autor.html
```

Schemas incorporados:

```text
CollectionPage
WebPage
```

### Fichas de aula

```text
docs/fichas-aula/*.html
```

Schema incorporado:

```text
LearningResource
```

### Newsletter

```text
docs/newsletter/index.html
docs/newsletter/newsletter-*.html
```

Schemas incorporados:

```text
CollectionPage
ItemList
ListItem
```

## Decisiones editoriales documentadas

### No usar Article / NewsArticle para noticias externas

Se decide no marcar las noticias enlazadas como `Article` ni `NewsArticle` propio.

Motivo:

```text
Comercio Digital no publica la noticia original completa.
El sitio actúa como agregador educativo, curador y generador de contexto docente.
```

En su lugar se utilizan:

```text
CollectionPage
ItemList
ListItem
LearningResource para fichas propias
```

## Alta en buscadores

Estado: completado.

```text
Google Search Console: completado
Bing Webmaster Tools: completado
Sitemap: https://comerciodigital.net/sitemap.xml
```

## Informe post-pipeline de cierre

Fecha del informe:

```text
2026-07-07 21:56:24
```

Estado general:

```text
AMARILLO
```

Lectura:

```text
El sistema funciona correctamente, pero mantiene avisos no bloqueantes.
```

Resumen:

```text
Noticias resumidas: 282
Noticias clasificadas: 282
Fuentes configuradas: 19
Fuentes activas: 14
Fuentes inactivas: 5
Registros en historial: 241
Fichas HTML generadas: 10
Fichas MD generadas: 10
Newsletters HTML disponibles: 2
Newsletters MD disponibles: 2
Alertas críticas: 0
Avisos: 5
Recomendaciones: 1
```

Archivos clave detectados correctamente:

```text
Portada: OK
Aula: OK
Índice newsletter: OK
CSS principal: OK
```

## Avisos no bloqueantes

El informe mantiene avisos relacionados con:

```text
- 2 noticias sin RA asignado.
- 2 noticias sin conceptos clave.
- Concentración histórica de ecommerce-news.es.
- Concentración de ecommerce-news.es en la última ejecución.
- Fuentes activas sin aportación en la última ejecución.
```

Estos avisos no bloquean el cierre de la v0.7 porque no corresponden al objetivo principal de la fase, centrado en Schema.org y SEO semántico.

## Recomendación trasladada

Se traslada a una fase posterior:

```text
v0.8 · Revisión de fuentes, diversidad y aportación editorial
```

Objetivo previsto:

```text
Revisar fuentes activas sin aportación histórica, concentración de fuentes y diversidad editorial del agregador.
```

## Criterios de cierre

```text
✅ Pipeline ejecutado.
✅ Informe post-pipeline generado.
✅ Sin alertas críticas.
✅ JSON-LD validado en portada.
✅ JSON-LD validado en páginas principales.
✅ LearningResource validado en fichas de aula.
✅ CollectionPage / ItemList validado en newsletter.
✅ NewsArticle ausente en newsletter y noticias externas.
✅ Search Console y Bing dados de alta.
✅ Documentación actualizada.
```

## Estado final

```text
v0.7 cerrada con avisos no bloqueantes.
```

## Comandos de cierre recomendados

```powershell
git status
git add _documentacion/ROADMAP_v0.7.md DIARIO_PROYECTO.md README.md
git commit -m "Documenta cierre v0.7 SEO semántico"
git push origin main
git status
git tag v0.7
git push origin v0.7
```

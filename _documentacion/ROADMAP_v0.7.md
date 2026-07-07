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

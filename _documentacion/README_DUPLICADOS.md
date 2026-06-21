# Control de duplicados

Este documento recoge el criterio usado para evitar duplicados en el agregador, especialmente en la sección `Del Autor`.

## Problema detectado

Algunos artículos propios podían entrar duplicados porque llegaban por varias vías:

- RSS de categorías de WordPress;
- WordPress API;
- feed del podcast.

Esto provocaba que la misma publicación apareciera más de una vez en la web.

## Decisión aplicada

Se mantiene activo:

```text
https://juanarmada.com/podcast/feed/
https://juanarmada.com/wp-json/wp/v2/posts?...
```

Se desactivan como fuentes principales:

```text
https://juanarmada.com/inteligencia-artificial/feed/
https://juanarmada.com/marketing-digital/feed/
```

Motivo:

```text
WordPress API ya permite recuperar artículos propios de forma más controlada.
```

## Script relacionado

```text
limpiar_duplicados.py
```

## Limpieza de duplicados existentes

```powershell
python limpiar_duplicados.py
```

## Regeneración posterior

```powershell
python run_pipeline.py
```

## Publicación

```powershell
git status
git add feeds.json limpiar_duplicados.py docs/
git commit -m "Evita duplicados en Del Autor"
git push
```

## Comprobaciones recomendadas

Buscar títulos repetidos en las páginas generadas:

```powershell
Select-String -Path docs\del-autor.html -Pattern "juanarmada.com"
```

Comprobar también que las noticias propias siguen apareciendo:

```powershell
start docs\del-autor.html
```

## Criterio futuro

Si se añaden nuevas fuentes propias, revisar antes si ya están cubiertas por WordPress API para evitar duplicados desde el origen.

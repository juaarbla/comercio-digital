# Parche duplicados Del Autor

Causa: los artículos propios podían entrar por el RSS de categoría y por WordPress API.

Se mantiene activo:
- `https://juanarmada.com/podcast/feed/`
- `https://juanarmada.com/wp-json/wp/v2/posts?...`

Se desactivan:
- `https://juanarmada.com/inteligencia-artificial/feed/`
- `https://juanarmada.com/marketing-digital/feed/`

## Instalar

```powershell
copy feeds.json feeds.json
copy limpiar_duplicados.py limpiar_duplicados.py
```

## Limpiar duplicados existentes

```powershell
python limpiar_duplicados.py
```

## Regenerar

```powershell
python run_pipeline.py
```

## Publicar

```powershell
git add feeds.json limpiar_duplicados.py docs/
git commit -m "Evita duplicados en Del Autor"
git push
```

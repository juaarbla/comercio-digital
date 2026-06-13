# Aula v3.2 integrada con `style.css`

Esta versión de `generar_aula.py` genera `docs/aula.html` usando la hoja de estilos principal del sitio.

## Ventaja

No incrusta un diseño nuevo en `aula.html`. Usa las clases ya existentes del agregador:

- `masthead`
- `site-title`
- `subtitle-bar`
- `container`
- `sec-header`
- `seccion-lista`
- `noticia-full`
- `cat-badge`
- `ra-badge`
- `fecha`
- `docente-box`
- `concepto-chip`

## Uso

```powershell
python generar_aula.py --max-noticias 25
```

## CSS utilizado

`docs/aula.html` enlaza con:

```html
<link rel="stylesheet" href="assets/style.css">
```

Por tanto, debe existir:

```text
docs/assets/style.css
```

## Comprobación rápida

```powershell
Select-String -Path docs\aula.html -Pattern "assets/style.css"
Select-String -Path docs\aula.html -Pattern "<style>"
```

Resultado esperado:

```text
assets/style.css  → aparece
<style>           → no aparece
```

## Publicación

```powershell
git add generar_aula.py docs/aula.html
git commit -m "Integra aula con el estilo principal"
git push
```

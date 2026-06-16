# Parche final: favicon y diseño de fichas

Este parche no sustituye tus archivos completos. Aplica cambios puntuales sobre la versión actual del proyecto.

## Qué hace

- Crea `docs/assets/favicon.svg` si no existe.
- Añade favicon a `generar_aula.py`.
- Añade favicon a `generar_fichas_aula.py`.
- Mejora el diseño visual de las fichas docentes.
- Añade estilos nuevos a `docs/assets/style.css`.

## Instalar

Copia el script a la raíz del proyecto:

```powershell
copy aplicar_parche_final_fichas.py aplicar_parche_final_fichas.py
```

Ejecuta:

```powershell
python aplicar_parche_final_fichas.py
```

Regenera:

```powershell
python generar_fichas_aula.py --max-fichas 10 --limpiar
python generar_aula.py --max-noticias 25
python generar_seo.py
```

Comprueba:

```powershell
Select-String -Path docs\aula.html -Pattern "favicon.svg"
Select-String -Path docs\fichas-aula\*.html -Pattern "favicon.svg"
Test-Path docs\assets\favicon.svg
```

Publica:

```powershell
git add docs/ generar_aula.py generar_fichas_aula.py aplicar_parche_final_fichas.py
git commit -m "Mejora favicon y diseño de fichas docentes"
git push
```

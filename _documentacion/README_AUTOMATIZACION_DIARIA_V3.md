# Automatizacion publicacion diaria v3

Corrige el error de codificacion provocado por emojis en `run_pipeline.py`.

## Cambio principal

Anade al BAT:

```bat
chcp 65001 >nul
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
```

## Instalar

```powershell
copy publicar_web_diaria.bat publicar_web_diaria.bat
```

## Probar

```powershell
.\publicar_web_diaria.bat
```

## Ver log

```powershell
notepad logs\publicacion_diaria.log
```

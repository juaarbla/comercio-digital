# Instalación y publicación rápida

## 1. Abrir proyecto

```powershell
cd "C:\Users\Juan\Google Drive\00_CDI_press"
```

## 2. Activar entorno

El entorno virtual se guarda fuera de Google Drive:

```text
%LOCALAPPDATA%\PythonVenvs\comercio-digital
```

Desde VS Code debe seleccionarse:

```text
C:\Users\Juan\AppData\Local\PythonVenvs\comercio-digital\Scripts\python.exe
```

## 3. Ejecutar panel

```powershell
.\arrancar.bat
```

Opción recomendada:

```text
2. Proceso completo + publicar SOLO web docs/
```

## 4. Ejecución manual equivalente

```powershell
python run_pipeline.py
git add docs/
git commit -m "Actualiza web"
git push
```

## 5. Si también cambian scripts y documentación

```powershell
git add docs/ *.py *.md arrancar.bat
git commit -m "Actualiza proyecto"
git push
```

## 6. Comprobaciones tras publicar

```text
https://comerciodigital.net
https://comerciodigital.net/aula.html
https://comerciodigital.net/sitemap.xml
https://comerciodigital.net/robots.txt
```

## 7. Comprobaciones locales útiles

```powershell
Select-String -Path docs\index.html -Pattern "aula.html"
Select-String -Path docs\aula.html -Pattern "Descargar Markdown"
Select-String -Path docs\aula.html -Pattern "Descargar material de aula MD"
Select-String -Path docs\*.html -Pattern "autor.html"
Test-Path docs\fichas-aula\material-aula.md
```

`autor.html` no debe aparecer. La página correcta es `del-autor.html`.

# Instalación, generación y publicación

Guía rápida para ejecutar el agregador de Comercio Digital y publicar los resultados en GitHub Pages.

## 1. Requisitos

- Windows con PowerShell.
- Python 3.12 o compatible.
- Git instalado.
- Repositorio local del proyecto.
- Entorno virtual fuera de Google Drive.

## 2. Entorno virtual

El entorno virtual se mantiene fuera de Google Drive para evitar problemas de sincronización.

Ruta recomendada:

```text
%LOCALAPPDATA%\PythonVenvs\comercio-digital\
```

Ejemplo en el equipo principal:

```text
C:\Users\Juan\AppData\Local\PythonVenvs\comercio-digital\
```

Activación manual:

```powershell
& "$env:LOCALAPPDATA\PythonVenvs\comercio-digital\Scripts\Activate.ps1"
```

Comprobación:

```powershell
python -c "import sys; print(sys.executable)"
```

Debe apuntar al entorno virtual externo, no al Python global.

## 3. Ejecución recomendada

Ejecutar el flujo completo:

```powershell
python run_pipeline.py
```

También puede usarse el panel:

```powershell
.\arrancar.bat
```

## 4. Ejecución manual por partes

```powershell
python news_aggregator.py
python clasificador_ra.py
python enriquecer_docente.py --forzar
python imagen_destacada.py
python generar_web.py
python generar_fichas_aula.py --max-fichas 10 --limpiar
python generar_aula.py --max-noticias 25
python generar_newsletter.py --periodicidad quincenal --force
python generar_seo.py
```

## 5. Newsletter

La newsletter se genera solo cuando se ejecuta el script.

Quincenal:

```powershell
python generar_newsletter.py --periodicidad quincenal --force
```

Semanal:

```powershell
python generar_newsletter.py --periodicidad semanal --force
```

Archivos generados:

```text
docs/newsletter/index.html
docs/newsletter/newsletter-AAAA-WSS.html
docs/newsletter/newsletter-AAAA-WSS.md
```

## 6. Comprobaciones locales

Abrir páginas principales:

```powershell
start docs\index.html
start docs\aula.html
start docs\newsletter\index.html
```

Comprobaciones rápidas:

```powershell
Test-Path docs\index.html
Test-Path docs\aula.html
Test-Path docs\newsletter\index.html
Test-Path docs\fichas-aula\material-aula.md
Test-Path docs\sitemap.xml
Test-Path docs\robots.txt
Select-String -Path docs\newsletter\*.html -Pattern "newsletter-card"
Select-String -Path docs\*.html -Pattern "newsletter/index.html"
```

## 7. Publicar en GitHub Pages

```powershell
git status
git add docs/ README.md DIARIO_PROYECTO.md _documentacion/
git add *.py feeds.json paths.py arrancar.bat
git commit -m "Actualiza agregador de Comercio Digital"
git push
```

Si solo se actualiza la newsletter:

```powershell
git status
git add docs/newsletter docs/assets/style.css generar_newsletter.py
git commit -m "Publica newsletter docente"
git push
```

## 8. Revisar en la web pública

```text
https://comerciodigital.net
https://comerciodigital.net/aula.html
https://comerciodigital.net/newsletter/
```

## 9. Envío de newsletter por email

El agregador no envía correos ni gestiona suscriptores.

Procedimiento recomendado:

1. Generar newsletter.
2. Publicarla en GitHub Pages.
3. Comprobar que se ve bien.
4. Crear un correo breve en Gmail o herramienta externa.
5. Incluir el enlace a la newsletter.
6. Enviar primero una prueba.
7. Enviar al grupo reducido.

Herramientas posibles:

- Gmail para pruebas internas.
- Brevo o MailerLite para listas sencillas.
- Mailchimp si se necesita una herramienta más conocida.
- Substack si se quiere una publicación externa con suscriptores.
- Mailgun si se decide automatizar desde scripts.

## 10. Problemas habituales

### El entorno no se activa en VS Code

Comprobar el intérprete seleccionado y confirmar:

```powershell
python -c "import sys; print(sys.executable)"
```

### Aparecen problemas de acentos en `.bat`

Mantener estas líneas al inicio del BAT:

```bat
chcp 65001 >nul
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
```

### El comando `mcp` no se reconoce

No es obligatorio tener `mcp` en el PATH global. Para MCP Inspector se puede configurar directamente el Python del entorno virtual y el script del servidor.

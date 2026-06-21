# Automatización y publicación del agregador

Este documento recoge el criterio actual de automatización del proyecto.

## Decisión actual

El pipeline general puede ejecutarse completo, pero la newsletter se mantiene como acción manual o semimanual.

Motivos:

- la newsletter no debe generarse todos los días;
- funciona mejor como selección curada semanal o quincenal;
- la distribución por correo se realizará con herramienta externa;
- el agregador no gestionará suscriptores ni envíos;
- conviene revisar la edición antes de compartirla.

## Pipeline general

```powershell
python run_pipeline.py
```

El pipeline genera la web pública en:

```text
docs/
```

## Ejecución desde panel

También puede ejecutarse desde:

```powershell
.\arrancar.bat
```

El panel debe usar el entorno virtual externo del proyecto.

## Generación manual de newsletter

Quincenal:

```powershell
python generar_newsletter.py --periodicidad quincenal --force
```

Semanal:

```powershell
python generar_newsletter.py --periodicidad semanal --force
```

## Orden recomendado cuando se quiere publicar newsletter

```powershell
python run_pipeline.py
python generar_newsletter.py --periodicidad quincenal --force
python generar_seo.py
```

Si `run_pipeline.py` ya incluye newsletter, revisar igualmente la edición antes de publicar.

## Publicación en GitHub Pages

```powershell
git status
git add docs/ generar_newsletter.py
git commit -m "Publica actualización del agregador"
git push
```

## Comprobaciones

```powershell
Test-Path docs\index.html
Test-Path docs\aula.html
Test-Path docs\newsletter\index.html
Test-Path docs\sitemap.xml
Test-Path docs\robots.txt
Select-String -Path docs\newsletter\*.html -Pattern "newsletter-card"
Select-String -Path docs\*.html -Pattern "newsletter/index.html"
```

## Envío por correo

El envío no se realiza desde Python.

Procedimiento recomendado:

1. Generar la newsletter.
2. Publicarla en GitHub Pages.
3. Abrir `https://comerciodigital.net/newsletter/`.
4. Crear un correo breve en Gmail, Brevo, Mailchimp, Substack, MailerLite u otra herramienta.
5. Incluir el enlace público.
6. Enviar primero una prueba al propio correo.
7. Enviar al grupo reducido.

## Nota de codificación en Windows

Si se usa un `.bat`, mantener:

```bat
chcp 65001 >nul
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
```

## Criterio futuro

Automatizar más solo cuando el flujo manual esté validado. Primero interesa calidad de selección; después, automatización.

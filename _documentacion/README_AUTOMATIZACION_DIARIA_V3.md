# Automatización y publicación del agregador

Este documento recoge el criterio actual de automatización del proyecto.

## Decisión actual

El pipeline general puede ejecutarse de forma completa, pero la newsletter se mantiene como una acción manual o semimanual.

Motivo:

- la newsletter no debe generarse todos los días;
- debe funcionar como selección curada semanal o quincenal;
- la distribución por correo se realizará con una herramienta externa;
- el agregador no gestionará suscriptores ni envíos.

## Pipeline general

```powershell
python run_pipeline.py
```

El pipeline genera la web pública en:

```text
docs/
```

## Generación manual recomendada de newsletter

Quincenal:

```powershell
python generar_newsletter.py --periodicidad quincenal --force
```

Semanal:

```powershell
python generar_newsletter.py --periodicidad semanal --force
```

## Publicación en GitHub Pages

```powershell
git status
git add docs/ generar_newsletter.py
git commit -m "Publica newsletter docente"
git push
```

## Comprobaciones

```powershell
Test-Path docs\newsletter\index.html
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
7. Enviar a la lista de destinatarios.

## Nota de codificación en Windows

Si se usa un `.bat`, mantener:

```bat
chcp 65001 >nul
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
```

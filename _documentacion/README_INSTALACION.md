# Instalación, generación y publicación

Guía rápida para ejecutar el agregador de Comercio Digital y publicar los resultados en GitHub Pages.

## 1. Activar entorno

El entorno virtual se mantiene fuera de Google Drive para evitar problemas de sincronización.

Ejemplo:

```powershell
C:\Users\Juan\AppData\Local\PythonVenvs\comercio-digital\Scripts\Activate.ps1
```

## 2. Ejecutar flujo completo

```powershell
python run_pipeline.py
```

También puede usarse el panel:

```powershell
.\arrancar.bat
```

## 3. Ejecución manual por partes

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

## 4. Newsletter

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

## 5. Comprobaciones locales

```powershell
start docs\index.html
start docs\aula.html
start docs\newsletter\index.html
```

Comprobaciones rápidas:

```powershell
Test-Path docs\newsletter\index.html
Test-Path docs\fichas-aula\material-aula.md
Select-String -Path docs\newsletter\*.html -Pattern "newsletter-card"
Select-String -Path docs\*.html -Pattern "newsletter/index.html"
```

## 6. Publicar en GitHub Pages

```powershell
git status
git add docs/ generar_web.py generar_aula.py generar_fichas_aula.py generar_newsletter.py
git commit -m "Actualiza agregador y newsletter docente"
git push
```

## 7. Revisar en la web pública

```text
https://comerciodigital.net
https://comerciodigital.net/aula.html
https://comerciodigital.net/newsletter/
```

## 8. Envío de newsletter por email

El agregador no envía correos ni gestiona suscriptores.

Procedimiento recomendado:

1. Generar newsletter.
2. Publicarla en GitHub Pages.
3. Comprobar que se ve bien.
4. Crear un correo breve en una herramienta externa.
5. Incluir el enlace a la newsletter.
6. Enviar primero una prueba.
7. Enviar a destinatarios.

Herramientas posibles:

- Gmail para pruebas internas.
- Brevo o MailerLite para listas sencillas.
- Mailchimp si se necesita una herramienta más conocida.
- Substack si se quiere una publicación externa con suscriptores.

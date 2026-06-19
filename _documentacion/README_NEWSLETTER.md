# Newsletter docente

La newsletter es una salida periódica del agregador `Comercio Digital`.

Su objetivo es convertir la actualidad clasificada en una selección breve y útil para compartir con docentes o usar directamente en clase.

## Qué genera

`generar_newsletter.py` crea:

```text
docs/newsletter/index.html
docs/newsletter/newsletter-AAAA-WSS.html
docs/newsletter/newsletter-AAAA-WSS.md
```

Ejemplo:

```text
docs/newsletter/newsletter-2026-W25.html
docs/newsletter/newsletter-2026-W25.md
```

## Qué no hace

La newsletter no envía correos.

El agregador no gestiona:

- suscriptores;
- bajas;
- listas de distribución;
- campañas de email;
- métricas de apertura.

La distribución se hace con una herramienta externa o de forma manual.

## Periodicidad

La newsletter no se genera cada día.

Uso recomendado:

```powershell
python generar_newsletter.py --periodicidad quincenal --force
```

También se puede generar semanalmente:

```powershell
python generar_newsletter.py --periodicidad semanal --force
```

## Criterios de selección

El script prioriza noticias con:

```text
seleccion_newsletter = true
valor_docente = alto
```

También tiene en cuenta el valor docente, el tipo de uso y la información disponible.

## Relación con Aula y fichas

```text
Aula            → banco de noticias útiles para clase
Fichas docentes → material individual HTML/Markdown
Newsletter      → selección periódica para compartir
```

Cuando existe ficha docente, la newsletter enlaza a:

```text
docs/fichas-aula/
```

Por eso se recomienda generar primero las fichas:

```powershell
python generar_fichas_aula.py --max-fichas 10 --limpiar
python generar_aula.py --max-noticias 25
python generar_newsletter.py --periodicidad quincenal --force
python generar_seo.py
```

## Publicación

Tras generar la newsletter:

```powershell
git status
git add docs/newsletter docs/assets/style.css generar_newsletter.py
git commit -m "Publica newsletter docente"
git push
```

Comprobar:

```text
https://comerciodigital.net/newsletter/
```

## Envío por Gmail

1. Generar la newsletter.
2. Publicar en GitHub Pages.
3. Abrir `https://comerciodigital.net/newsletter/`.
4. Crear un correo nuevo.
5. Escribir un texto breve.
6. Incluir el enlace.
7. Enviar primero una prueba al propio correo.
8. Enviar a destinatarios.

Modelo de correo:

```text
Asunto: Comercio Digital en el aula · Selección quincenal

Hola,

Ya está disponible una nueva selección de noticias de Comercio Digital para trabajar en clase.

Incluye noticias relacionadas con comercio electrónico, digitalización, marketing digital e inteligencia artificial aplicada al comercio, junto con propuestas de uso docente y enlaces a fichas de aula.

Puedes verla aquí:

https://comerciodigital.net/newsletter/

Un saludo,
Juan
```

## Envío con herramienta externa

Herramientas posibles:

- Brevo;
- Mailchimp;
- MailerLite;
- Substack;
- Buttondown.

Procedimiento:

1. Crear una lista o audiencia.
2. Crear una campaña.
3. Escribir una introducción breve.
4. Añadir 3 titulares destacados si se desea.
5. Incluir botón o enlace a la newsletter publicada.
6. Enviar prueba.
7. Enviar campaña.

Recomendación inicial:

```text
No copiar todo el HTML de la newsletter en el email.
Enviar un correo breve con enlace a la edición publicada.
```

## Enfoque recomendado

Empezar con periodicidad quincenal y distribución manual o semimanual.

Después de varias ediciones, valorar si merece la pena crear una lista pública de suscripción con una herramienta externa.

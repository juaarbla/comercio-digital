# Newsletter docente

La newsletter es una salida periódica del agregador `Comercio Digital`. Convierte noticias clasificadas y enriquecidas en una selección breve para compartir con docentes, departamentos o grupos de prueba.

## Objetivo

La newsletter sirve para distribuir una selección curada de actualidad relacionada con:

- comercio electrónico;
- digitalización;
- marketing digital;
- inteligencia artificial aplicada al comercio;
- casos reales útiles para clase.

No sustituye a Aula. Aula es el banco de recursos; la newsletter es una selección periódica para compartir.

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

El agregador no envía correos y no gestiona:

- suscriptores;
- bajas;
- listas de distribución;
- campañas de email;
- métricas de apertura;
- cumplimiento legal de campañas externas.

La distribución se realiza con Gmail, Brevo, Mailchimp, MailerLite, Substack, Mailgun u otra herramienta externa.

## Periodicidad recomendada

La recomendación actual es empezar con periodicidad quincenal.

```powershell
python generar_newsletter.py --periodicidad quincenal --force
```

También se puede generar semanalmente:

```powershell
python generar_newsletter.py --periodicidad semanal --force
```

La newsletter no se genera todos los días. Solo se crea cuando se ejecuta el script.

## Criterios de selección

El script prioriza noticias con:

```text
seleccion_newsletter = true
valor_docente = alto
```

También tiene en cuenta:

- tipo de uso;
- módulo relacionado;
- existencia de ficha docente;
- calidad del resumen;
- utilidad para abrir debate o actividad.

## Relación con Aula y fichas

```text
Aula            → banco de noticias útiles para clase
Fichas docentes → material individual HTML/Markdown
Newsletter      → selección periódica para compartir
```

## Relación con podcast

La newsletter puede actuar como selección editorial base para otros formatos, incluido el podcast `comercIAaliza.online`.

Para evitar acoplar proyectos, el agregador no genera audio. Genera un brief Markdown reutilizable:

```powershell
python .\generar_brief_newsletter.py --periodicidad quincenal
```

Tambien existe un lanzador para uso manual o Programador de tareas:

```powershell
generar_brief_podcast.bat
```

Salida esperada:

```text
outputs/podcast/podcast-brief-AAAA-MM-QN.md
```

Ese archivo puede revisarse manualmente y usarse como entrada en el proyecto de podcast. La idea es que ComercioDigital.net seleccione y contextualice noticias; el proyecto de podcast decide tono, guion final, locución y audio.

Cuando existe ficha docente, la newsletter puede enlazar a:

```text
docs/fichas-aula/
```

Por eso se recomienda este orden:

```powershell
python generar_fichas_aula.py --max-fichas 10 --limpiar
python generar_aula.py --max-noticias 25
python generar_newsletter.py --periodicidad quincenal --force
python generar_seo.py
```

## Publicación

Después de generar la newsletter:

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

## Distribución inicial recomendada

Fase inicial:

```text
1. Enviar primero al propio correo.
2. Enviar después a un grupo reducido de profesorado.
3. Valorar claridad, utilidad y frecuencia.
4. Decidir si se abre una lista más amplia.
```

## Formulario de suscripción

En la fase actual, la captación de inscritos se realiza mediante Google Forms.

La URL del formulario se configura en `.env`:

```text
NEWSLETTER_SUBSCRIPTION_URL=https://forms.gle/...
```

El formulario puede enlazar a la política de privacidad pública:

```text
https://comerciodigital.net/privacidad.html
```

Si esa variable existe, el índice de newsletters y cada edición generada muestran un bloque breve con icono de sobre y enlace `Apúntate`.

El formulario debe volcar respuestas a Google Sheets. Cuando se vaya a enviar una campaña, exportar la hoja a CSV y guardarla fuera de Git:

```text
data/private/suscriptores_newsletter.csv
```

## Envío por Gmail

1. Generar la newsletter.
2. Publicar en GitHub Pages.
3. Abrir `https://comerciodigital.net/newsletter/`.
4. Crear un correo nuevo.
5. Escribir un texto breve.
6. Incluir el enlace.
7. Enviar primero una prueba al propio correo.
8. Enviar al grupo reducido.

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
- Buttondown;
- Mailgun si se integra desde scripts propios.

Recomendación inicial:

```text
No copiar todo el HTML de la newsletter dentro del email.
Enviar un correo breve con enlace a la edición publicada.
```

## Posible evolución con Mailgun

Mailgun se usa como canal de distribución desde scripts propios. La integración queda separada de la generación de la newsletter.

Uso prudente:

```text
- empezar con cuenta propia;
- hacer pruebas con pocos destinatarios;
- gestionar la lista desde CSV privado exportado desde Google Forms o Google Sheets;
- separar generación de newsletter y envío por correo.
```

Documento específico:

```text
_documentacion/NEWSLETTER_ENVIO_MAILGUN.md
```

Prueba sin envío real:

```powershell
python .\enviar_newsletter_mailgun.py --test tu-correo@example.com
```

Estado:

```text
Validado envío real individual con Mailgun EU y mg.comerciodigital.net.
```

## Decisión actual

```text
El agregador genera la newsletter y puede preparar el envío por Mailgun.
El envío real requiere confirmación explícita con --send --yes.
```

La lista de inscritos se mantiene fuera de Git y debe revisarse antes de cada envío.

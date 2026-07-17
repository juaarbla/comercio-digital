# Envío de newsletter con Mailgun

## Decisión

La newsletter publicada en `docs/newsletter/` sigue siendo el contenido canónico.

Mailgun se usa solo como canal de distribución por correo:

```text
newsletter web publicada → email breve con enlace → lista de inscritos
```

No se copia todo el HTML de la newsletter dentro del email.

## Estado actual

```text
Fase: validada con envío real individual
Envío real: solo con confirmación explícita
Lista: CSV privado exportado desde Google Forms o Google Sheets
```

Validación realizada:

```text
2026-07-17: envío real de prueba correcto a un destinatario propio.
Dominio de envío: mg.comerciodigital.net
Región: Mailgun EU
```

## Archivos

```text
enviar_newsletter_mailgun.py
enviar_newsletter_mailgun.bat
data/private/suscriptores_newsletter.csv
logs/newsletter_mailgun.log
templates/email/newsletter_mailgun.txt
templates/email/newsletter_mailgun.html
```

`data/private/` está excluido de Git.

## Variables de entorno

Copiar `env.example` como `.env` y completar:

```text
MAILGUN_API_KEY=
MAILGUN_API_BASE=https://api.eu.mailgun.net
MAILGUN_DOMAIN=mg.comerciodigital.net
MAILGUN_FROM="ComercioDigital.net <newsletter@mg.comerciodigital.net>"
MAILGUN_REPLY_TO=
NEWSLETTER_BASE_URL=https://comerciodigital.net/newsletter/
NEWSLETTER_SUBSCRIPTION_URL=
NEWSLETTER_SITE_NAME=Comercio Digital
NEWSLETTER_UNSUBSCRIBE_TEXT=
```

No guardar nunca `MAILGUN_API_KEY` en Git.

El dominio de Mailgun debe ser el subdominio `mg.comerciodigital.net`, no el dominio raíz `comerciodigital.net`.

## CSV de suscriptores

La captación inicial se realiza con Google Forms enlazado desde la zona de newsletter de la web.

La URL pública del formulario se configura en `.env`:

```text
NEWSLETTER_SUBSCRIPTION_URL=https://forms.gle/...
```

El formulario debe enlazar a:

```text
https://comerciodigital.net/privacidad.html
```

Ruta recomendada:

```text
data/private/suscriptores_newsletter.csv
```

Columnas recomendadas:

```text
email,nombre,consentimiento,activo
```

Reglas:

- `email` es obligatorio.
- `nombre` es opcional.
- `consentimiento` puede dejarse vacío si la lista ya procede de un formulario con consentimiento.
- `activo` permite excluir bajas con valores como `no`, `false`, `baja` o `inactivo`.

## Prueba sin envío

```powershell
python .\enviar_newsletter_mailgun.py --test tu-correo@example.com
```

o:

```powershell
enviar_newsletter_mailgun.bat --test tu-correo@example.com
```

Esto valida la última newsletter publicada y prepara el envío, pero no envía nada.

## Contenido del email

El cuerpo del correo se edita en plantillas:

```text
templates/email/newsletter_mailgun.txt
templates/email/newsletter_mailgun.html
```

Variables disponibles:

```text
{{site_name}}
{{url}}
{{unsubscribe}}
```

Previsualizar sin enviar:

```powershell
python .\enviar_newsletter_mailgun.py --preview
```

## Envío real de prueba

```powershell
python .\enviar_newsletter_mailgun.py --test tu-correo@example.com --send --yes
```

## Envío real a la lista

```powershell
python .\enviar_newsletter_mailgun.py --send --yes
```

Antes de usar este comando:

1. Generar la newsletter.
2. Publicarla en la web.
3. Comprobar la URL pública.
4. Revisar el CSV de inscritos.
5. Ejecutar primero una prueba a un solo correo.

## Baja

En esta fase la baja es semimanual:

```text
Para dejar de recibir esta newsletter, responde a este correo con BAJA.
```

La baja debe reflejarse en el CSV antes del siguiente envío.

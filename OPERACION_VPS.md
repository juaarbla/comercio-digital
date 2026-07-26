# Operación del VPS

Esta guía describe el estado operativo de Comercio Digital tras su migración
al VPS. No contiene direcciones, endpoints, correos, secretos ni valores de
`.env`; los datos locales necesarios están en el manual privado ignorado.

El VPS es el entorno principal de producción y `main` es la rama operativa. Los
dos timers de Comercio Digital y `openvpn3-session@ausias.service` están
habilitados y validados después de reinicio.

## Arquitectura resumida

- systemd programa el pipeline diario y la generación quincenal del borrador.
- `openvpn3-session@ausias.service` mantiene una única VPN para el acceso
  privado a Ollama; SSH utiliza la interfaz pública.
- el pipeline valida Ollama con reintentos, actualiza `main`, genera la web y
  publica únicamente cambios de `docs/`.
- la newsletter automática solo crea un borrador privado `PENDIENTE`.
- pipeline y newsletter comparten un bloqueo para impedir solapamientos.
- revisar/corregir el borrador, aprobar/publicar y autorizar el envío por
  Mailgun son tres decisiones manuales separadas.
- el CSV de destinatarios y Mailgun están disponibles en el VPS, siempre como
  recursos privados; ninguno se incorpora al repositorio.

## Tareas automáticas

| Tarea | Horario (`Europe/Madrid`) | Resultado |
| --- | --- | --- |
| Pipeline y web | todos los días, 08:00 | Ejecuta pipeline e informe; publica `docs/` si todo termina correctamente. |
| Borrador de newsletter | días 1 y 16, 08:45 | Crea un borrador privado pendiente; no publica ni envía. |

Las tareas programadas equivalentes de Windows están desactivadas. No deben
reactivarse mientras systemd sea el planificador de producción.

## Comprobar la ejecución diaria

Desde la raíz del repositorio en el VPS:

```bash
systemctl list-timers --all 'comercio-digital-*'
systemctl is-enabled comercio-digital-pipeline.timer comercio-digital-newsletter.timer
systemctl status comercio-digital-pipeline.timer comercio-digital-pipeline.service
systemctl show comercio-digital-pipeline.service -p Result -p ExecMainStatus -p ExecMainExitTimestamp
journalctl -u comercio-digital-pipeline.service --since today
tail -n 100 logs/publicacion_diaria.log
.venv/bin/python scripts/comprobar_ollama.py
git status --short --branch
```

`systemctl show` permite comprobar la última ejecución y su código;
`systemctl list-timers --all` muestra la activación anterior y la próxima.
También deben revisarse la duración, el resultado del preflight y, si hubo
cambios, el commit/push indicado en el log.
Un servicio `inactive (dead)` puede ser normal para una unidad `oneshot`; lo
importante es `Result=success` y un código 0 en la última ejecución.

## Revisar una newsletter pendiente

La consulta es de solo lectura y no envía nada:

```bash
scripts/estado_newsletter.sh
```

Si el estado es `PENDIENTE`, revisar localmente todos los ficheros enumerados
en `data/private/newsletter_pendiente/archivos/`: contenido, enlaces, fechas,
imágenes, accesibilidad y aspecto HTML. El borrador es privado y no debe
compartirse ni añadirse a Git.

## Tres decisiones manuales sobre la newsletter

### 1. Revisar y corregir el borrador

Revisar los tres ficheros enumerados por `metadata.json`. Las correcciones se
hacen únicamente en el área privada pendiente y deben volver a revisarse; no
implican aprobación, publicación ni envío. No existe un script que apruebe o
publique borradores.

### 2. Aprobar y publicar

La aprobación es una decisión editorial humana. Una vez registrada, la
promoción de los tres ficheros desde
`data/private/newsletter_pendiente/archivos/` a `docs/newsletter/` es un
procedimiento asistido por Codex, no un comando ni un script existente. Debe
solicitarse expresamente a Codex, con el árbol limpio y en una rama de trabajo.
Después se revisa antes de preparar cambios:

```bash
git status --short
git diff -- docs/newsletter/
git diff --check
```

Preparar, confirmar y fusionar la publicación sigue el flujo Git habitual y
requiere una revisión humana distinta de la aprobación editorial. Comprobar la
página publicada antes de considerar la edición lista para distribución. No se
debe cambiar el estado ni borrar el borrador antes de completar esta
comprobación. El timer no realiza ninguno de estos pasos.

### 3. Autorizar y ejecutar el envío Mailgun

Mailgun se ejecuta siempre manualmente, después de verificar que la edición ya
está publicada. La vista previa no envía:

```bash
.venv/bin/python enviar_newsletter_mailgun.py --preview
```

El envío real requiere las dos opciones de confirmación explícita:

```bash
.venv/bin/python enviar_newsletter_mailgun.py --send --yes
```

El CSV privado y la configuración Mailgun residen en el VPS, pero no se
versionan. Antes de autorizar el envío, verificar edición, asunto, URL pública
y destinatarios por el procedimiento privado. La autorización del envío es una
decisión explícita independiente de la aprobación/publicación. No incluir
correos ni la salida de `--list` en incidencias o documentación. Mailgun nunca
se ejecuta desde timers.

## Trabajo desde el PC

1. Abrir VS Code y usar **Remote - SSH: Connect to Host…** con el alias privado
   configurado en el PC.
2. Abrir en remoto la ruta del repositorio indicada en el manual privado.
3. Confirmar host y rama con `hostname` y `git status --short --branch` sin
   copiar datos sensibles a documentación pública.
4. Editar y ejecutar comandos en la terminal remota del VPS; no mantener otra
   copia ejecutando automatizaciones.

Para actualizar una copia local de trabajo, situarse en su rama principal con
el árbol limpio y ejecutar:

```bash
git pull --ff-only origin main
```

No usar `pull` para ocultar cambios locales: revisarlos o guardarlos primero.

## Recuperación básica

- **VPN:** mantener abierto SSH público, revisar estado y journal de
  `openvpn3-session@ausias.service`, confirmar una sola sesión y seguir
  `deploy/systemd/VPN_PERSISTENCIA.md`. Detener el timer del pipeline durante
  una reversión.
- **Ollama:** revisar el servicio de Ollama en su equipo, la VPN y el preflight.
  No lanzar el pipeline hasta que el preflight vuelva a código 0.
- **Git:** revisar rama, `git status` y remoto. Resolver un árbol sucio o una
  divergencia manualmente; no usar reset destructivo. El publicador exige
  `main`, árbol limpio y pull fast-forward.
- **Pipeline:** revisar journal y `logs/publicacion_diaria.log`. Los cambios
  locales tras un fallo se conservan para diagnóstico; no relanzar hasta
  entender el código de salida.
- **Mailgun:** detenerse ante cualquier error, revisar
  `logs/newsletter_mailgun.log` y configuración sin imprimir secretos. No
  repetir un envío si no se ha confirmado si el anterior llegó a aceptarse.

## Copias de seguridad

Respaldar cifrados y con acceso restringido los datos ignorados que no puedan
reconstruirse: `.env`, `data/private/`, `data/backups/`, datos de suscriptores,
estado editorial pendiente y cualquier dato operativo local. No incluir claves
SSH privadas en estas copias del proyecto. Probar periódicamente la
restauración y conservar al menos una copia fuera del VPS.

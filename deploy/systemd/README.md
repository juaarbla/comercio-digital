# Automatización systemd de Comercio Digital

El VPS es el entorno principal de producción y `main` es su rama operativa.
Las unidades de este directorio están instaladas en el VPS y han sido
validadas, incluido su funcionamiento después de un reinicio. Los dos timers y
la unidad VPN están habilitados (`enabled`). Los archivos versionados son la
referencia que debe mantenerse sincronizada con las copias instaladas por el
administrador en systemd.

## Unidades y horarios

- `comercio-digital-pipeline.timer`: ejecución diaria a las 08:00,
  explícitamente en `Europe/Madrid`.
- `comercio-digital-newsletter.timer`: generación de borrador los días 1 y 16
  a las 08:45, también en `Europe/Madrid`.
- `openvpn3-session@ausias.service`: mantiene la única sesión VPN necesaria
  para llegar a Ollama.

Los timers son persistentes: si el VPS estaba apagado a la hora prevista,
systemd programa la ejecución pendiente al volver a estar disponible.

## Pipeline diario

`comercio-digital-pipeline.service` ejecuta
`scripts/publicar_web_diaria.sh`. El lanzador:

1. adquiere el bloqueo compartido;
2. valida el entorno, Git y los archivos requeridos;
3. ejecuta el preflight de Ollama antes de modificar datos;
4. en ejecución normal, exige `main` y un árbol limpio, y actualiza mediante
   `git pull --ff-only origin main`;
5. repite el preflight de Ollama;
6. ejecuta el pipeline y el informe;
7. prepara exclusivamente `docs/`, crea un commit y hace push solo si existen
   cambios preparados.

El preflight `scripts/comprobar_ollama.py` valida el túnel, la ruta, la API y
el modelo configurado. Hace tres intentos, con cinco segundos entre intentos,
para absorber retrasos de la VPN o de Ollama. Si no supera la comprobación, el
pipeline se detiene antes del pull y antes de modificar datos.

El modo `scripts/publicar_web_diaria.sh --no-publish` existe para diagnóstico:
no hace pull, `git add`, commit ni push. No debe lanzarse mientras el timer o
la newsletter estén trabajando.

## Newsletter quincenal

`comercio-digital-newsletter.service` ejecuta
`scripts/generar_newsletter_quincenal.sh`. Genera un borrador privado con
estado `PENDIENTE` en `data/private/newsletter_pendiente/`, ruta ignorada por
Git y protegida con permisos restrictivos. El borrador nunca se sobrescribe y
requiere revisión y aprobación manual.

Este timer no modifica `docs/`, no prepara cambios, no crea commits, no publica
y no ejecuta Mailgun. Aprobar, publicar y enviar son operaciones manuales y
separadas. Mailgun nunca se ejecuta desde ninguno de los timers.

El CSV privado de destinatarios y la integración Mailgun están presentes en
el VPS. Ambos permanecen privados: el CSV está dentro de `data/private/`, las
credenciales están fuera de Git y el envío exige autorización manual explícita.

El estado se consulta sin generar ni enviar nada:

```bash
scripts/estado_newsletter.sh
```

## Bloqueo compartido

Los dos lanzadores usan el mismo bloqueo no bloqueante:

```text
PROJECT_DIR/.runtime/comercio-digital.lock
```

El descriptor permanece abierto durante toda la operación. Si el pipeline y
la newsletter coinciden, la segunda operación no espera y termina con código
75. `.runtime/` y `logs/` están ignorados por Git; los servicios aplican además
`UMask=0077`.

## Estado y logs

Comandos de solo lectura:

```bash
systemctl status comercio-digital-pipeline.timer comercio-digital-newsletter.timer
systemctl is-enabled comercio-digital-pipeline.timer comercio-digital-newsletter.timer
systemctl status comercio-digital-pipeline.service comercio-digital-newsletter.service
systemctl status openvpn3-session@ausias.service
systemctl list-timers --all 'comercio-digital-*'
systemctl show comercio-digital-pipeline.service -p Result -p ExecMainStatus -p ExecMainExitTimestamp
journalctl -u comercio-digital-pipeline.service --since today
journalctl -u comercio-digital-newsletter.service --since today
journalctl -u openvpn3-session@ausias.service -b
tail -n 100 logs/publicacion_diaria.log
tail -n 100 logs/newsletter_quincenal.log
.venv/bin/python scripts/comprobar_ollama.py
git status --short --branch
```

`systemctl show` muestra el resultado, código y fecha de la última ejecución;
`list-timers --all` muestra las activaciones anterior y próxima. El journal
recoge el ciclo de systemd y los logs locales conservan inicio, duración y
código de salida del lanzador. El preflight es una comprobación de diagnóstico:
no ejecuta el pipeline ni publica contenido.

Códigos relevantes:

- `0`: operación completada; también puede significar que no había cambios
  que publicar o que no existe newsletter pendiente al consultar su estado.
- `1`: error general, dependencia ausente, preflight fallido o configuración
  no válida.
- `2`: el directorio de newsletter existe pero su estado está incompleto.
- `64`: uso incorrecto de argumentos del lanzador diario.
- `65`: el borrador generado no superó su validación interna.
- `74`: el árbol Git no estaba limpio o fue alterado al generar el borrador.
- `75`: otra operación mantiene el bloqueo compartido.
- `76`: ya existe o apareció otro borrador pendiente.
- cualquier otro valor del pipeline o del informe se conserva como código de
  salida y debe investigarse en los logs.

No se deben usar los comandos anteriores para deducir ni publicar valores de
`.env`, direcciones privadas, endpoints, destinatarios o credenciales.

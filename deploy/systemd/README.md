# Borradores systemd para Comercio Digital

Estos archivos son borradores versionables. En la Fase 3 no se copian a
`/etc/systemd/system`, no se ejecuta `daemon-reload` y no se activa ningún
servicio o timer.

## Flujo diario

`comercio-digital-pipeline.timer` programa el servicio todos los días a las
08:00, interpretadas explícitamente en `Europe/Madrid`. El servicio ejecuta el
lanzador Linux como `depinf`.

El lanzador:

1. adquiere su bloqueo exclusivo;
2. valida archivos, rama y árbol Git limpio;
3. comprueba `tun0`, la ruta privada, `/api/tags` y `CHAT_MODEL`;
4. actualiza `main` con `git pull --ff-only`;
5. repite el preflight de Ollama antes del pipeline;
6. ejecuta el pipeline y el informe;
7. prepara exclusivamente `docs/`;
8. crea commit y hace push solo si hay cambios preparados.

El preflight de Ollama detiene la ejecución antes de que el pipeline modifique
datos cuando la VPN, el endpoint o el modelo no están disponibles.

El argumento `--no-publish` habilita el modo de prueba: permite ejecutar el
pipeline y el informe desde una rama de preparación, pero omite pull,
preparación del índice, commit y push. Los cambios quedan locales para
inspección y se conserva el código real de salida del pipeline.

## Flujo quincenal

El timer propone los días 1 y 16 a las 08:45. El lanzador exige primero un
árbol Git limpio y genera la quincena en el directorio local ignorado
`data/private/newsletter_pendiente/`. No modifica `docs/`, no prepara cambios,
no crea commits, no publica y no ejecuta Mailgun.

Si ya existe un borrador `PENDIENTE`, el lanzador no lo sobrescribe: informa
del conflicto y termina con código 76. El estado editorial se consulta con:

```bash
scripts/estado_newsletter.sh
```

La revisión se realiza abriendo los archivos enumerados dentro de
`data/private/newsletter_pendiente/archivos/`. Una fase posterior deberá
incorporar una orden explícita y separada para aprobar y publicar el borrador.
Hasta entonces no existe aprobación automática ni envío por Mailgun. Como el
borrador permanece en una ruta ignorada, el pipeline diario puede seguir
exigiendo un árbol limpio y ejecutarse mientras la revisión está pendiente.

## Logs y bloqueo

Los dos lanzadores escriben en `logs/`, que está excluido de Git, y comparten
exactamente el mismo bloqueo:

```text
PROJECT_DIR/.runtime/comercio-digital.lock
```

Cada lanzador crea `PROJECT_DIR/.runtime/` si es necesario, aplica permisos
`0700`, abre el lock sin truncarlo y lo adquiere con `flock -n`. El descriptor
permanece abierto durante preflight, pipeline o newsletter, informe y
operaciones Git. Cualquier segunda operación, aunque sea del otro tipo, no
espera: informa del conflicto y termina con código 75. `.runtime/` está
excluido de Git y los servicios usan además `UMask=0077`.

## Dependencia de VPN

En la Fase 3 no se inicia ni reinicia la VPN. El pipeline falla de forma segura
si Ollama no está accesible. El servicio diario declara `Wants=` y `After=`
respecto de `openvpn3-session@ausias.service`; si el borrador se instala y se
inicia en una fase posterior, systemd intentará iniciar primero esa unidad. La
dependencia solo será utilizable después de preparar la ACL y transición
descritas en `VPN_PERSISTENCIA.md`. Antes de instalar o probar el servicio
diario debe completarse la persistencia de OpenVPN.

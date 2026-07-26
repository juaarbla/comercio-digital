# Persistencia de OpenVPN 3

## Estado final

La transición a una sesión gestionada por systemd está completada. La unidad
`openvpn3-session@ausias.service` está habilitada y fue validada después de un
reinicio controlado. El VPS mantiene una única sesión VPN; no debe iniciarse
otra sesión manual en paralelo.

El túnel se usa únicamente para alcanzar el servicio privado requerido por el
pipeline. SSH continúa entrando y saliendo por la interfaz pública del VPS. No
se documentan aquí direcciones, rutas privadas, endpoints, perfiles ni
credenciales.

`comercio-digital-pipeline.service` declara `Wants=` y `After=` sobre la unidad
VPN. La dependencia es deliberadamente débil: si la VPN no queda operativa, el
preflight de Ollama termina con error antes del pull y antes de modificar
datos.

## Diagnóstico seguro

Estas comprobaciones no muestran secretos ni el contenido del perfil:

```bash
systemctl is-enabled openvpn3-session@ausias.service
systemctl status openvpn3-session@ausias.service
journalctl -u openvpn3-session@ausias.service -b
openvpn3 sessions-list
ip link show tun0
```

La comprobación de ruta no se construye manualmente en esta guía para evitar
exponer el destino. En la operación normal se usa
`scripts/comprobar_ollama.py`, que obtiene la configuración local y valida la
ruta completa con reintentos sin imprimir secretos.

Resultados esperados:

1. la unidad figura como `enabled` y `active (running)`;
2. `openvpn3 sessions-list` muestra una sola sesión correspondiente al perfil
   operativo;
3. `tun0` existe;
4. la ruta privada usa el túnel;
5. el preflight termina con código 0;
6. una sesión SSH abierta por la interfaz pública permanece conectada.

No se debe ejecutar el preflight durante esta revisión documental ni copiar su
salida si contiene datos operativos.

## Reversión controlada

La reversión debe hacerse desde una ventana con dos sesiones SSH públicas
abiertas:

1. detener el timer del pipeline para evitar una ejecución durante el cambio;
2. detener y deshabilitar `openvpn3-session@ausias.service`;
3. comprobar que no quedan sesiones duplicadas;
4. recuperar temporalmente la conexión mediante el procedimiento privado del
   administrador;
5. verificar primero SSH público y después el acceso privado;
6. corregir la causa, restaurar una única sesión gestionada por systemd y
   validar de nuevo tras reinicio antes de reactivar el timer.

Comandos de reversión, que requieren privilegios y confirmación del
administrador:

```bash
sudo systemctl stop comercio-digital-pipeline.timer
sudo systemctl disable --now openvpn3-session@ausias.service
openvpn3 sessions-list
```

No se debe borrar el perfil ni modificar su ACL como parte de una recuperación
básica. Si falla la reversión, se mantiene detenido el timer y se revisan el
journal y el procedimiento privado sin exponer información sensible.

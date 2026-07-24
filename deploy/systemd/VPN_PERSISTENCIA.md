# Propuesta de persistencia de OpenVPN 3

## Estado observado

- OpenVPN 3 Linux v27.1 está instalado.
- El perfil importado se llama `ausias` y es persistente.
- La sesión actual está conectada mediante `tun0`.
- `openvpn3-autoload.service` existe, pero la propia herramienta indica que
  está deprecada desde OpenVPN 3 Linux v20.
- La instalación proporciona `openvpn3-session@.service`, que es el mecanismo
  recomendado para una sesión gestionada por systemd.

No se ha modificado el perfil, la ACL, la sesión ni ningún servicio.

## Propuesta

Usar la unidad instalada:

```text
openvpn3-session@ausias.service
```

Antes de activarla, un administrador debe revisar y conceder a root acceso
limitado al perfil importado. La documentación de OpenVPN recomienda configurar
la ACL del perfil, opcionalmente bloquear la extracción de su contenido y
transferir la propiedad de la sesión al usuario operativo cuando proceda.

Comandos propuestos para una fase posterior, no ejecutados:

```bash
openvpn3 config-acl --show --config ausias
sudo openvpn3 config-acl \
  --config ausias \
  --grant root \
  --lock-down true \
  --transfer-owner-session true
sudo systemctl enable openvpn3-session@ausias.service
```

Como la sesión actual se inició manualmente, no debe usarse `--now` ni arrancar
la unidad mientras siga conectada: eso podría intentar crear una sesión
duplicada. La transición debe programarse en una ventana controlada, manteniendo
dos sesiones SSH.

El borrador `comercio-digital-pipeline.service` declara `Wants=` y `After=`
sobre esa unidad. Cuando la transición esté completada, un arranque manual o
programado del pipeline pedirá a systemd que inicie primero la sesión VPN. La
dependencia es deliberadamente débil: si OpenVPN falla, el servicio del pipeline
continúa hasta su preflight y termina de forma segura con un error explícito, sin
pull ni modificación de datos.

## Validación antes de activar el pipeline

En una fase posterior:

1. validar la ACL sin mostrar el perfil;
2. habilitar la unidad sin `--now` mientras exista la sesión manual;
3. verificar la unidad y su comportamiento tras un reinicio controlado;
4. confirmar una única sesión `ausias`;
5. confirmar que la ruta hacia Ollama usa el túnel;
6. ejecutar `scripts/comprobar_ollama.py`;
7. comprobar que SSH y los servicios públicos siguen accesibles.

El preflight del pipeline exige que exista `tun0`, que la ruta al host privado
use esa interfaz, que `/api/tags` responda y que `CHAT_MODEL` esté disponible.
Si cualquiera de esas condiciones falla, el servicio termina con código
distinto de cero antes del pull y antes de modificar datos.

El timer del pipeline no debe activarse hasta superar estas pruebas.

## Recuperación propuesta

Si la unidad no restaura la VPN tras el reinicio:

```bash
sudo systemctl disable openvpn3-session@ausias.service
```

Después se recuperaría temporalmente la conexión manual siguiendo el
procedimiento operativo existente en `/home/depinf/vpn-ausias/`, sin modificar
el perfil ni exponerlo.

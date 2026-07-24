#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_DIR="$(cd -- "${SCRIPT_DIR}/.." && pwd -P)"
PYTHON="${PROJECT_DIR}/.venv/bin/python"
ENV_FILE="${PROJECT_DIR}/.env"
NEWSLETTER_SCRIPT="${PROJECT_DIR}/generar_newsletter.py"
LOG_DIR="${PROJECT_DIR}/logs"
LOG_FILE="${LOG_DIR}/newsletter_quincenal.log"
LOCK_FILE="${PROJECT_DIR}/.runtime/comercio-digital.lock"
START_EPOCH="$(date +%s)"
START_TEXT="$(date --iso-8601=seconds)"

if ! command -v flock >/dev/null 2>&1; then
    printf 'ERROR: flock no está disponible.\n' >&2
    exit 1
fi

mkdir -p -- "${PROJECT_DIR}/.runtime"
chmod 700 -- "${PROJECT_DIR}/.runtime"
exec 9>>"${LOCK_FILE}"
if ! flock -n 9; then
    printf 'ERROR: otra operación de Comercio Digital está activa; no se genera la newsletter.\n' >&2
    exit 75
fi

mkdir -p -- "${LOG_DIR}"
touch -- "${LOG_FILE}"
chmod 600 -- "${LOG_FILE}"
exec > >(tee -a "${LOG_FILE}") 2>&1

on_error() {
    local line="$1"
    local status="$2"
    printf 'ERROR: fallo en la línea %s (código %s).\n' "${line}" "${status}"
}

on_exit() {
    local status="$?"
    local end_epoch
    local duration

    end_epoch="$(date +%s)"
    duration="$((end_epoch - START_EPOCH))"
    printf 'Finalización: %s\n' "$(date --iso-8601=seconds)"
    printf 'Duración: %s segundos\n' "${duration}"
    printf 'Código de salida: %s\n' "${status}"
}

trap 'on_error "${LINENO}" "$?"' ERR
trap on_exit EXIT

printf '\n============================================================\n'
printf 'Inicio newsletter quincenal: %s\n' "${START_TEXT}"
printf 'Proyecto: %s\n' "${PROJECT_DIR}"

cd -- "${PROJECT_DIR}"

if [[ ! -d "${PROJECT_DIR}/.venv" ]]; then
    printf 'ERROR: no existe el entorno virtual .venv/.\n'
    exit 1
fi

for required_file in "${PYTHON}" "${ENV_FILE}" "${NEWSLETTER_SCRIPT}"; do
    if [[ ! -f "${required_file}" ]]; then
        printf 'ERROR: falta un archivo requerido: %s\n' "${required_file#${PROJECT_DIR}/}"
        exit 1
    fi
done

if [[ ! -x "${PYTHON}" ]]; then
    printf 'ERROR: .venv/bin/python no es ejecutable.\n'
    exit 1
fi
printf 'Generando newsletter; no se enviará ni publicará automáticamente.\n'
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 \
    "${PYTHON}" "${NEWSLETTER_SCRIPT}" \
    --periodicidad quincenal \
    --force

printf '\nCambios dejados para revisión editorial:\n'
git status --short -- docs/newsletter/
git diff --stat -- docs/newsletter/
printf 'Newsletter generada y dejada sin preparar ni publicar.\n'

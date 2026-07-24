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
PENDING_PARENT="${PROJECT_DIR}/data/private"
PENDING_DIR="${PENDING_PARENT}/newsletter_pendiente"
TEMP_DIR=""
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

cleanup_temp_dir() {
    if [[ -z "${TEMP_DIR}" || ! -e "${TEMP_DIR}" ]]; then
        return
    fi
    case "${TEMP_DIR}" in
        "${PENDING_PARENT}"/.newsletter_pendiente.tmp.*)
            rm -rf -- "${TEMP_DIR}"
            ;;
        *)
            printf 'ERROR: se rechaza limpiar una ruta temporal inesperada.\n'
            ;;
    esac
}

on_exit() {
    local status="$?"
    local end_epoch
    local duration

    set +e
    cleanup_temp_dir
    end_epoch="$(date +%s)"
    duration="$((end_epoch - START_EPOCH))"
    printf 'Finalización: %s\n' "$(date --iso-8601=seconds)"
    printf 'Duración: %s segundos\n' "${duration}"
    printf 'Código de salida: %s\n' "${status}"
    trap - EXIT
    exit "${status}"
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

if [[ -n "$(git status --porcelain --untracked-files=normal)" ]]; then
    printf 'ERROR: el árbol Git debe estar limpio antes de generar el borrador.\n'
    exit 74
fi

if [[ -e "${PENDING_DIR}" ]]; then
    printf 'ERROR: ya existe un borrador o estado pendiente en %s.\n' \
        "${PENDING_DIR#${PROJECT_DIR}/}"
    printf 'Revísalo antes de generar una nueva edición.\n'
    exit 76
fi

mkdir -p -- "${PENDING_PARENT}"
chmod 700 -- "${PENDING_PARENT}"
TEMP_DIR="$(mktemp -d "${PENDING_PARENT}/.newsletter_pendiente.tmp.XXXXXX")"
TEMP_FILES_DIR="${TEMP_DIR}/archivos"
TEMP_METADATA_FILE="${TEMP_DIR}/metadata.json"
mkdir -p -- "${TEMP_FILES_DIR}"
chmod 700 -- "${TEMP_DIR}" "${TEMP_FILES_DIR}"

printf 'Generando borrador privado; no se enviará ni publicará automáticamente.\n'
set +e
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 \
    "${PYTHON}" "${NEWSLETTER_SCRIPT}" \
    --periodicidad quincenal \
    --output-dir "${TEMP_FILES_DIR}" \
    --metadata-file "${TEMP_METADATA_FILE}"
newsletter_status=$?
set -e

if (( newsletter_status != 0 )); then
    printf 'ERROR: la generación del borrador terminó con código %s.\n' \
        "${newsletter_status}"
    exit "${newsletter_status}"
fi

if ! "${PYTHON}" - "${TEMP_DIR}" <<'PY'
import json
import sys
from pathlib import Path

draft_dir = Path(sys.argv[1])
metadata_file = draft_dir / "metadata.json"
files_dir = draft_dir / "archivos"

try:
    metadata = json.loads(metadata_file.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError):
    raise SystemExit(1)

declared = metadata.get("archivos")
if (
    metadata.get("estado") != "PENDIENTE"
    or metadata.get("codigo_salida") != 0
    or not metadata.get("fecha_generacion")
    or not metadata.get("periodo")
    or not isinstance(declared, list)
):
    raise SystemExit(1)

declared_names = {str(name) for name in declared}
actual_names = {path.name for path in files_dir.iterdir() if path.is_file()}
html_issues = {name[:-5] for name in declared_names if name.startswith("newsletter-") and name.endswith(".html")}
markdown_issues = {name[:-3] for name in declared_names if name.startswith("newsletter-") and name.endswith(".md")}

if (
    len(declared) != 3
    or len(declared_names) != 3
    or declared_names != actual_names
    or "index.html" not in declared_names
    or len(html_issues) != 1
    or html_issues != markdown_issues
):
    raise SystemExit(1)
PY
then
    printf 'ERROR: el borrador generado no supera la validación interna.\n'
    exit 65
fi

chmod 600 -- "${TEMP_METADATA_FILE}"
find "${TEMP_FILES_DIR}" -maxdepth 1 -type f -exec chmod 600 -- {} +

if [[ -n "$(git status --porcelain --untracked-files=normal)" ]]; then
    printf 'ERROR: la generación alteró el árbol Git; no se considera válida.\n'
    exit 74
fi

if ! mv -T -- "${TEMP_DIR}" "${PENDING_DIR}" 2>/dev/null; then
    if [[ -e "${PENDING_DIR}" ]]; then
        printf 'ERROR: apareció otro borrador pendiente durante la generación.\n'
        exit 76
    fi
    printf 'ERROR: no se pudo promover el borrador validado.\n'
    exit 1
fi
TEMP_DIR=""

printf 'Borrador PENDIENTE generado en: %s\n' "${PENDING_DIR#${PROJECT_DIR}/}"
printf 'El árbol Git continúa limpio.\n'
printf 'No se ejecutó Mailgun ni se preparó o publicó ningún archivo.\n'

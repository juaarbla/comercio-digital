#!/usr/bin/env bash
set -Eeuo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
PROJECT_DIR="$(cd -- "${SCRIPT_DIR}/.." && pwd -P)"
PYTHON="${PROJECT_DIR}/.venv/bin/python"
ENV_FILE="${PROJECT_DIR}/.env"
LOG_DIR="${PROJECT_DIR}/logs"
LOG_FILE="${LOG_DIR}/publicacion_diaria.log"
LOCK_FILE="${PROJECT_DIR}/.runtime/comercio-digital.lock"
START_EPOCH="$(date +%s)"
START_TEXT="$(date --iso-8601=seconds)"
NO_PUBLISH=false

usage() {
    printf 'Uso: %s [--no-publish]\n' "$(basename -- "$0")"
}

case "${1:-}" in
    "")
        ;;
    --no-publish)
        NO_PUBLISH=true
        ;;
    -h|--help)
        usage
        exit 0
        ;;
    *)
        usage >&2
        exit 64
        ;;
esac

if (( $# > 1 )); then
    usage >&2
    exit 64
fi

if ! command -v flock >/dev/null 2>&1; then
    printf 'ERROR: flock no está disponible.\n' >&2
    exit 1
fi

mkdir -p -- "${PROJECT_DIR}/.runtime"
chmod 700 -- "${PROJECT_DIR}/.runtime"
exec 9>>"${LOCK_FILE}"
if ! flock -n 9; then
    printf 'ERROR: otra operación de Comercio Digital está activa; no se inicia el pipeline.\n' >&2
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
printf 'Inicio publicación diaria: %s\n' "${START_TEXT}"
printf 'Proyecto: %s\n' "${PROJECT_DIR}"
if [[ "${NO_PUBLISH}" == true ]]; then
    printf '*** MODO DE PRUEBA / NO PUBLISH ***\n'
    printf 'No se ejecutarán git add, commit ni push.\n'
fi

cd -- "${PROJECT_DIR}"

if [[ ! -d "${PROJECT_DIR}/.venv" ]]; then
    printf 'ERROR: no existe el entorno virtual .venv/.\n'
    exit 1
fi

required_files=(
    "${PYTHON}"
    "${ENV_FILE}"
    "${PROJECT_DIR}/run_pipeline.py"
    "${PROJECT_DIR}/generar_informe_pipeline.py"
    "${PROJECT_DIR}/scripts/comprobar_ollama.py"
)
for required_file in "${required_files[@]}"; do
    if [[ ! -f "${required_file}" ]]; then
        printf 'ERROR: falta un archivo requerido: %s\n' "${required_file#${PROJECT_DIR}/}"
        exit 1
    fi
done

if [[ ! -x "${PYTHON}" ]]; then
    printf 'ERROR: .venv/bin/python no es ejecutable.\n'
    exit 1
fi
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    printf 'ERROR: el directorio no es un repositorio Git.\n'
    exit 1
fi

printf 'Comprobando Ollama antes de cualquier actualización o pipeline...\n'
"${PYTHON}" "${PROJECT_DIR}/scripts/comprobar_ollama.py"

if [[ "${NO_PUBLISH}" == false ]]; then
    current_branch="$(git branch --show-current)"
    if [[ "${current_branch}" != "main" ]]; then
        printf 'ERROR: la publicación normal exige la rama main; rama actual: "%s".\n' \
            "${current_branch}"
        exit 1
    fi

    if [[ -n "$(git status --porcelain --untracked-files=normal)" ]]; then
        printf 'ERROR: el árbol de trabajo no está limpio antes de actualizar.\n'
        git status --short
        exit 1
    fi

    printf 'Actualizando main mediante fast-forward...\n'
    git pull --ff-only origin main

    printf 'Repitiendo preflight de Ollama antes del pipeline...\n'
    "${PYTHON}" "${PROJECT_DIR}/scripts/comprobar_ollama.py"
fi

printf 'Ejecutando pipeline...\n'
pipeline_started="$(date +%s)"
set +e
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 \
    "${PYTHON}" "${PROJECT_DIR}/run_pipeline.py"
pipeline_status="$?"
set -e
pipeline_duration="$(($(date +%s) - pipeline_started))"
printf 'Resultado del pipeline: código %s, duración %s segundos.\n' \
    "${pipeline_status}" "${pipeline_duration}"

printf 'Generando informe post-pipeline como diagnóstico best-effort...\n'
report_started="$(date +%s)"
set +e
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 \
    "${PYTHON}" "${PROJECT_DIR}/generar_informe_pipeline.py"
report_status="$?"
set -e
report_duration="$(($(date +%s) - report_started))"
if (( report_status == 0 )); then
    printf 'Informe generado correctamente en %s segundos.\n' "${report_duration}"
else
    printf 'AVISO: el informe falló con código %s tras %s segundos.\n' \
        "${report_status}" "${report_duration}"
fi

if (( pipeline_status != 0 )); then
    printf 'ERROR: run_pipeline.py terminó con código %s; no se publicará.\n' \
        "${pipeline_status}"
    printf '\nCambios locales conservados para diagnóstico:\n'
    git status --short
    git diff --stat
    exit "${pipeline_status}"
fi

if (( report_status != 0 )); then
    printf 'ERROR: el pipeline terminó correctamente, pero el informe es obligatorio para publicar.\n'
    exit "${report_status}"
fi

if [[ "${NO_PUBLISH}" == true ]]; then
    printf '\n*** MODO DE PRUEBA / NO PUBLISH: cambios locales para inspección ***\n'
    git status --short
    git diff --stat
    printf 'Pipeline e informe completados. No se preparó ni publicó ningún cambio.\n'
    exit "${pipeline_status}"
fi

printf 'Preparando exclusivamente docs/...\n'
git add -- docs/

printf '\nEstado Git:\n'
git status --short
printf '\nResumen preparado:\n'
git diff --cached --stat

if git diff --cached --quiet; then
    printf 'No hay cambios preparados en docs/. No se crea commit ni se hace push.\n'
    exit 0
fi

if git diff --cached --name-only | while IFS= read -r path; do
    [[ "${path}" == docs/* ]] || exit 1
done; then
    :
else
    printf 'ERROR: el índice contiene cambios fuera de docs/.\n'
    exit 1
fi

commit_message="Actualiza web diaria $(date +%F)"
git commit -m "${commit_message}"
commit_hash="$(git rev-parse --short HEAD)"
printf 'Commit creado: %s\n' "${commit_hash}"

git push origin main
printf 'Push completado para el commit %s.\n' "${commit_hash}"

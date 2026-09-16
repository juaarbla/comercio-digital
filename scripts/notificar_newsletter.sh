#!/usr/bin/env bash
set -Eeuo pipefail
PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
ENV_FILE="${PROJECT_DIR}/.env"
status="${1:-1}"; subject="${2:-Newsletter quincenal: resultado ${status}}"; body="${3:-Sin detalles adicionales.}"
[[ -f "${ENV_FILE}" ]] || exit 0
set -a; source "${ENV_FILE}"; set +a
[[ -n "${MAILGUN_API_KEY:-}" && -n "${MAILGUN_DOMAIN:-}" && -n "${MAILGUN_FROM:-}" && -n "${MAILGUN_ALERT_TO:-}" ]] || exit 0
api_base="${MAILGUN_API_BASE:-https://api.eu.mailgun.net}"; api_base="${api_base%/}"
curl --fail --silent --show-error --user "api:${MAILGUN_API_KEY}" --form-string "from=${MAILGUN_FROM}" --form-string "to=${MAILGUN_ALERT_TO}" --form-string "subject=${subject}" --form-string "text=${body}" "${api_base}/v3/${MAILGUN_DOMAIN}/messages" >/dev/null

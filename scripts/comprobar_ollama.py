#!/usr/bin/env python3
"""Preflight seguro de Ollama para los lanzadores Linux."""

from __future__ import annotations

import ipaddress
import json
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from dotenv import dotenv_values


TIMEOUT_SECONDS = 15
MAX_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 5
PRIVATE_NETWORKS = tuple(
    ipaddress.ip_network(network)
    for network in (
        "10.0.0.0/8",
        "172.16.0.0/12",
        "192.168.0.0/16",
        "100.64.0.0/10",
        "127.0.0.0/8",
        "fc00::/7",
        "::1/128",
    )
)


class PreflightError(Exception):
    """Fallo clasificado sin incluir direcciones ni datos de configuración."""

    def __init__(self, error_type: str, *, recoverable: bool) -> None:
        super().__init__(error_type)
        self.error_type = error_type
        self.recoverable = recoverable


def check_once() -> None:
    project_dir = Path(__file__).resolve().parent.parent
    env_file = project_dir / ".env"

    if not env_file.is_file():
        raise PreflightError("CONFIGURACION_LOCAL", recoverable=False)

    config = dotenv_values(env_file)
    base_url = (config.get("OLLAMA_BASE_URL") or "").strip().rstrip("/")
    chat_model = (config.get("CHAT_MODEL") or "").strip()

    if not base_url:
        raise PreflightError("CONFIGURACION_LOCAL", recoverable=False)
    if not chat_model:
        raise PreflightError("CONFIGURACION_LOCAL", recoverable=False)

    parsed = urllib.parse.urlparse(base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise PreflightError("CONFIGURACION_LOCAL", recoverable=False)

    try:
        addresses = {
            result[4][0]
            for result in socket.getaddrinfo(
                parsed.hostname,
                parsed.port or (443 if parsed.scheme == "https" else 80),
                type=socket.SOCK_STREAM,
            )
        }
    except socket.gaierror:
        raise PreflightError("DNS", recoverable=True) from None

    if not addresses or not all(
        any(ipaddress.ip_address(address) in network for network in PRIVATE_NETWORKS)
        for address in addresses
    ):
        raise PreflightError("CONFIGURACION_LOCAL", recoverable=False)

    if not Path("/sys/class/net/tun0").is_dir():
        raise PreflightError("RED_VPN", recoverable=True)

    try:
        route = subprocess.run(
            ["ip", "route", "get", parsed.hostname],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout.split()
    except (FileNotFoundError, subprocess.SubprocessError):
        raise PreflightError("RUTA", recoverable=True) from None

    try:
        route_device = route[route.index("dev") + 1]
    except (ValueError, IndexError):
        raise PreflightError("RUTA", recoverable=True) from None
    if route_device != "tun0":
        raise PreflightError("RUTA", recoverable=True)

    request = urllib.request.Request(
        f"{base_url}/api/tags",
        headers={"Accept": "application/json"},
    )

    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
            status = response.status
            payload = json.load(response)
    except urllib.error.HTTPError:
        raise PreflightError("HTTP", recoverable=True) from None
    except urllib.error.URLError as error:
        reason = error.reason
        if isinstance(reason, (TimeoutError, socket.timeout)):
            error_type = "TIMEOUT"
        elif isinstance(reason, socket.gaierror):
            error_type = "DNS"
        elif isinstance(reason, ConnectionRefusedError):
            error_type = "CONEXION_RECHAZADA"
        else:
            error_type = "RED"
        raise PreflightError(error_type, recoverable=True) from None
    except (TimeoutError, socket.timeout):
        raise PreflightError("TIMEOUT", recoverable=True) from None
    except ConnectionRefusedError:
        raise PreflightError("CONEXION_RECHAZADA", recoverable=True) from None
    except OSError:
        raise PreflightError("RED", recoverable=True) from None
    except json.JSONDecodeError:
        raise PreflightError("RESPUESTA_ENDPOINT", recoverable=True) from None

    if status != 200:
        raise PreflightError("HTTP", recoverable=True)

    models = {
        str(item.get("name") or item.get("model") or "")
        for item in payload.get("models", [])
        if isinstance(item, dict)
    }
    if chat_model not in models:
        raise PreflightError("MODELO_NO_DISPONIBLE", recoverable=False)


def run_with_retries(
    check=check_once,
    *,
    attempts: int = MAX_ATTEMPTS,
    retry_delay: int = RETRY_DELAY_SECONDS,
    sleep=time.sleep,
) -> int:
    for attempt in range(1, attempts + 1):
        started = time.monotonic()
        try:
            check()
        except PreflightError as error:
            elapsed = time.monotonic() - started
            print(
                f"Intento {attempt}/{attempts}: "
                f"FALLO {error.error_type} ({elapsed:.3f} s).",
                file=sys.stderr,
            )
            if not error.recoverable or attempt == attempts:
                return 1
            sleep(retry_delay)
        else:
            elapsed = time.monotonic() - started
            print(
                f"Intento {attempt}/{attempts}: "
                f"OK NINGUNO ({elapsed:.3f} s)."
            )
            return 0
    return 1


def main() -> None:
    raise SystemExit(run_with_retries())


if __name__ == "__main__":
    main()

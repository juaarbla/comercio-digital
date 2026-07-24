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


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    project_dir = Path(__file__).resolve().parent.parent
    env_file = project_dir / ".env"

    if not env_file.is_file():
        fail("no existe .env")

    config = dotenv_values(env_file)
    base_url = (config.get("OLLAMA_BASE_URL") or "").strip().rstrip("/")
    chat_model = (config.get("CHAT_MODEL") or "").strip()

    if not base_url:
        fail("OLLAMA_BASE_URL no está configurada")
    if not chat_model:
        fail("CHAT_MODEL no está configurado")

    parsed = urllib.parse.urlparse(base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        fail("OLLAMA_BASE_URL no tiene un formato HTTP(S) válido")

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
        fail("no se puede resolver el host privado de Ollama")

    if not addresses or not all(
        any(ipaddress.ip_address(address) in network for network in PRIVATE_NETWORKS)
        for address in addresses
    ):
        fail("OLLAMA_BASE_URL no resuelve exclusivamente a una red privada")

    if not Path("/sys/class/net/tun0").is_dir():
        fail("la interfaz VPN tun0 no está disponible")

    try:
        route = subprocess.run(
            ["ip", "route", "get", parsed.hostname],
            check=True,
            capture_output=True,
            text=True,
            timeout=5,
        ).stdout.split()
    except (FileNotFoundError, subprocess.SubprocessError):
        fail("no se puede comprobar la ruta privada hacia Ollama")

    try:
        route_device = route[route.index("dev") + 1]
    except (ValueError, IndexError):
        fail("la ruta hacia Ollama no indica una interfaz válida")
    if route_device != "tun0":
        fail("la ruta hacia Ollama no utiliza tun0")

    request = urllib.request.Request(
        f"{base_url}/api/tags",
        headers={"Accept": "application/json"},
    )
    started = time.monotonic()

    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(request, timeout=TIMEOUT_SECONDS) as response:
            status = response.status
            payload = json.load(response)
    except (TimeoutError, OSError, urllib.error.URLError, json.JSONDecodeError):
        fail("Ollama no responde correctamente en /api/tags")

    if status != 200:
        fail(f"Ollama devolvió HTTP {status} en /api/tags")

    models = {
        str(item.get("name") or item.get("model") or "")
        for item in payload.get("models", [])
        if isinstance(item, dict)
    }
    if chat_model not in models:
        fail("CHAT_MODEL no está disponible en Ollama")

    elapsed = time.monotonic() - started
    print(
        "Preflight Ollama correcto: "
        f"tun0, red privada, endpoint y modelo confirmados ({elapsed:.3f} s)."
    )


if __name__ == "__main__":
    main()

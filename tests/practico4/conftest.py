import importlib.util
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]


def cargar_app(ejercicio):
    # Cada Ejercicio tiene su propio app.py y su propio config.py, así que los
    # cargo por ruta y limpio el módulo "config" para que no se mezclen.
    carpeta = ROOT / f"Ejercicio{ejercicio}"
    sys.path.insert(0, str(carpeta))
    sys.modules.pop("config", None)
    try:
        spec = importlib.util.spec_from_file_location(
            f"app_ejercicio_{ejercicio}", carpeta / "app.py"
        )
        modulo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modulo)
        modulo.app.template_folder = str(carpeta / "templates")
        return modulo
    finally:
        sys.path.remove(str(carpeta))
        sys.modules.pop("config", None)


@pytest.fixture
def modulo_ejercicio1():
    return cargar_app(1)


@pytest.fixture
def modulo_ejercicio2():
    return cargar_app(2)


@pytest.fixture(scope="session", autouse=True)
def esperar_aplicacion_integracion(request):
    # Las pruebas de integración necesitan la app Java levantada en Docker.
    # Si no responde, fallan con un mensaje claro en vez de confundir un error
    # de conexión con el resultado de seguridad.
    if not any(item.get_closest_marker("integration") for item in request.session.items):
        return

    url = os.environ.get("PRACTICO4_URL", "http://127.0.0.1:8080")
    limite = time.monotonic() + 60
    while time.monotonic() < limite:
        try:
            urllib.request.urlopen(url, timeout=2).close()
            return
        except (urllib.error.URLError, OSError, TimeoutError):
            time.sleep(0.5)

    pytest.fail(f"La aplicación de integración no respondió en {url}")

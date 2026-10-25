import os
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

import pytest


pytestmark = pytest.mark.integration
URL = os.environ.get("PRACTICO4_URL", "http://127.0.0.1:8080")
CONTENEDOR = os.environ.get("PRACTICO4_CONTENEDOR", "cinebuscador4")


def en_contenedor(*argumentos):
    return subprocess.run(
        ["docker", "exec", CONTENEDOR, *argumentos],
        check=False,
        capture_output=True,
        text=True,
    )


def buscar(texto):
    query = urllib.parse.urlencode({"buscar": texto})
    try:
        return urllib.request.urlopen(f"{URL}/?{query}")
    except urllib.error.HTTPError as error:
        return error


def existe(ruta):
    return en_contenedor("test", "-e", ruta).returncode == 0


def test_busqueda_normal():
    respuesta = buscar("'Inception'")

    assert respuesta.status == 200
    assert b"Inception" in respuesta.read()


def test_busqueda_no_ejecuta_comandos():
    # Sin acceso al contenedor, "el archivo no existe" no probaría nada.
    assert en_contenedor("true").returncode == 0, f"No se pudo entrar a {CONTENEDOR}"

    marcador = f"/tmp/practico4-rce-{uuid.uuid4().hex}"
    comando = (
        "T(java.lang.Runtime).getRuntime()"
        f".exec(new String[]{{'touch','{marcador}'}})"
    )
    try:
        buscar(comando).read()
        # exec no espera al proceso: le doy unos segundos para que aparezca.
        for _ in range(10):
            if existe(marcador):
                break
            time.sleep(0.3)

        assert not existe(marcador), "La búsqueda ejecutó un comando en el servidor"
    finally:
        en_contenedor("rm", "-f", marcador)

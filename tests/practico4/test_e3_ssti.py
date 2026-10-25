import os
import urllib.error
import urllib.parse
import urllib.request

import pytest


pytestmark = pytest.mark.integration
URL = os.environ.get("PRACTICO4_URL", "http://127.0.0.1:8080")


def buscar(texto):
    # Devuelve (status, cuerpo). La mitigación del P2 rechaza las expresiones
    # peligrosas con un error 500, así que capturamos también ese caso.
    query = urllib.parse.urlencode({"buscar": texto})
    try:
        respuesta = urllib.request.urlopen(f"{URL}/?{query}")
    except urllib.error.HTTPError as error:
        return error.code, error.read().decode("utf-8", "replace")
    return respuesta.status, respuesta.read().decode("utf-8", "replace")


def test_busqueda_normal_funciona():
    estado, pagina = buscar("'Inception'")

    assert estado == 200
    assert "Inception" in pagina


def test_no_resuelve_tipos_java_del_sistema():
    # T(...) referencia clases Java: es el vector de SSTI/SpEL que la
    # mitigación del P2 (SimpleEvaluationContext) bloquea. En main se evalúa
    # y filtra el nombre del sistema operativo; en practico-2 se rechaza.
    _, pagina = buscar("T(java.lang.System).getProperty('os.name')")

    assert "Resultados buscando por: Linux" not in pagina


def test_no_referencia_la_clase_runtime():
    # Runtime es la puerta a la ejecución de comandos; tampoco debe resolverse.
    # En main, T(java.lang.Runtime) se evalúa y muestra "class java.lang.Runtime".
    _, pagina = buscar("T(java.lang.Runtime)")

    assert "class java.lang.Runtime" not in pagina

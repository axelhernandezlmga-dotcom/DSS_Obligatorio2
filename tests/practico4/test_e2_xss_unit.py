import pytest
from flask import render_template


pytestmark = pytest.mark.unit


def vista_previa(modulo, descripcion):
    # Renderiza la plantilla real edit.html con la misma llamada que la ruta
    # /edit, sin base de datos ni servidor, y devuelve el bloque de vista previa.
    pelicula = {
        "id": 1,
        "nombre": "Dune",
        "genero": "Sci-Fi",
        "director": "Denis Villeneuve",
        "descripcion": descripcion,
    }
    with modulo.app.test_request_context():
        pagina = render_template("edit.html", pelicula=pelicula)
    bloque = pagina.split('<div class="prev-descripcion">', 1)[1]
    return bloque.split("</div>", 1)[0]


def test_descripcion_con_script_se_escapa(modulo_ejercicio2):
    bloque = vista_previa(modulo_ejercicio2, "<script>alert('xss')</script>")

    # La versión vulnerable deja el <script> tal cual (filtro | safe); la
    # mitigada lo escapa, así que el navegador no lo ejecuta.
    assert "<script>" not in bloque
    assert "&lt;script&gt;" in bloque


def test_descripcion_normal_se_muestra(modulo_ejercicio2):
    bloque = vista_previa(modulo_ejercicio2, "Una pelicula de ciencia ficcion")

    assert "Una pelicula de ciencia ficcion" in bloque

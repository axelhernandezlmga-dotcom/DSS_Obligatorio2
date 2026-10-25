import sqlite3

import pytest


pytestmark = pytest.mark.unit


@pytest.fixture
def buscar(monkeypatch, modulo_ejercicio1):
    # Base SQLite en memoria creada por el test: reemplaza solo la conexión.
    # La consulta la arma y la ejecuta la función real de app.py.
    base = sqlite3.connect(":memory:")
    base.executescript(
        """
        CREATE TABLE peliculas (id INTEGER PRIMARY KEY, nombre TEXT);
        CREATE TABLE funciones (
            pelicula_id INTEGER, fecha_hora TEXT,
            asientos_totales INTEGER, asientos_ocupados INTEGER
        );
        INSERT INTO peliculas VALUES (1, 'Dune'), (2, 'Oppenheimer');
        INSERT INTO funciones VALUES (1, '2026-10-24 19:00', 100, 20);
        INSERT INTO funciones VALUES (2, '2026-10-24 20:00', 100, 30);
        """
    )
    monkeypatch.setattr(modulo_ejercicio1, "get_db", lambda: base)
    yield modulo_ejercicio1.buscar_funciones
    base.close()


def nombres(filas):
    return [fila[0] for fila in filas]


def test_busqueda_normal(buscar):
    assert nombres(buscar("Dune")) == ["Dune"]


def test_comilla_en_buscar_no_altera_la_consulta(buscar):
    # En la versión vulnerable, OR 1=1 hace que vuelvan todas las películas.
    assert nombres(buscar("%' OR 1=1 -- ")) == []


def test_sentido_de_orden_no_altera_la_consulta(buscar):
    # sort_dir va al ORDER BY; si se concatena, LIMIT 0 deja la búsqueda vacía.
    assert nombres(buscar("Dune", sort_dir="ASC LIMIT 0")) == ["Dune"]

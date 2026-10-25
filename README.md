# Desarrollo Seguro de Software — Práctico 4

Pruebas automáticas que verifican las mitigaciones del Práctico 2 y evitan que las vulnerabilidades se reintroduzcan. El mismo conjunto de pruebas está en las dos ramas: en **`main`** (código vulnerable) las aserciones de seguridad **fallan**, y en **`practico-2`** (código mitigado) **pasan**. Los casos normales pasan en ambas.

El detalle de cada ejercicio, con la discrepancia de numeración entre la consigna y el repositorio, está en el [informe del práctico](docs/practico-4/Informe-Practico4.md). El [registro de evidencias](docs/practico-4/evidencias/README.md) enlaza logs y capturas por ejercicio y rama.

| Ej. | Vulnerabilidad | Tipo de prueba | Tecnología | Archivo |
|---|---|---|---|---|
| 1 | SQL Injection | Unitaria | Pytest | `tests/practico4/test_e1_sqli_unit.py` |
| 2 | XSS | Unitaria | Pytest | `tests/practico4/test_e2_xss_unit.py` |
| 3 | SSTI (SpEL, en `Ejercicio4`) | Integración | Pytest + Docker | `tests/practico4/test_e3_ssti.py` |
| 4 | RCE | Integración | Pytest + Docker | `tests/practico4/test_e4_rce.py` |
| 5 | Almacenamiento inseguro | Unitaria | JUnit | `Ejercicio5/src/test/java/com/cinebuscador/config/EncryptionServiceTest.java` |

## Requisitos

- Python 3.14 y pytest 8 (`requirements-practico4.txt`), más Flask para E1 y E2.
- Docker Engine y Docker Compose v2 para las integraciones (E3 y E4).
- Para E5, Java 17 y Maven 3.9, o la imagen Maven vía Docker (comando más abajo).

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r Ejercicio1/requirements.txt -r Ejercicio2/requirements.txt -r requirements-practico4.txt
```

## Pruebas unitarias (E1 y E2)

Se corren por línea de comando, sin levantar la aplicación ni servicios. E1 llama a la función real de búsqueda con una base SQLite en memoria; E2 renderiza la plantilla real con `render_template`.

```sh
python -m pytest -m unit -q
```

## Integración SSTI y RCE (E3 y E4)

Recorren por HTTP el controlador real de `Ejercicio4` (contenedor `cinebuscador4`). Se sugiere el ambiente dockerizado:

```sh
docker compose -f Ejercicio4/docker-compose.yml up --build -d
python -m pytest -m integration -q
docker compose -f Ejercicio4/docker-compose.yml down
```

`PRACTICO4_URL` cambia la URL (por defecto `http://127.0.0.1:8080`) y `PRACTICO4_CONTENEDOR`, el nombre del contenedor. E3 comprueba que los vectores de SSTI/SpEL que acceden a tipos de Java (`T(...)`) se evalúan en `main` y los rechaza la mitigación de `practico-2`; E4, que una expresión no ejecute un comando del sistema operativo.

## Unitaria de almacenamiento (E5, JUnit)

```sh
cd Ejercicio5
mvn test
cd ..
```

O desde la raíz, con Docker (sin Java ni Maven instalados):

```sh
docker run --rm -v "$PWD/Ejercicio5:/workspace" -w /workspace \
  maven:3.9.11-eclipse-temurin-17-noble mvn test
```

## Resultados esperados

En **`practico-2`**: pasan las 5 unitarias de Pytest (3 de E1 y 2 de E2), las 5 de integración (3 de E3 y 2 de E4) y las 3 de JUnit.

En **`main`**: pasan los casos normales y **fallan** las aserciones que detectan SQLi, XSS, SSTI, RCE y el almacenamiento AES/ECB. Un código de salida distinto de cero en esos grupos es el resultado esperado.

> Nota: el `Ejercicio3` del repositorio es carga insegura de archivos (no es uno de los cinco ejercicios del Práctico 4), por lo que no tiene una prueba automática en este conjunto.

# Registro de evidencias

Cada log guarda, en su encabezado, la rama, el commit, el comando y el código de salida de una corrida real. El mismo conjunto de pruebas corre en las dos ramas: el fallo en `main` es el comportamiento vulnerable que la aserción detecta. La prueba del resultado está en los logs; el código de la aplicación se enlaza directamente desde el informe. La única evidencia visual son las tres capturas de navegador de E3.

| Ejercicio | Resultado en `main` | Resultado en `practico-2` | Evidencia |
|---|---|---|---|
| E1 — SQL Injection (unitaria) | 1 normal pasa; fallan comilla `OR 1=1` y `sort_dir` | 3 pasan | [main](E1-sqli/main/) · [practico-2](E1-sqli/practico-2/) |
| E2 — XSS (unitaria) | normal pasa; falla el escape del `<script>` | 2 pasan | [main](E2-xss/main/) · [practico-2](E2-xss/practico-2/) |
| E3 — SSTI / SpEL (integración) | normal pasa; fallan `T(System)` (fuga `Linux`) y `T(Runtime)` | 3 pasan (los `T(...)` dan 500) | [main](E3-ssti/main/) · [practico-2](E3-ssti/practico-2/) |
| E4 — RCE (integración) | normal pasa; falla la ejecución de `touch` | 2 pasan | [main](E4-rce/main/) · [practico-2](E4-rce/practico-2/) |
| E5 — Almacenamiento (JUnit) | verificación pasa; fallan desigualdad y formato BCrypt | 3 pasan | [main](E5-storage/main/) · [practico-2](E5-storage/practico-2/) |

## Archivos por carpeta

- `02-pytest.log` — unitarias de Pytest (E1, E2).
- `02-integracion.log` — integración HTTP contra el contenedor `cinebuscador4` (E3, E4).
- `02-junit.log` — salida de `mvn test` (E5).
- `E3-ssti/main/01-ssti-navegador.png` — `main`: `T(java.lang.System).getProperty('os.name')` filtra «Linux».
- `E3-ssti/practico-2/02-busqueda-normal.png` — `practico-2`: la búsqueda normal `'Inception'` funciona (app sana).
- `E3-ssti/practico-2/01-ssti-navegador.png` — `practico-2`: el mismo payload de `main` devuelve error 500 (rechazado).

## Notas sobre las capturas

La evidencia visual son las tres capturas de navegador de E3, tomadas contra el contenedor en vivo. La mitigación no se demuestra por el error 500 por sí solo: se muestra el contraste entre `main` (filtra «Linux»), `practico-2` funcionando normal y `practico-2` rechazando el mismo payload, y los logs de integración verifican por aserción que el nombre del sistema no aparece.

Retiré las capturas de VS Code con el código de la aplicación: eran reales pero su barra de pestañas y su árbol de archivos mostraban tests ya eliminados (`test_e1_sqli.py`, `test_e2_xss.py`, `test_e3_upload.py`), y no pude regenerarlas limpias en este entorno. El código se enlaza desde el informe y los logs demuestran el resultado. Tampoco fue posible capturar la terminal integrada; los logs corresponden a los comandos ejecutados.

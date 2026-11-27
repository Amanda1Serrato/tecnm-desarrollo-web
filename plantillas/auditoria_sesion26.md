# Bitácora de Requerimientos y Auditoría IA — Sesión 26
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Transacciones ACID, Aislamiento y Rollback  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Amanda Ideth Serrato Carmona]  
**Matrícula:** [23531056]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Bloque try/except con rollback() explicito  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad que encontré fue controlar correctamente las operaciones de la base de datos, porque primero tenía que verificar si había ejemplares disponibles y después descontar uno y registrar el préstamo. Me di cuenta de que si ocurría un error durante el proceso, los datos podían quedar incompletos. Por eso fue necesario utilizar una transacción y rollback para cancelar los cambios cuando algo falla.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python 3.13, FastAPI y SQLite ejecutados en Google Colab. Se necesita administrar libros y préstamos mediante una base de datos.|
| **Rol (R)** | Desarrollador especializado en APIs REST, Python y bases de datos, encargado de implementar transacciones seguras y mantener la integridad de la información. |
| **Especificación (E)** | Crear las rutas GET /api/libros/{id} y POST /api/prestamos. El sistema debe consultar el stock, descontar un ejemplar y registrar el préstamo dentro de una misma transacción. Si no hay ejemplares, debe responder HTTP 409 y ejecutar rollback para evitar cambios en la base de datos. |
| **Output (O)** | Código funcional en app.py, utilizando FastAPI, SQLite, COMMIT y ROLLBACK. Debe cumplir las pruebas HTTP y evitar que existan préstamos sin descuento o cantidades negativas de ejemplares. |

### 2.2 Prompt Estructurado
```text
[Pega aquí el prompt formal que redactaste para la IA]
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sqlite3

app = FastAPI(
    title="Biblioteca API",
    version="1.0.0"
)

DATABASE = "biblioteca.db"


# Conexión a la base de datos
def conectar():
    conexion = sqlite3.connect(DATABASE, timeout=10)
    conexion.row_factory = sqlite3.Row
    return conexion


# Crear las tablas e insertar el libro inicial
def inicializar_bd():
    conexion = conectar()

    try:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS libros (
                id INTEGER PRIMARY KEY,
                titulo TEXT NOT NULL,
                ejemplares INTEGER NOT NULL CHECK (ejemplares >= 0)
            )
        """)

        conexion.execute("""
            CREATE TABLE IF NOT EXISTS prestamos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                libro_id INTEGER NOT NULL,
                usuario TEXT NOT NULL,
                FOREIGN KEY (libro_id) REFERENCES libros(id)
            )
        """)

        conexion.execute("""
            INSERT OR IGNORE INTO libros (id, titulo, ejemplares)
            VALUES (1, 'Rayuela', 1)
        """)

        conexion.commit()

    finally:
        conexion.close()


# Preparar la base de datos
inicializar_bd()


# Modelo para recibir los datos del préstamo
class PrestamoEntrada(BaseModel):
    libro_id: int
    usuario: str


# Consultar los ejemplares disponibles
@app.get("/api/libros/{id}")
def obtener_libro(id: int):
    conexion = conectar()

    try:
        libro = conexion.execute(
            "SELECT id, titulo, ejemplares FROM libros WHERE id = ?",
            (id,)
        ).fetchone()

        if libro is None:
            return JSONResponse(
                status_code=404,
                content={"error": "libro no encontrado"}
            )

        return {
            "id": libro["id"],
            "titulo": libro["titulo"],
            "ejemplares": libro["ejemplares"]
        }

    finally:
        conexion.close()


# Registrar un préstamo mediante una transacción
@app.post("/api/prestamos", status_code=201)
def crear_prestamo(datos: PrestamoEntrada):

    conexion = conectar()

    try:
        # Iniciar la transacción
        conexion.execute("BEGIN IMMEDIATE")

        # Consultar el libro dentro de la transacción
        libro = conexion.execute(
            "SELECT ejemplares FROM libros WHERE id = ?",
            (datos.libro_id,)
        ).fetchone()

        if libro is None:
            conexion.rollback()

            return JSONResponse(
                status_code=404,
                content={"error": "libro no encontrado"}
            )

        # Validar que existan ejemplares
        if libro["ejemplares"] <= 0:
            conexion.rollback()

            return JSONResponse(
                status_code=409,
                content={"error": "sin ejemplares"}
            )

        # Descontar un ejemplar
        conexion.execute(
            """
            UPDATE libros
            SET ejemplares = ejemplares - 1
            WHERE id = ? AND ejemplares > 0
            """,
            (datos.libro_id,)
        )

        # Registrar el préstamo
        cursor = conexion.execute(
            """
            INSERT INTO prestamos (libro_id, usuario)
            VALUES (?, ?)
            """,
            (datos.libro_id, datos.usuario)
        )

        prestamo_id = cursor.lastrowid

        # Confirmar ambas operaciones
        conexion.commit()

        # Consultar el stock actualizado
        libro_actualizado = conexion.execute(
            "SELECT ejemplares FROM libros WHERE id = ?",
            (datos.libro_id,)
        ).fetchone()

        return {
            "prestamo_id": prestamo_id,
            "libro_id": datos.libro_id,
            "quedan": libro_actualizado["ejemplares"]
        }

    except Exception:
        # Deshacer los cambios si ocurre un error
        conexion.rollback()
        raise

    finally:
        conexion.close()

==============================================================================

VERIFICACIÓN DEL RESULTADO · 5 casos · app.py

==============================================================================

✅ 01. El libro inicia con un ejemplar
✅ 02. El primer préstamo se completa
✅ 03. El stock quedó en cero
✅ 04. El segundo préstamo falla con 409
✅ 05. El stock no quedó negativo

------------------------------------------------------------------------------

RESULTADO: 5/5 casos correctos. ¡Resultado logrado!

✅ La operación usa una transacción

------------------------------------------------------------------------------

RESULTADO: 1/1 comprobaciones correctas. ¡Resultado logrado!

```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de aborto por falla intermedia y consistencia

* [ x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [ x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [ x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> Al revisar la implementación, identifiqué que era importante controlar el caso en el que se intenta realizar un préstamo cuando ya no existen ejemplares disponibles. Para corregirlo utilicé el código HTTP 409 Conflict y agregué rollback para cancelar la operación. También utilicé una restricción CHECK en la base de datos para evitar que el stock tuviera cantidades negativas. De esta manera, los cambios se confirman solamente cuando las operaciones se realizan correctamente.

---
**Firma digital:** [Amanda1Serrato]

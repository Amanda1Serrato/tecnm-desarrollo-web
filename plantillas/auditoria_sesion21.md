# Bitácora de Requerimientos y Auditoría IA — Sesión 21
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Fundamentos de Persistencia: SQLite / PostgreSQL y Drivers  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Amanda Ideth Serrato Carmona]  
**Matrícula:** [23531056]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Conexión manual y ejecución de sentencias SQL  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> 

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Utilizar Python 3.10 o superior, FastAPI y SQLite para desarrollar una API con almacenamiento permanente de información. |
| **Rol (R)** | La IA actuará como un arquitecto de software especializado en APIs REST y bases de datos.|
| **Especificación (E)** | Implementar una conexión con SQLite, crear automáticamente la tabla libros, registrar libros mediante POST y consultarlos mediante GET, utilizando consultas SQL parametrizadas.|
| **Output (O)** | Obtener un archivo app.py funcional, organizado y con una base de datos llamada biblioteca.db, además de las pruebas HTTP aprobadas.|

### 2.2 Prompt Estructurado
```text
[Actúa como un arquitecto de software especializado en
Python, FastAPI y bases de datos SQLite.

Necesito desarrollar una API REST que permita almacenar
y consultar libros utilizando SQLite.

La aplicación debe cumplir los siguientes requisitos:

1. Crear automáticamente la base de datos biblioteca.db.
2. Crear la tabla libros si todavía no existe.
3. La tabla debe contener id, titulo y anio.
4. Implementar POST /api/libros para registrar libros.
5. Implementar GET /api/libros para consultar los libros.
6. Utilizar consultas SQL parametrizadas.
7. Utilizar commit() para guardar los registros.
8. Devolver HTTP 201 al registrar un libro.
9. Devolver HTTP 200 al consultar los libros.
10. Validar los datos recibidos mediante Pydantic.
11. Organizar el código mediante funciones para
    conectar y consultar la base de datos.

Entrega el código completo en app.py, utilizando
Python y FastAPI, compatible con Google Colab.]
```

---

## 3. Código Devuelto por el Modelo
```python
# Código devuelto por el LLM
```
%%writefile app.py
import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Tus libros sobrevivirán al reinicio")

# Nombre del archivo de la base de datos
DB_NAME = "biblioteca.db"


# Crear la conexión con SQLite
def conectar_db():
    conexion = sqlite3.connect(DB_NAME)
    conexion.row_factory = sqlite3.Row
    return conexion


# Crear la tabla si todavía no existe
def inicializar_db():
    conexion = conectar_db()

    conexion.execute("""
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            anio INTEGER NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()


# Inicializar la base de datos
inicializar_db()


# Modelo para recibir los datos del libro
class LibroEntrada(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    anio: int = Field(ge=0)


# Ruta para registrar un libro
@app.post("/api/libros", status_code=201)
def crear_libro(datos: LibroEntrada):

    conexion = conectar_db()

    cursor = conexion.execute(
        "INSERT INTO libros (titulo, anio) VALUES (?, ?)",
        (datos.titulo, datos.anio)
    )

    conexion.commit()

    nuevo_id = cursor.lastrowid

    conexion.close()

    return {
        "id": nuevo_id,
        "titulo": datos.titulo,
        "anio": datos.anio
    }


# Ruta para consultar todos los libros
@app.get("/api/libros")
def listar_libros():

    conexion = conectar_db()

    resultados = conexion.execute(
        "SELECT id, titulo, anio FROM libros ORDER BY id"
    ).fetchall()

    libros = [dict(fila) for fila in resultados]

    conexion.close()

    return {
        "libros": libros
    }

==============================================================================

VERIFICACIÓN DEL RESULTADO · 3 casos · app.py

==============================================================================

✅ 01. La base inicia sin libros
✅ 02. El libro se inserta en SQLite
✅ 03. El listado lee la base

------------------------------------------------------------------------------

RESULTADO: 3/3 casos correctos. ¡Resultado logrado!



✅ La fila existe en el archivo SQLite
------------------------------------------------------------------------------
RESULTADO: 1/1 comprobaciones correctas. ¡Resultado logrado!

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de recuperación ante desconexión de DB

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [ x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [ x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> La IA no contempló inicialmente el manejo de posibles errores al conectar con la base de datos ni la validación de datos incorrectos. Para mejorar esto, revisé las consultas SQL, utilicé consultas parametrizadas para evitar insertar datos de forma insegura y agregué validaciones con Pydantic. También comprobé que la API respondiera correctamente con los códigos HTTP 200 y 201, evitando errores durante las pruebas.

---
**Firma digital:** [amanda1Serrato]

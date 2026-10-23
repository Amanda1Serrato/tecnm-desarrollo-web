# Bitácora de Requerimientos y Auditoría IA — Sesión 02
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Gestión en GitHub Web y Métodos HTTP (GET, POST, PUT, DELETE)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Amanda Ideth Serrato Carmona]  
**Matrícula:** [23531056]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Enrutamiento manual por verbo HTTP  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad que encontré fue identificar qué debía hacer cada petición HTTP y comprobar que los datos recibidos fueran correctos. También debía asegurarme de que cada operación devolviera el código de respuesta adecuado. Por ejemplo, al consultar un libro que no existe, la API debe responder con 404, mientras que si se utiliza un método no permitido para una ruta, debe responder con 405. Esto me ayudó a comprender la importancia de organizar las rutas y validar los datos correctamente.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | FastAPI 0.110+ (Python 3.10+) o PHP 8.2 con servidor embebido |
| **Rol (R)** | Arquitecto de software senior especialista en APIs RESTful y Seguridad Web |
| **Especificación (E)** | Especificación semántica de verbos e idempotencia |
| **Output (O)** | Solo código modular, esquemas Pydantic/DTO y códigos HTTP semánticos |

### 2.2 Prompt Estructurado
```text
[Actúa como un desarrollador de Python y FastAPI. Ayúdame a crear una API de libros que permita registrar, consultar, actualizar y eliminar libros usando GET, POST, PUT y DELETE. Guarda los libros en memoria, valida los datos con Pydantic y utiliza los códigos HTTP correctos. Si un libro no existe, debe responder 404 y, si se usa un método no permitido como PATCH, debe responder 405. Entrega el código completo y fácil de entender para ejecutarlo en Google Colab.]
```

---

## 3. Código Devuelto por el Modelo
```python

%%writefile app.py
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

app = FastAPI(title="CRUD de libros")

# Modelo para recibir los datos de un libro
class LibroEntrada(BaseModel):
    titulo: str
    anio: int

# Colección en memoria, inicia vacía
libros = {}
siguiente_id = 1


# GET: consultar todos los libros
@app.get("/api/libros")
def listar_libros():
    return {"libros": list(libros.values())}


# POST: crear un libro
@app.post("/api/libros", status_code=201)
def crear_libro(datos: LibroEntrada):
    global siguiente_id

    libro = {
        "id": siguiente_id,
        "titulo": datos.titulo,
        "anio": datos.anio
    }

    libros[siguiente_id] = libro
    siguiente_id += 1

    return libro


# GET: consultar un libro por su ID
@app.get("/api/libros/{id}")
def obtener_libro(id: int):
    if id not in libros:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    return libros[id]


# PUT: reemplazar los datos de un libro
@app.put("/api/libros/{id}")
def actualizar_libro(id: int, datos: LibroEntrada):
    if id not in libros:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    libro = {
        "id": id,
        "titulo": datos.titulo,
        "anio": datos.anio
    }

    libros[id] = libro
    return libro


# DELETE: eliminar un libro sin devolver contenido
@app.delete("/api/libros/{id}", status_code=204)
def eliminar_libro(id: int):
    if id not in libros:
        raise HTTPException(status_code=404, detail="Libro no encontrado")

    del libros[id]
    return Response(status_code=204)


```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de métodos no permitidos (HTTP 405)

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> El error más importante que revisé fue la diferencia entre los códigos 404 y 405. Lo corregí utilizando 404 cuando un libro no existe y dejando que FastAPI responda 405 cuando se utiliza un método no permitido, como PATCH. También comprobé que cada operación devolviera el código HTTP correspondiente.

---
**Firma digital:** [Amanda]

# Bitácora de Requerimientos y Auditoría IA — Sesión 08
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Respuestas Semánticas y Excepciones HTTP Personalizadas  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Amanda Ideth Serrato Carmona]  
**Matrícula:** [23531056]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Lanzamiento manual de excepciones estructuradas  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad fue identificar los errores y asignarles el código HTTP correcto. También era complicado validar los datos manualmente y mostrar mensajes claros sin revelar información interna del sistema.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python 3.10 o superior, FastAPI y Pydantic para crear una API.|
| **Rol (R)** | Actuar como desarrollador especializado en manejo de errores HTTP. |
| **Especificación (E)** | Crear una excepción para libros inexistentes y validar los datos enviados. Utilizar códigos 404 y 422 con mensajes personalizados. |
| **Output (O)** | Código completo en app.py, con respuestas JSON uniformes y sin mostrar errores internos. |

### 2.2 Prompt Estructurado
```text
[Desarrolla una API utilizando Python, FastAPI y Pydantic.
Crea una excepción personalizada llamada LibroNoEncontrado
para cuando se consulte un libro que no existe.]
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from fastapi.exceptions import RequestValidationError

app = FastAPI(title="Manejo de errores HTTP")

# Base de datos inicial
libros = {
    1: {"id": 1, "titulo": "Rayuela", "anio": 1963}
}

# Modelo para registrar libros
class Libro(BaseModel):
    titulo: str = Field(min_length=1)
    anio: int

# Excepción personalizada
class LibroNoEncontrado(Exception):
    def __init__(self, libro_id):
        self.libro_id = libro_id

# Manejador para libros inexistentes
@app.exception_handler(LibroNoEncontrado)
async def libro_no_encontrado(request: Request, exc: LibroNoEncontrado):
    return JSONResponse(
        status_code=404,
        content={
            "error": {
                "codigo": "NO_ENCONTRADO",
                "mensaje": f"El libro {exc.libro_id} no existe"
            }
        }
    )

# Manejador para errores de validación
@app.exception_handler(RequestValidationError)
async def error_validacion(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "codigo": "VALIDACION",
                "mensaje": "Revisa los datos enviados"
            }
        }
    )

# Consultar un libro
@app.get("/api/libros/{libro_id}")
async def obtener_libro(libro_id: int):
    if libro_id not in libros:
        raise LibroNoEncontrado(libro_id)
    return libros[libro_id]

# Registrar un libro
@app.post("/api/libros", status_code=201)
async def crear_libro(libro: Libro):
    nuevo_id = max(libros.keys()) + 1
    nuevo_libro = {
        "id": nuevo_id,
        "titulo": libro.titulo,
        "anio": libro.anio
    }
    libros[nuevo_id] = nuevo_libro
    return nuevo_libro

```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de captura de errores sin crashing (HTTP 500)

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> La IA debía cuidar que los errores no mostraran información interna del sistema. Lo corregí utilizando manejadores personalizados para los errores 404 y 422, mostrando mensajes claros y evitando revelar detalles del código.

---
**Firma digital:** [Amanda1serrato]

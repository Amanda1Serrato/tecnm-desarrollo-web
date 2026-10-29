# Bitácora de Requerimientos y Auditoría IA — Sesión 06
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Validación Estricta, Constraints y Params Query/Body  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Amanda Ideth Serrato Carmona]  
**Matrícula:** [23531056]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Filtro manual de rangos y longitudes de texto  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad fue validar manualmente cada dato, porque tenía que revisar que el título tuviera la longitud correcta, que el año estuviera dentro del rango y que el precio fuera positivo. Esto podía provocar errores si olvidaba alguna condición.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | FastAPI 0.110+ (Python 3.10+) o PHP 8.2 con servidor embebido |
| **Rol (R)** | Actuar como desarrollador de una API REST que valide libros. |
| **Especificación (E)** | Crear y listar libros, validar el título de 3 a 80 caracteres, el año de 1450 a 2100, el precio mayor que cero y el límite entre 1 y 100. |
| **Output (O)** | SCódigo completo en app.py, con validaciones automáticas y respuestas HTTP 201, 200 o 422 según el resultado.|

### 2.2 Prompt Estructurado
```text
[Desarrolla una API REST con FastAPI y Python que permita registrar y consultar libros. Utiliza Pydantic y Field para validar que el título tenga entre 3 y 80 caracteres, el año esté entre 1450 y 2100 y el precio sea mayor que cero. En el listado, utiliza Query para aceptar un límite entre 1 y 100. Devuelve HTTP 201 al crear un libro válido, HTTP 200 al consultar y HTTP 422 cuando los datos no cumplan las restricciones. Organiza el código de forma clara y evita errores internos del servidor.]
```

---

## 3. Código Devuelto por el Modelo
```python
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()

class Libro(BaseModel):
    titulo: str = Field(min_length=3, max_length=80)
    anio: int = Field(ge=1450, le=2100)
    precio: float = Field(gt=0)

libros = []

@app.post("/api/libros", status_code=201)
def crear_libro(libro: Libro):
    nuevo = {
        "id": len(libros) + 1,
        **libro.model_dump()
    }
    libros.append(nuevo)
    return nuevo

@app.get("/api/libros")
def listar_libros(
    limite: int = Query(default=10, ge=1, le=100)
):
    return {"libros": libros[:limite]}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de desbordamiento de cadenas y números negativos

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> La IA podía omitir el código HTTP 422 al recibir datos inválidos. Lo corregí usando Field y Query para validar la longitud del título, el rango del año, el precio positivo y el límite de paginación, evitando que se acepten datos incorrectos.

---
**Firma digital:** [Amanda1serrato]

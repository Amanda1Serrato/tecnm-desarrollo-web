# Bitácora de Requerimientos y Auditoría IA — Sesión 07
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Especificación OpenAPI (Swagger) y ReDoc  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Amanda Ideth Serrato Carmona]  
**Matrícula:** [23531056]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Anotación manual de metadata de endpoints  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad fue escribir manualmente la información de cada endpoint, porque debía indicar su ruta, función y códigos HTTP. Esto podía provocar errores o dejar información incompleta.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python 3, FastAPI y Pydantic para crear y documentar una API. |
| **Rol (R)** | Actuar como desarrollador de una API REST. |
| **Especificación (E)** | Crear las rutas para listar y registrar libros, documentar sus modelos y mostrar los códigos HTTP correctos. |
| **Output (O)** | Código completo en app.py y documentación automática en OpenAPI, Swagger UI y ReDoc.|

### 2.2 Prompt Estructurado
```text
[Crea una API REST con Python y FastAPI para registrar y consultar libros. Define los datos de la API con el título “Biblioteca API”, versión “1.0.0” y una descripción. Crea los endpoints GET y POST en /api/libros, utiliza modelos Pydantic y documenta las respuestas HTTP. Asegúrate de que /openapi.json, /docs y /redoc funcionen correctamente. Entrega el código completo en app.py, de forma clara y organizada.]
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="Biblioteca API",
    version="1.0.0",
    description="API de libros del curso DAB-2201"
)


# Modelo de los libros
class Libro(BaseModel):
    id: int
    titulo: str = Field(min_length=3, max_length=80)
    anio: int = Field(ge=1450, le=2100)
    precio: float = Field(gt=0)


# Datos que se reciben al crear un libro
class LibroCrear(BaseModel):
    titulo: str = Field(min_length=3, max_length=80)
    anio: int = Field(ge=1450, le=2100)
    precio: float = Field(gt=0)


# Modelo para la respuesta del listado
class ListadoLibros(BaseModel):
    libros: list[Libro]


libros = []


@app.get(
    "/api/libros",
    summary="Listar libros",
    response_model=ListadoLibros
)
def listar_libros():
    return {"libros": libros}


@app.post(
    "/api/libros",
    status_code=201,
    summary="Crear un libro",
    response_model=Libro
)
def crear_libro(datos: LibroCrear):
    nuevo = Libro(
        id=len(libros) + 1,
        **datos.model_dump()
    )
    libros.append(nuevo)
    return nuevo
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Verificación de renderizado de interfaz Swagger UI

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> 

---
**Firma digital:** [Amanda1serrato]

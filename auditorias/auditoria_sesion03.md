# Bitácora de Requerimientos y Auditoría IA — Sesión 03
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Headers, Content-Type y Negociación de Contenido  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Amanda Ideth Serrato Carmona]  
**Matrícula:** [23531056]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Lectura y emisión manual de encabezados HTTP  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> 

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Utilizar Python y FastAPI en Google Colab, sin base de datos. |
| **Rol (R)** | Actuar como desarrollador de una API para administrar libros. |
| **Especificación (E)** | Revisar los encabezados Content-Type y Accept, aceptar JSON y responder con los códigos HTTP correctos. |
| **Output (O)** | Un archivo app.py funcional, con validaciones y respuestas HTTP correctas. |

### 2.2 Prompt Estructurado
```text
[Ayúdame a crear una API con Python y FastAPI para registrar y consultar libros. Debe revisar los encabezados Content-Type y Accept, aceptar únicamente JSON y responder con los códigos HTTP 200, 201, 415 y 406 según corresponda. Guarda los libros en memoria y utiliza un código sencillo que funcione en Google Colab.]
```

---

## 3. Código Devuelto por el Modelo
```python

%%writefile app.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
import json

app = FastAPI(title="API de libros con negociación de contenido")

# Modelo para validar los datos del libro
class Libro(BaseModel):
    titulo: str
    anio: int

# Colección en memoria
libros = []
siguiente_id = 1


# POST: crear un libro
@app.post("/api/libros", status_code=201)
async def crear_libro(request: Request):
    global siguiente_id

    # Revisar el formato enviado
    content_type = request.headers.get("content-type", "")
    tipo = content_type.split(";")[0].strip().lower()

    if tipo != "application/json":
        raise HTTPException(
            status_code=415,
            detail="Solo se acepta application/json"
        )

    # Leer y validar el contenido
    try:
        contenido = await request.json()
        datos = Libro.model_validate(contenido)
    except (json.JSONDecodeError, ValueError, ValidationError):
        raise HTTPException(
            status_code=400,
            detail="Los datos JSON no son válidos"
        )

    libro = {
        "id": siguiente_id,
        "titulo": datos.titulo,
        "anio": datos.anio
    }

    libros.append(libro)
    siguiente_id += 1

    return JSONResponse(
        status_code=201,
        content=libro,
        media_type="application/json"
    )


# GET: listar libros
@app.get("/api/libros")
async def listar_libros(request: Request):
    accept = request.headers.get("accept", "*/*")
    formatos = [formato.strip().lower() for formato in accept.split(",")]

    acepta_json = any(
        formato.split(";")[0].strip() in (
            "application/json",
            "*/*",
            "application/*"
        )
        for formato in formatos
    )

    if not acepta_json:
        raise HTTPException(
            status_code=406,
            detail="Solo se ofrece application/json"
        )

    return JSONResponse(
        content={"libros": libros},
        media_type="application/json"
    )
==============================================================================
VERIFICACIÓN DEL RESULTADO · 4 casos · app.py
==============================================================================
✅ 01. POST válido en JSON
✅ 02. POST en texto plano se rechaza con 415
✅ 03. GET que pide XML se rechaza con 406
✅ 04. GET que acepta JSON responde 200
------------------------------------------------------------------------------
RESULTADO: 4/4 casos correctos. ¡Resultado logrado!
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas con tipos de contenido no soportados (415)

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> La IA no había validado correctamente los formatos enviados y solicitados. Lo corregí agregando una revisión de los encabezados Content-Type y Accept, para que la API responda con 415 si recibe un formato no permitido y con 406 si se solicita uno que no acepta.

---
**Firma digital:** [Amanda1serrato]

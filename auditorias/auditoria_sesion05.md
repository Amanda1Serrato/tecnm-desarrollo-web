# Bitácora de Requerimientos y Auditoría IA — Sesión 05
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Pydantic v2 / DTOs en PHP y Tipado Estático  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Amanda Ideth Serrato Carmona]  
**Matrícula:** [23531056]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* DTO manual con validación de tipos primitivos  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad fue validar que los datos tuvieran el tipo correcto y evitar que se enviaran campos que no estaban permitidos. También era necesario controlar los errores para que la API respondiera correctamente.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Utilizar Python, FastAPI y Pydantic v2 para crear una API de libros. |
| **Rol (R)** | Crear una API segura que valide los datos antes de guardarlos. |
| **Especificación (E)** | ECrear DTOs de entrada y salida, validar los campos y rechazar datos incorrectos o adicionales. |
| **Output (O)** | Código organizado que registre y consulte libros usando los códigos HTTP correspondientes.|

### 2.2 Prompt Estructurado
```text
[
%%writefile app.py
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict

app = FastAPI(title="API de libros")

libros = []

# DTO para recibir los datos
class LibroEntrada(BaseModel):
    model_config = ConfigDict(extra="forbid")

    titulo: str
    anio: int
    precio: float
    disponible: bool


# DTO para devolver los datos
class LibroSalida(BaseModel):
    id: int
    titulo: str
    anio: int
    precio: float
    disponible: bool


# Registrar un libro
@app.post("/api/libros", status_code=201, response_model=LibroSalida)
def crear_libro(libro: LibroEntrada):
    nuevo_libro = libro.model_dump()
    nuevo_libro["id"] = len(libros) + 1

    libros.append(nuevo_libro)
    return nuevo_libro


# Consultar los libros registrados
@app.get("/api/libros")
def listar_libros():
    return {"libros": libros}
]
```

---

## 3. Código Devuelto por el Modelo
```python
==============================================================================
VERIFICACIÓN DEL RESULTADO · 5 casos · app.py
==============================================================================
✅ 01. Un libro válido se crea con 201
✅ 02. La cadena numérica se convierte a entero
✅ 03. Un año no numérico produce 422
✅ 04. Un campo extra produce 422
✅ 05. El listado devuelve los libros creados
------------------------------------------------------------------------------
RESULTADO: 5/5 casos correctos. ¡Resultado logrado!
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de tipos incompatibles y coerción

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> La primera versión no rechazaba los campos adicionales ni asignaba correctamente el primer ID. Lo corregí utilizando ConfigDict(extra="forbid") y len(libros) + 1 para generar los identificadores desde el número uno.

---
**Firma digital:** [Usuario de GitHub]

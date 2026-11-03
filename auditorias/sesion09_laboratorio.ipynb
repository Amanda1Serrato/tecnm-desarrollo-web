# Bitácora de Requerimientos y Auditoría IA — Sesión 09
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Middleware Web, Intercepción y Logging de Transacciones  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Amanda Ideth Serrato Carmona]  
**Matrícula:** [23531056]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Middleware manual de tiempo de respuesta (X-Process-Time)  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> 

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Framework FastAPI en Python, ejecutándose en el entorno de Google Colab para la asignatura de Desarrollo Web (TecNM Cancún). |
| **Rol (R)** | Desarrollador backend encargado de implementar un middleware HTTP para la medición de tiempos de procesamiento y trazabilidad de peticiones. |
| **Especificación (E)** | Código fuente funcional en el archivo app.py que cumpla con el contrato y supere los casos de prueba automatizados.


- Middleware que intercepte todas las peticiones (incluyendo errores 404).


- Inserción obligatoria de los encabezados X-Process-Time (tiempo decimal en segundos) y X-Request-ID (preservando el del cliente o generando un UUID único). |
| **Output (O)** | Solo código modular, esquemas Pydantic/DTO y códigos HTTP semánticos |

### 2.2 Prompt Estructurado
```text
%%writefile app.py
import time
import uuid
from fastapi import FastAPI, Request

app = FastAPI(title="Todas tus respuestas llevarán estas cabeceras")

@app.middleware("http")
async def add_process_time_and_request_id(request: Request, call_next):
    start_time = time.time()
    
    # Recupera el X-Request-ID del cliente o genera uno nuevo
    request_id = request.headers.get("X-Request-ID")
    if not request_id:
        request_id = str(uuid.uuid4())
        
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    # Inyecta las cabeceras requeridas en cualquier respuesta (incluyendo 404)
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    response.headers["X-Request-ID"] = request_id
    
    return response

@app.get("/api/libros")
def obtener_libros():
    return {"libros": []}
```

---

## 3. Código Devuelto por el Modelo
```python
==============================================================================
VERIFICACIÓN DEL RESULTADO · 3 casos · app.py
==============================================================================
✅ 01. Una respuesta correcta trae tiempo y traza
✅ 02. El X-Request-ID del cliente se conserva
✅ 03. El middleware también cubre los 404
------------------------------------------------------------------------------
RESULTADO: 3/3 casos correctos. ¡Resultado logrado!
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de inyección de encabezados de rastreo

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> En esta actividad implementé un middleware HTTP en FastAPI dentro de app.py para medir el tiempo de respuesta de cada petición (X-Process-Time) y manejar un identificador de trazabilidad (X-Request-ID).

---
**Firma digital:** [Amanda1Serrato]

# Bitácora de Requerimientos y Auditoría IA — Sesión 18
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Rate Limiting, Throttling y Prevención de Abuso  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Amanda Ideth Serrato Carmona]  
**Matrícula:** [23531056]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Contador manual de peticiones por IP en memoria  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad que encontré fue llevar el conteo de las peticiones de cada usuario y controlar el tiempo de espera. Al principio se me complicó hacer que el contador fuera independiente para cada dirección IP, porque si utilizaba un solo contador podía afectar a todos los clientes. También tuve que revisar que después de 60 segundos se reiniciara el conteo correctamente.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** |Python 3.10+ y FastAPI en Google Colab, utilizando almacenamiento en memoria.|
| **Rol (R)** | Desarrollador backend especializado en APIs REST, seguridad web y control de peticiones.|
| **Especificación (E)** | Implementar un Rate Limiting que permita tres peticiones por cliente durante una ventana de 60 segundos. La cuarta petición debe responder HTTP 429 e incluir el encabezado Retry-After. |
| **Output (O)** | Código completo en app.py, utilizando FastAPI, contadores por IP y respuestas HTTP con formato JSON. |

### 2.2 Prompt Estructurado
```text
[Actúa como un arquitecto de software especializado
en Python, FastAPI y seguridad de APIs REST.

Necesito implementar un sistema de Rate Limiting
para controlar las peticiones que recibe una API.

La ruta GET /api/recurso debe permitir un máximo
de tres peticiones por cliente durante 60 segundos.

Cada cliente debe identificarse mediante su IP
y tener su propio contador independiente.

Las primeras tres peticiones deben responder
con HTTP 200 OK.

La cuarta petición debe responder con HTTP 429
Too Many Requests e incluir el encabezado
Retry-After indicando el tiempo que debe esperar.

La respuesta debe ser un JSON con el mensaje:
"límite de peticiones alcanzado".

El contador debe reiniciarse al iniciar la aplicación
y cuando termine la ventana de tiempo.

Entrega el código completo en app.py, utilizando
FastAPI y Python, evitando errores HTTP 500
y manteniendo respuestas JSON correctas.]
```

---

## 3. Código Devuelto por el Modelo
```python
==============================================================================
VERIFICACIÓN DEL RESULTADO · 4 casos · app.py
==============================================================================
✅ 01. Primera petición permitida
✅ 02. Segunda petición permitida
✅ 03. Tercera petición permitida
✅ 04. La cuarta petición se limita
------------------------------------------------------------------------------
RESULTADO: 4/4 casos correctos. ¡Resultado logrado!
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de ráfaga masiva y bloqueo temporal (HTTP 429)

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> Un detalle que tuve que revisar fue que la respuesta 429 debía incluir el encabezado Retry-After, porque no era suficiente con indicar que se había superado el límite. También cuidé que cada dirección IP tuviera su propio contador para evitar afectar a otros usuarios. Con estos cambios se logró controlar la cantidad de peticiones y evitar que un solo cliente pudiera saturar la API.

---
**Firma digital:** [Amanda1Serrato]

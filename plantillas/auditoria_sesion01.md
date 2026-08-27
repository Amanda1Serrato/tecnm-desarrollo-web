# Bitácora de Requerimientos y Auditoría IA — Sesión 01
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Estudiante:** [Nombre Completo del Alumno]  
**Matrícula:** [No. de Control]  
**Fecha:** [AAAA-MM-DD]  
**Track Seleccionado:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Diagnóstico Manual)
*Describe qué dificultad encontraste al procesar el cuerpo JSON de la petición HTTP y validar datos a mano:*
> (Ejemplo: En FastAPI tuve que recordar cómo configurar el modelo Pydantic para capturar campos requeridos, o en PHP decodificar `php://input` con `json_decode`).

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos y Contexto C-R-E-O)

### 2.1 Matriz de Especificación de Endpoint (Contrato OpenAPI)

| Elemento C-R-E-O | Especificación Técnica Formal |
| :--- | :--- |
| **Contexto (C)** | Framework FastAPI 0.110+ (Python 3.10+) o PHP 8.2 con servidor embebido. |
| **Rol (R)** | Arquitecto de software senior especialista en seguridad y diseño de APIs RESTful. |
| **Especificación (E)** | Endpoint `POST /api/saludo`, Payload JSON `{ "nombre": "str" }` validando longitud [3..50] caracteres. Respuestas semánticas: `200 OK`, `400 Bad Request` / `422 Unprocessable Entity`. |
| **Output (O)** | Únicamente el bloque de código modular con esquemas de validación, sin texto introductorio innecesario. |

### 2.2 Diseño del Prompt Contextualizado
*Pega el prompt formal que redactaste a partir de la matriz:*

```text
[Pega aquí tu prompt estructurado]
```
3. Código Devuelto por el Modelo
Pega el fragmento de código retornado por el LLM:

```Python


# Código generado por la IA (FastAPI o PHP)
```

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
### 4.1 Batería de Pruebas de Códigos de Estado
```text
[ ] Petición con datos válidos: ¿Retorna código semántico 200 OK?

[ ] Nombre menor a 3 caracteres: ¿Rechaza la petición con código 400 o 422?

[ ] Campo vacío o espacios en blanco: ¿Dispara el error de validación esperado?

[ ] Payload mal formado / Ausente: ¿Maneja el error sin emitir una falla interna del servidor (500 Internal Server Error)?
```
### 4.2 Reporte Crítico
*¿La IA devolvió códigos de estado semánticos adecuados o intentó retornar HTTP 200 con un JSON que decía "error": true? Justifica técnicamente.*

(Documenta tu análisis y corrección aquí).

Firma digital: [Usuario de GitHub]

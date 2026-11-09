# Bitácora de Requerimientos y Auditoría IA — Sesión 11
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Arquitectura en Capas: Router, Servicio y Capa de Datos  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Amanda Ideth Serrato Carmona]  
**Matrícula:** [23531056]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Separación manual de controladores y lógica  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad que encontré fue separar las rutas de las funciones que realizan las operaciones, porque al principio todo estaba en un mismo archivo. También fue necesario organizar la validación de los datos para evitar errores al registrar libros y lograr que cada archivo tuviera una responsabilidad diferente.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python 3.13, FastAPI y Pydantic en Google Colab. Se trabaja con almacenamiento en memoria.|
| **Rol (R)** | Actuar como desarrollador de APIs REST con experiencia en arquitectura por capas.|
| **Especificación (E)** | Separar la aplicación en cuatro archivos: app, router, servicio y repositorio. Mantener GET 200, POST 201 y validaciones 422. |
| **Output (O)** | Entregar los cuatro archivos Python completos, organizados y funcionales, respetando el contrato HTTP. |

### 2.2 Prompt Estructurado
```text
[Actúa como un desarrollador experto en Python y FastAPI.
Organiza una API de libros utilizando arquitectura en capas.

Separa el proyecto en cuatro archivos:
app.py, router.py, servicio.py y repositorio.py.

El router debe manejar las rutas GET y POST, el servicio
debe contener la lógica para crear y listar libros, y el
repositorio debe almacenar los datos en memoria.

Utiliza Pydantic para validar el título y el año del libro.
Mantén las respuestas HTTP 200, 201 y 422.

Entrega el código completo, organizado y funcional,
sin mezclar las responsabilidades de cada capa.]
```

---

## 3. Código Devuelto por el Modelo
```python
# %%writefile app.py

from fastapi import FastAPI
from router import router

app = FastAPI(title="Biblioteca por capas")

# Incluimos las rutas de libros
app.include_router(router)
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de aislamiento de errores en lógica de negocio

* [X] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [X] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [X] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> La IA inicialmente podía dejar mezcladas algunas responsabilidades entre las capas. Para corregirlo, organicé el código separando el router, el servicio y el repositorio. También revisé que los datos inválidos fueran rechazados con el código HTTP 422 y que las respuestas de creación y consulta mantuvieran los códigos 201 y 200. De esta manera, la API quedó mejor organizada y fue más fácil de comprobar.

---
**Firma digital:** [Amanda1Serrato]

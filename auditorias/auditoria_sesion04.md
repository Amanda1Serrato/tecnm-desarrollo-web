# Bitácora de Requerimientos y Auditoría IA — Sesión 04
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Anatomía RESTful, URIs Nombres y Recursos  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Amanda Ideth Serrato Carmona]  
**Matrícula:** [23531056]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Diseño de URIs jerárquicas sin verbos en la ruta  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
>La dificultad que encontré fue organizar las rutas para consultar los libros de cada autor sin utilizar verbos en la URL. También tuve que validar que el autor existiera y hacer que los filtros por género y límite funcionaran correctamente. Para solucionarlo, utilicé la ruta /api/autores/{autor_id}/libros y los parámetros de consulta genero y limite. 

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Estoy desarrollando una API para consultar autores y sus libros, sin utilizar una base de datos. |
| **Rol (R)** | Desarrollador de una API RESTful que debe seguir buenas prácticas de diseño. |
| **Especificación (E)** | Crear la ruta GET /api/autores/{autor_id}/libros.

Registrar al autor 1, Gabriel García Márquez, con los libros “Cien años de soledad” (novela) y “Doce cuentos peregrinos” (cuento).

Registrar al autor 2, Julio Cortázar, con el libro “Rayuela” (novela).

Permitir filtrar los libros por el parámetro genero y limitar los resultados mediante limite.

Responder con el código HTTP 404 y el mensaje “Autor no encontrado” si el autor no existe.

Crear la ruta GET /api/libros para mostrar los tres libros.

Utilizar URIs jerárquicas sin verbos, respuestas JSON y códigos HTTP adecuados. |
| **Output (O)** | Entregar el código completo de app.py, organizado y listo para ejecutarse en Google Colab con FastAPI. |

### 2.2 Prompt Estructurado
```text
[==============================================================================
VERIFICACIÓN DEL RESULTADO · 4 casos · app.py
==============================================================================
✅ 01. Libros del autor 1
✅ 02. Filtro por género y límite
✅ 03. Un autor inexistente produce 404
✅ 04. La colección completa de libros
------------------------------------------------------------------------------
RESULTADO: 4/4 casos correctos. ¡Resultado logrado!]
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py
from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI(title="API de autores y libros")

# Autores registrados
autores = {
    1: "Gabriel García Márquez",
    2: "Julio Cortázar"
}

# Libros iniciales
libros = [
    {
        "id": 1,
        "titulo": "Cien años de soledad",
        "genero": "novela",
        "autor_id": 1
    },
    {
        "id": 2,
        "titulo": "Doce cuentos peregrinos",
        "genero": "cuento",
        "autor_id": 1
    },
    {
        "id": 3,
        "titulo": "Rayuela",
        "genero": "novela",
        "autor_id": 2
    }
]


# Consultar los libros de un autor
@app.get("/api/autores/{autor_id}/libros")
def libros_por_autor(
    autor_id: int,
    genero: Optional[str] = None,
    limite: Optional[int] = None
):
    if autor_id not in autores:
        raise HTTPException(
            status_code=404,
            detail="Autor no encontrado"
        )

    resultado = [
        libro for libro in libros
        if libro["autor_id"] == autor_id
    ]

    # Filtrar por género si se solicita
    if genero is not None:
        resultado = [
            libro for libro in resultado
            if libro["genero"].lower() == genero.lower()
        ]

    # Limitar la cantidad de resultados
    if limite is not None:
        resultado = resultado[:max(0, limite)]

    return {
        "autor_id": autor_id,
        "libros": [
            {
                "id": libro["id"],
                "titulo": libro["titulo"],
                "genero": libro["genero"]
            }
            for libro in resultado
        ]
    }


# Consultar todos los libros
@app.get("/api/libros")
def listar_libros():
    return {"libros": libros}
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de peticiones a recursos inexistentes (404)

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> en la IA se omitieron pasos cuando se solicitaba un autor que no existía  

---
**Firma digital:** [Amanda1serrato]

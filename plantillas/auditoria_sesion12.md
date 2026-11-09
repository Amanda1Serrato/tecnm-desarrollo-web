# Bitácora de Requerimientos y Auditoría IA — Sesión 12
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Inyección de Dependencias (FastAPI Depends / PHP Container)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Amanda Ideth Serrato Carmona]  
**Matrícula:** [23531056]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Inyector de dependencias manual por funciones  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> 

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Se utiliza Python 3 y FastAPI en Google Colab para desarrollar una API de libros mediante inyección de dependencias.|
| **Rol (R)** |Actúa como un desarrollador experto en Python, FastAPI y arquitectura de software, especializado en inyección de dependencias.|
| **Especificación (E)** | Crear un repositorio en memoria que se proporcione mediante Depends. Implementar las rutas GET y POST para consultar y registrar libros, además de una ruta de diagnóstico|
| **Output (O)** | Entregar el código completo en app.py, organizado, funcional y con inyección de dependencias correctamente implementada. |

### 2.2 Prompt Estructurado
```text
[Actúa como un desarrollador experto en Python y FastAPI.
Implementa una API de libros utilizando inyección de
dependencias con Depends().

Crea un repositorio en memoria y una función
get_repositorio() que proporcione una instancia
de RepositorioMemoria.

Implementa las rutas GET /api/libros,
POST /api/libros y GET /api/diagnostico.

Utiliza Pydantic para validar el título y el año.
Mantén las respuestas HTTP 200, 201 y 422.

Los endpoints deben recibir el repositorio mediante
Depends(), sin crear nuevas instancias dentro
de cada función.

Entrega el código completo y funcional en app.py.]
```

---

## 3. Código Devuelto por el Modelo
```python
# Código devuelto por el LLM
```
%%writefile app.py
from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field

app = FastAPI(title="Biblioteca con Inyección de Dependencias")


# Modelo para validar los datos del libro
class LibroEntrada(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    anio: int = Field(ge=1500, le=2026)


# Repositorio en memoria
class RepositorioMemoria:
    def __init__(self):
        self.libros = []
        self.siguiente_id = 1

    def guardar_libro(self, datos):
        libro = {
            "id": self.siguiente_id,
            "titulo": datos["titulo"],
            "anio": datos["anio"]
        }

        self.libros.append(libro)
        self.siguiente_id += 1

        return libro

    def obtener_libros(self):
        return self.libros


# Función que proporciona la dependencia
repositorio = RepositorioMemoria()

def get_repositorio():
    return repositorio


# Diagnóstico para conocer el repositorio utilizado
@app.get("/api/diagnostico")
def diagnostico(repo: RepositorioMemoria = Depends(get_repositorio)):
    return {"repositorio": type(repo).__name__}


# Registrar un libro
@app.post("/api/libros", status_code=201)
def crear_libro(
    libro: LibroEntrada,
    repo: RepositorioMemoria = Depends(get_repositorio)
):
    return repo.guardar_libro(libro.model_dump())


# Consultar los libros registrados
@app.get("/api/libros")
def listar_libros(repo: RepositorioMemoria = Depends(get_repositorio)):
    return {"libros": repo.obtener_libros()}

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de ciclo de vida de dependencias por request

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
>La IA inicialmente podía no contemplar que todos los endpoints debían utilizar la misma instancia del repositorio. Para corregirlo, utilicé una función llamada get_repositorio() que entrega el repositorio mediante Depends(). También revisé que los datos incorrectos fueran rechazados con el código HTTP 422 y que las rutas mantuvieran sus respuestas 200 y 201. 

---
**Firma digital:** [Usuario de GitHub]

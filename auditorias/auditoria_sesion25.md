# Bitácora de Requerimientos y Auditoría IA — Sesión 25
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Consultas Complejas, Joins y Carga Ansiosa (Eager Loading)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Amanda Ideth Serrato Carmona]  
**Matrícula:** [23531056]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Consulta SQL con INNER JOIN manual  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad que encontré fue relacionar correctamente los autores con sus libros, porque necesitaba consultar información de dos tablas y mostrarla de manera organizada. También se me complicó evitar que se realizaran demasiadas consultas por separado. Por eso fue necesario utilizar las relaciones del ORM y la carga ansiosa para obtener los datos relacionados de una manera más eficiente.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python 3.10+, FastAPI y SQLAlchemy con consultas a una base de datos relacional. Se trabaja con las tablas de autores y libros.|
| **Rol (R)** |Desarrollador especializado en APIs RESTful, SQLAlchemy y bases de datos, encargado de crear consultas eficientes y organizar las relaciones entre tablas.|
| **Especificación (E)** |Implementar consultas para obtener autores junto con sus libros relacionados utilizando selectinload o joinedload. Crear las rutas GET /api/autores, GET /api/autores/{id} y mantener funcionando GET /api/libros. Evitar el problema N+1 y devolver respuestas JSON correctas. |
| **Output (O)** |Código funcional en Python con FastAPI, modelos relacionados de SQLAlchemy, carga ansiosa y respuestas HTTP semánticas. La implementación debe devolver los autores con sus respectivos libros sin generar errores HTTP 500.|

### 2.2 Prompt Estructurado
```text
[Contexto:
Estoy trabajando en la Sesión 25 de Desarrollo de Aplicaciones
Web de TecNM Cancún. Utilizo Python, FastAPI y SQLAlchemy
para trabajar con una base de datos relacional.

Rol:
Actúa como un desarrollador de software especializado
en APIs RESTful, SQLAlchemy y consultas ORM.

Especificación:
Implementa consultas para obtener autores y sus libros
relacionados utilizando carga ansiosa (Eager Loading).

Utiliza selectinload o joinedload para evitar el problema N+1.

Necesito las siguientes rutas:
GET /api/autores
GET /api/autores/1
GET /api/libros

Los datos deben mostrar los autores con sus respectivos libros.
Por ejemplo:
García Márquez -> Cien años de soledad
Cortázar -> Rayuela

También debes asegurar que las relaciones se carguen
correctamente antes de generar las respuestas JSON,
evitando errores de sesión y problemas de serialización.

Output:
Entrega el código completo y funcional de la implementación,
con modelos, relaciones ORM, consultas y esquemas de respuesta.
El código debe funcionar con FastAPI y superar las pruebas
del verificador HTTP sin errores 500.]
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select
from sqlalchemy.orm import declarative_base, relationship, sessionmaker, selectinload

# --------------------------------------------------
# 1. CONFIGURACIÓN DE FASTAPI Y BASE DE DATOS
# --------------------------------------------------

app = FastAPI(
    title="Biblioteca API",
    version="1.0.0"
)

DATABASE_URL = "sqlite:///./biblioteca.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()


# --------------------------------------------------
# 2. MODELOS DE LA BASE DE DATOS
# --------------------------------------------------

class Autor(Base):
    __tablename__ = "autores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)

    libros = relationship(
        "Libro",
        back_populates="autor"
    )


class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)

    autor_id = Column(
        Integer,
        ForeignKey("autores.id"),
        nullable=False
    )

    autor = relationship(
        "Autor",
        back_populates="libros"
    )


# --------------------------------------------------
# 3. CREAR TABLAS Y CARGAR DATOS INICIALES
# --------------------------------------------------

def inicializar_bd():

    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:

        existe = db.execute(
            select(Autor.id).limit(1)
        ).first()

        if existe is None:

            autor1 = Autor(
                id=1,
                nombre="Gabriel García Márquez",
                libros=[
                    Libro(
                        id=1,
                        titulo="Cien años de soledad"
                    )
                ]
            )

            autor2 = Autor(
                id=2,
                nombre="Julio Cortázar",
                libros=[
                    Libro(
                        id=2,
                        titulo="Rayuela"
                    )
                ]
            )

            db.add_all([autor1, autor2])
            db.commit()


# Inicializar al cargar la aplicación
inicializar_bd()


# --------------------------------------------------
# 4. CONSULTAR TODOS LOS AUTORES CON SUS LIBROS
# --------------------------------------------------

@app.get("/api/autores")
def listar_autores():

    with SessionLocal() as db:

        consulta = (
            select(Autor)
            .options(selectinload(Autor.libros))
            .order_by(Autor.id)
        )

        autores = db.execute(consulta).scalars().all()

        return {
            "autores": [
                {
                    "id": autor.id,
                    "nombre": autor.nombre,
                    "libros": [
                        {
                            "id": libro.id,
                            "titulo": libro.titulo
                        }
                        for libro in autor.libros
                    ]
                }
                for autor in autores
            ]
        }


# --------------------------------------------------
# 5. CONSULTAR UN AUTOR ESPECÍFICO CON SUS LIBROS
# --------------------------------------------------

@app.get("/api/autores/{id}")
def obtener_autor(id: int):

    with SessionLocal() as db:

        consulta = (
            select(Autor)
            .options(selectinload(Autor.libros))
            .where(Autor.id == id)
        )

        autor = db.execute(consulta).scalars().first()

        if autor is None:
            raise HTTPException(
                status_code=404,
                detail="Autor no encontrado"
            )

        return {
            "id": autor.id,
            "nombre": autor.nombre,
            "libros": [
                {
                    "id": libro.id,
                    "titulo": libro.titulo
                }
                for libro in autor.libros
            ]
        }


# --------------------------------------------------
# 6. CONSULTAR TODOS LOS LIBROS
# --------------------------------------------------

@app.get("/api/libros")
def listar_libros():

    with SessionLocal() as db:

        libros = db.execute(
            select(Libro).order_by(Libro.id)
        ).scalars().all()

        return {
            "libros": [
                {
                    "id": libro.id,
                    "titulo": libro.titulo
                }
                for libro in libros
            ]
        }

==============================================================================

VERIFICACIÓN DEL RESULTADO · 3 casos · app.py

==============================================================================

✅ 01. Los autores llegan con sus libros
✅ 02. Un autor concreto trae sus libros
✅ 03. El listado de libros sigue disponible

------------------------------------------------------------------------------

RESULTADO: 3/3 casos correctos. ¡Resultado logrado!

✅ Se usa carga ansiosa

------------------------------------------------------------------------------

RESULTADO: 1/1 comprobaciones correctas. ¡Resultado logrado!

```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Prevención del problema N+1 de consultas en bucle

* [ x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [ x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [ x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> Durante la verificación encontré que las tres pruebas devolvían un error HTTP 500 en lugar de una respuesta JSON con estado 200. Esto me permitió identificar que la implementación todavía tenía problemas al consultar o devolver los datos relacionados entre autores y libros. Comprendí que no basta con utilizar Eager Loading, también es necesario revisar que las relaciones se carguen correctamente y que los datos puedan convertirse a JSON antes de responder la petición. Por eso es importante revisar las consultas, las sesiones y la serialización para evitar errores internos del servidor.

---
**Firma digital:** [Amanda1Serrato]

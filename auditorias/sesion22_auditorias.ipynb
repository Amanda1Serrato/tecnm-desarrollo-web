# Bitácora de Requerimientos y Auditoría IA — Sesión 22
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Modelado Relacional (1:1, 1:N, N:M) con ORMs  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Nombre Completo]  
**Matrícula:** [No. de Control]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Definición de tablas relacionales en código  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad que encontré fue relacionar correctamente las tablas de autores y libros, porque tenía que definir las llaves primarias y foráneas para que cada libro quedara asociado con su autor. También fue un poco complicado hacer que los libros se mostraran dentro de la información del autor sin tener que realizar todo manualmente.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Utilizar Python 3.10 o superior, FastAPI y SQLAlchemy con SQLite en Google Colab.|
| **Rol (R)** |La IA actuará como arquitecto de software especializado en APIs REST y modelado de bases de datos relacionales.|
| **Especificación (E)** | MCrear los modelos Autor y Libro con una relación 1:N, utilizando llaves primarias, llaves foráneas y relationship. Implementar rutas para registrar autores, registrar libros asociados y consultar autores con sus libros. |
| **Output (O)** |Obtener un archivo app.py funcional, una base de datos biblioteca.db y las cinco pruebas de verificación aprobadas.|

### 2.2 Prompt Estructurado
```text
[Actúa como un arquitecto de software especializado en Python,
FastAPI y SQLAlchemy.

Necesito desarrollar una API REST para una biblioteca utilizando
SQLite como base de datos.

Crea dos modelos:
- Autor: debe tener id y nombre.
- Libro: debe tener id, titulo, anio y autor_id como llave foránea.

Establece una relación uno a muchos (1:N), donde un autor pueda
tener varios libros, utilizando relationship() y ForeignKey().

Implementa los siguientes endpoints:
- POST /api/autores para registrar un autor.
- POST /api/autores/{id}/libros para registrar un libro asociado
  a un autor existente.
- GET /api/autores/{id} para consultar un autor y mostrar sus libros.
- GET /api/libros para listar todos los libros.

Utiliza SQLAlchemy para manejar la base de datos, Pydantic
para validar los datos y códigos HTTP adecuados.
Si el autor no existe, devuelve un error 404.
Incluye la creación automática de las tablas y entrega el código
completo en un archivo app.py.]
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

app = FastAPI(title="Tu relación autor → libros se verá así")

# --------------------------------
# 1. Configuración de la base de datos
# --------------------------------

DATABASE_URL = "sqlite:///./biblioteca.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# --------------------------------
# 2. Modelo ORM: Autor
# --------------------------------

class Autor(Base):
    __tablename__ = "autores"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(150), nullable=False)

    libros = relationship(
        "Libro",
        back_populates="autor",
        cascade="all, delete-orphan"
    )


# --------------------------------
# 3. Modelo ORM: Libro
# --------------------------------

class Libro(Base):
    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    anio = Column(Integer, nullable=False)

    autor_id = Column(
        Integer,
        ForeignKey("autores.id"),
        nullable=False
    )

    autor = relationship(
        "Autor",
        back_populates="libros"
    )


# --------------------------------
# 4. Crear las tablas
# --------------------------------

Base.metadata.create_all(bind=engine)


# --------------------------------
# 5. Esquemas de entrada
# --------------------------------

class AutorEntrada(BaseModel):
    nombre: str = Field(min_length=1, max_length=150)


class LibroEntrada(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    anio: int = Field(ge=0)


# --------------------------------
# 6. Registrar un autor
# --------------------------------

@app.post("/api/autores", status_code=201)
def crear_autor(datos: AutorEntrada):

    db = SessionLocal()

    try:
        autor = Autor(nombre=datos.nombre)

        db.add(autor)
        db.commit()
        db.refresh(autor)

        return {
            "id": autor.id,
            "nombre": autor.nombre
        }

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error al registrar el autor"
        )

    finally:
        db.close()


# --------------------------------
# 7. Registrar un libro asociado
# --------------------------------

@app.post("/api/autores/{autor_id}/libros", status_code=201)
def crear_libro(autor_id: int, datos: LibroEntrada):

    db = SessionLocal()

    try:
        autor = db.query(Autor).filter(
            Autor.id == autor_id
        ).first()

        if autor is None:
            raise HTTPException(
                status_code=404,
                detail="Autor no encontrado"
            )

        libro = Libro(
            titulo=datos.titulo,
            anio=datos.anio,
            autor=autor
        )

        db.add(libro)
        db.commit()
        db.refresh(libro)

        return {
            "id": libro.id,
            "titulo": libro.titulo,
            "anio": libro.anio,
            "autor_id": libro.autor_id
        }

    except HTTPException:
        raise

    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error al registrar el libro"
        )

    finally:
        db.close()


# --------------------------------
# 8. Consultar autor y sus libros
# --------------------------------

@app.get("/api/autores/{autor_id}")
def obtener_autor(autor_id: int):

    db = SessionLocal()

    try:
        autor = db.query(Autor).filter(
            Autor.id == autor_id
        ).first()

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

    finally:
        db.close()


# --------------------------------
# 9. Consultar todos los libros
# --------------------------------

@app.get("/api/libros")
def listar_libros():

    db = SessionLocal()

    try:
        libros = db.query(Libro).all()

        return {
            "libros": [
                {
                    "id": libro.id,
                    "titulo": libro.titulo,
                    "anio": libro.anio,
                    "autor_id": libro.autor_id
                }
                for libro in libros
            ]
        }

    finally:
        db.close()

==============================================================================

VERIFICACIÓN DEL RESULTADO · 4 casos · app.py

==============================================================================

✅ 01. Se crea el autor
✅ 02. Se crea el libro asociado
✅ 03. El autor devuelve sus libros
✅ 04. El listado de libros funciona

------------------------------------------------------------------------------

RESULTADO: 4/4 casos correctos. ¡Resultado logrado!

✅ La relación ORM está declarada
------------------------------------------------------------------------------
RESULTADO: 1/1 comprobaciones correctas. ¡Resultado logrado!
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de integridad referencial y cascadas

* [ x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [ x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [ x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> La IA no contempló inicialmente qué respuesta debía devolver cuando se intentaba registrar un libro con un autor que no existía. Lo corregí agregando una validación para comprobar que el autor estuviera registrado antes de guardar el libro. Si no existe, la API devuelve un código 404 Not Found. También utilicé llaves foráneas para mantener la relación entre autores y libros y evitar registros sin una relación válida.

---
**Firma digital:** [amanda1serrato]

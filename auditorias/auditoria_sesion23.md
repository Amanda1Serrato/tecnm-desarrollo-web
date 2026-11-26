# Bitácora de Requerimientos y Auditoría IA — Sesión 23
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Operaciones CRUD Transaccionales y Async Sessions  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Amanda Ideth Serrato Carmona]  
**Matrícula:** [23531056]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Operaciones de inserción y consulta manual  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad que encontré fue realizar las operaciones de inserción y consulta sin cometer errores al enviar los datos. También tuve que revisar que los campos estuvieran completos y que las respuestas fueran correctas. Al hacerlo manualmente era más complicado controlar los errores y asegurar que la información se guardara correctamente en la base de datos.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** |FastAPI con Python, SQLAlchemy asíncrono, SQLite y aiosqlite.|
| **Rol (R)** | Arquitecto de software especializado en APIs RESTful y bases de datos asíncronas.|
| **Especificación (E)** | Implementar un CRUD de libros utilizando AsyncSession, await y commit. Crear, consultar, actualizar y eliminar libros, controlando los errores y utilizando los códigos HTTP correspondientes. |
| **Output (O)** | Código completo y organizado en app.py, con modelos Pydantic, sesiones asíncronas y respuestas HTTP correctas.|

### 2.2 Prompt Estructurado
```text
[Contexto: Trabajo con Python, FastAPI, SQLAlchemy y SQLite.

Rol: Actúa como desarrollador especializado en APIs RESTful y bases de datos asíncronas.

Especificación: Implementa un CRUD de libros usando create_async_engine, aiosqlite, AsyncSession, async def y await. Incluye creación, consulta, actualización y eliminación, con respuestas HTTP 201, 200, 204 y 404.

Output: Entrega el código completo y funcional de app.py, con validaciones y manejo de errores.]
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py

from fastapi import FastAPI, HTTPException, Depends, Response
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import Integer, String, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)

# 1. Configuración de SQLite asíncrono
DATABASE_URL = "sqlite+aiosqlite:///./biblioteca.db"

engine = create_async_engine(
    DATABASE_URL,
    echo=False
)

SessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 2. Base de datos
class Base(DeclarativeBase):
    pass


# 3. Tabla de libros
class Libro(Base):
    __tablename__ = "libros"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    titulo: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    anio: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )


# 4. Modelos de entrada y salida
class LibroEntrada(BaseModel):
    titulo: str = Field(min_length=1, max_length=200)
    anio: int = Field(ge=1500, le=2026)


class LibroRespuesta(BaseModel):
    id: int
    titulo: str
    anio: int

    model_config = ConfigDict(from_attributes=True)


class ListaLibros(BaseModel):
    libros: list[LibroRespuesta]


# 5. Aplicación FastAPI
app = FastAPI(
    title="Biblioteca CRUD Asíncrona",
    version="1.0.0"
)


# 6. Obtener sesión y asegurar que exista la tabla
async def obtener_sesion():
    async with engine.begin() as conexion:
        await conexion.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        yield session


# 7. CREATE: Crear un libro
@app.post(
    "/api/libros",
    response_model=LibroRespuesta,
    status_code=201
)
async def crear_libro(
    datos: LibroEntrada,
    session: AsyncSession = Depends(obtener_sesion)
):
    nuevo_libro = Libro(
        titulo=datos.titulo,
        anio=datos.anio
    )

    session.add(nuevo_libro)

    await session.commit()
    await session.refresh(nuevo_libro)

    return nuevo_libro


# 8. READ: Consultar todos los libros
@app.get(
    "/api/libros",
    response_model=ListaLibros
)
async def listar_libros(
    session: AsyncSession = Depends(obtener_sesion)
):
    resultado = await session.execute(
        select(Libro).order_by(Libro.id)
    )

    libros = resultado.scalars().all()

    return {"libros": libros}


# 9. READ: Consultar un libro por ID
@app.get(
    "/api/libros/{libro_id}",
    response_model=LibroRespuesta
)
async def consultar_libro(
    libro_id: int,
    session: AsyncSession = Depends(obtener_sesion)
):
    libro = await session.get(Libro, libro_id)

    if libro is None:
        raise HTTPException(
            status_code=404,
            detail="El libro no existe"
        )

    return libro


# 10. UPDATE: Actualizar un libro
@app.put(
    "/api/libros/{libro_id}",
    response_model=LibroRespuesta
)
async def actualizar_libro(
    libro_id: int,
    datos: LibroEntrada,
    session: AsyncSession = Depends(obtener_sesion)
):
    libro = await session.get(Libro, libro_id)

    if libro is None:
        raise HTTPException(
            status_code=404,
            detail="El libro no existe"
        )

    libro.titulo = datos.titulo
    libro.anio = datos.anio

    await session.commit()
    await session.refresh(libro)

    return libro


# 11. DELETE: Eliminar un libro
@app.delete(
    "/api/libros/{libro_id}",
    status_code=204
)
async def eliminar_libro(
    libro_id: int,
    session: AsyncSession = Depends(obtener_sesion)
):
    libro = await session.get(Libro, libro_id)

    if libro is None:
        raise HTTPException(
            status_code=404,
            detail="El libro no existe"
        )

    await session.delete(libro)
    await session.commit()

    return Response(status_code=204)

==============================================================================

VERIFICACIÓN DEL RESULTADO · 5 casos · app.py

==============================================================================

✅ 01. Crear un libro
✅ 02. Listar los libros
✅ 03. Actualizar el libro
✅ 04. Eliminar el libro
✅ 05. El libro eliminado ya no existe

------------------------------------------------------------------------------

RESULTADO: 5/5 casos correctos. ¡Resultado logrado!

✅ La persistencia es asíncrona
------------------------------------------------------------------------------
RESULTADO: 1/1 comprobaciones correctas. ¡Resultado logrado!
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de inserción doble y manejo de llaves únicas

* [ x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [ x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [ x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> La IA inicialmente presentó problemas al ejecutar las operaciones, ya que el servidor devolvía errores HTTP 500. Tuve que revisar la configuración de la conexión asíncrona y la creación de las tablas. También comprobé que al consultar un libro inexistente se devolviera un error 404 y que al eliminarlo se utilizara el código 204. Con estas revisiones busqué que las respuestas fueran correctas y que no se mostraran errores internos del servidor.

---
**Firma digital:** [Amanda1Serrato]

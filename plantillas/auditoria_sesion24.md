# Bitácora de Requerimientos y Auditoría IA — Sesión 24
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Migraciones de Base de Datos con Alembic / Phinx  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Amanda Ideth Serrato Carmona]  
**Matrícula:** [23531056]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Script SQL de actualización de esquema  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad que encontré fue crear y modificar la estructura de la base de datos manualmente, ya que tenía que revisar que las tablas y sus campos estuvieran correctamente definidos. También se me complicó asegurar que los cambios pudieran revertirse sin dejar información o estructuras innecesarias.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python, SQLAlchemy, Alembic y SQLite trabajando en Google Colab.|
| **Rol (R)** | Desarrollador especializado en bases de datos y migraciones.|
| **Especificación (E)** | Crear un modelo Libro y configurar Alembic para realizar migraciones con upgrade y downgrade. |
| **Output (O)** | Entregar los archivos necesarios con código organizado para crear y revertir la tabla libros. |

### 2.2 Prompt Estructurado
```text
[Contexto: Trabajo con Python, SQLAlchemy, Alembic y SQLite.

Rol: Actúa como desarrollador especializado en bases de datos.

Especificación: Configura Alembic y crea una migración que permita crear y eliminar la tabla libros mediante upgrade y downgrade.

Output: Entrega los archivos modelos.py, alembic.ini, migrations/env.py y 0001_crear_libros.py con código completo y funcional.]
```

---

## 3. Código Devuelto por el Modelo
```python

%%writefile modelos.py

from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Libro(Base):
    __tablename__ = "libros"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    titulo: Mapped[str] = mapped_column(
        String(80),
        nullable=False
    )

    anio: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

✅ El modelo Libro existe
✅ Alembic está configurado
✅ Env.py conoce los metadatos

------------------------------------------------------------------------------

RESULTADO: 3/3 comprobaciones correctas. ¡Resultado logrado!

✅ La migración crea y revierte la tabla libros
------------------------------------------------------------------------------
RESULTADO: 1/1 comprobaciones correctas. ¡Resultado logrado!
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de actualización (upgrade) y reversión (downgrade)

* [ x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [ x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [ x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> En esta actividad no se trabajó directamente con códigos HTTP, sino con migraciones de bases de datos. Durante la verificación se detectó que la migración no estaba creando y revirtiendo correctamente la tabla libros. Para corregirlo revisé las funciones upgrade() y downgrade(), agregando op.create_table() para crear la tabla y op.drop_table() para eliminarla.



---
**Firma digital:** [Amanda1Serrato]

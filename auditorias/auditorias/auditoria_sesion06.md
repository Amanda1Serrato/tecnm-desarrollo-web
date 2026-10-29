 Sesión 06 · Validación Estricta, Constraints y Params Query/Body
Desarrollo de Aplicaciones Web (DAB-2201) · TecNM Cancún
Docente: MCC. Iván Márquez Larios (ijmarquezl)
Repositorio: https://github.com/ijmarquezl/tecnm-desarrollo-web

La pregunta de hoy: ¿Dónde pones los límites: en el cliente o en el servidor?

🖥️ Así se verá el resultado final
$ curl -X POST http://127.0.0.1:8000/api/libros \
       -H "Content-Type: application/json" \
       -d '{"titulo":"Rayuela","anio":1963,"precio":250.5}'
HTTP/1.1 201 Created
{"id":1,"titulo":"Rayuela","anio":1963,"precio":250.5}

$ curl -X POST http://127.0.0.1:8000/api/libros \
       -H "Content-Type: application/json" \
       -d '{"titulo":"Ya","anio":1200,"precio":-5}'
HTTP/1.1 422 Unprocessable Entity

$ curl "http://127.0.0.1:8000/api/libros?limite=0"
HTTP/1.1 422 Unprocessable Entity
Un título de dos letras, un año de 1200 y un precio negativo son datos, no errores del servidor.

No hay pasos intermedios. El cuaderno declara el resultado que debe existir al final; tú decides la estructura, los modelos y el orden de tu implementación. La celda de verificación compara tu resultado con este contrato.

🎯 Al finalizar podrás
Aplicar restricciones de negocio con Field y Query.
Explicar por qué el servidor no puede confiar en el cliente.
Verificar errores 422 por rangos, longitudes y valores negativos.
✅ Criterios de aceptación
El verificador ejecutará estos casos. Cada uno debe quedar en verde:

 Un libro dentro de los límites se crea → HTTP 201
 Un título demasiado corto produce 422 → HTTP 422
 Un año fuera de rango produce 422 → HTTP 422
 Un precio no positivo produce 422 → HTTP 422
 El límite de paginación debe ser al menos 1 → HTTP 422
 Un límite válido responde 200 → HTTP 200
🧩 El reto
Implementa el contrato de libros con reglas de negocio explícitas y un listado paginado.

Requisitos del contrato

titulo: entre 3 y 80 caracteres.
anio: entre 1450 y 2100.
precio: mayor que 0.
El parámetro limite de GET /api/libros acepta entre 1 y 100.
Los datos inválidos producen 422; los válidos, 201.
Pista conceptual: Field(min_length=3, max_length=80, ge=1450, le=2100, gt=0) describe el resultado esperado directamente en el DTO. La lógica de validación no se repite en cada endpoint.

📦 Entregable
Cuaderno en verde y bitácora auditorias/auditoria_sesion06.md con la tabla de restricciones.

⚙️ Preparación del entorno
Ejecuta esta celda una sola vez. Instala las herramientas del track Python / FastAPI y descarga el motor de verificación del repositorio. No necesitas instalar nada en tu computadora: todo corre en Colab.


[1]
10 s
import os, sys
print("⏳ Preparando el entorno de Desarrollo Web...")
!pip install -q fastapi uvicorn httpx pydantic "passlib[bcrypt]" bcrypt python-jose[cryptography] PyJWT "sqlalchemy[asyncio]" greenlet aiosqlite alembic python-multipart
!wget -q -O verificar.py https://raw.githubusercontent.com/ijmarquezl/tecnm-desarrollo-web/c275993ba69ef2a8cf650b2f127b55c8356279d7/laboratorios/verificar.py
if not os.path.exists("verificar.py") or os.path.getsize("verificar.py") < 1000:
    raise RuntimeError("No se pudo descargar verificar.py. Revisa tu conexión o abre el cuaderno desde el repositorio del curso.")
print("✅ Entorno listo")
print("Python:", sys.version.split()[0])
print("Motor de verificación:", os.path.getsize("verificar.py"), "bytes")

⏳ Preparando el entorno de Desarrollo Web...
✅ Entorno listo
Python: 3.13.18
Motor de verificación: 13395 bytes
🧩 El reto: escribe el resultado
Crea el o los archivos del contrato. No hay una plantilla de pasos: el esqueleto solo te da el punto de partida. Todo lo que sigue lo decides tú.

Archivos que debes producir: app.py

📄 app.py
Archivo principal de la implementación.


[2]
0 s

%%writefile app.py
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Validación estricta de libros")


# Modelo con las reglas de validación
class LibroEntrada(BaseModel):
    titulo: str = Field(min_length=3, max_length=80)
    anio: int = Field(ge=1450, le=2100)
    precio: float = Field(gt=0)


# Lista para guardar los libros registrados
libros = []


@app.post("/api/libros", status_code=201)
def crear_libro(libro: LibroEntrada):
    nuevo_libro = {
        "id": len(libros) + 1,
        "titulo": libro.titulo,
        "anio": libro.anio,
        "precio": libro.precio
    }

    libros.append(nuevo_libro)
    return nuevo_libro


@app.get("/api/libros")
def listar_libros(
    limite: int = Query(default=10, ge=1, le=100)
):
    return {"libros": libros[:limite]}

Writing app.py
🧪 Tu contrato C-R-E-O
Antes de pedir ayuda a la IA, escribe el contrato que describe el resultado. Esto alimenta tu bitácora y te obliga a pensar como arquitecto:

Elemento	Tu definición
Contexto	Python 3 y FastAPI con Pydantic v2 para validar los datos.
Rol	Actuar como desarrollador de una API REST que valide libros.
Especificación	Crear y listar libros, validar el título de 3 a 80 caracteres, el año de 1450 a 2100, el precio mayor que cero y el límite entre 1 y 100.
Output	Código completo en app.py, con validaciones automáticas y respuestas HTTP 201, 200 o 422 según el resultado.
No pegues código de la IA sin auditarlo. La responsabilidad técnica del resultado es tuya.

🔍 Verificación del resultado
Ejecuta esta celda cuando tu implementación esté lista. La verificación no modifica tu código: solo observa el comportamiento y compara con el contrato. Si algo falla, el mensaje te dice qué esperaba y qué recibió.


[3]
1 s
from verificar import probar_http

casos = [{'descripcion': 'Un libro dentro de los límites se crea',
  'metodo': 'POST',
  'ruta': '/api/libros',
  'json': {'titulo': 'Rayuela', 'anio': 1963, 'precio': 250.5},
  'estado': 201,
  'json_contiene': {'id': 1, 'titulo': 'Rayuela', 'anio': 1963}},
 {'descripcion': 'Un título demasiado corto produce 422',
  'metodo': 'POST',
  'ruta': '/api/libros',
  'json': {'titulo': 'Ya', 'anio': 1963, 'precio': 250.5},
  'estado': 422},
 {'descripcion': 'Un año fuera de rango produce 422',
  'metodo': 'POST',
  'ruta': '/api/libros',
  'json': {'titulo': 'Rayuela', 'anio': 1200, 'precio': 250.5},
  'estado': 422},
 {'descripcion': 'Un precio no positivo produce 422',
  'metodo': 'POST',
  'ruta': '/api/libros',
  'json': {'titulo': 'Rayuela', 'anio': 1963, 'precio': 0},
  'estado': 422},
 {'descripcion': 'El límite de paginación debe ser al menos 1',
  'metodo': 'GET',
  'ruta': '/api/libros?limite=0',
  'estado': 422},
 {'descripcion': 'Un límite válido responde 200', 'metodo': 'GET', 'ruta': '/api/libros?limite=5', 'estado': 200}]

probar_http(casos, archivo="app.py", limpiar=[], env={})

==============================================================================
VERIFICACIÓN DEL RESULTADO · 6 casos · app.py
==============================================================================
✅ 01. Un libro dentro de los límites se crea
✅ 02. Un título demasiado corto produce 422
✅ 03. Un año fuera de rango produce 422
✅ 04. Un precio no positivo produce 422
✅ 05. El límite de paginación debe ser al menos 1
✅ 06. Un límite válido responde 200
------------------------------------------------------------------------------
RESULTADO: 6/6 casos correctos. ¡Resultado logrado!
📝 Cierre y bitácora
Copia la plantilla plantillas/auditoria_sesion06.md a auditorias/auditoria_sesion06.md en tu fork.
Responde con tus palabras:
¿Qué resultado te costó más alcanzar y por qué? Me costó más configurar las validaciones para que cada dato tuviera sus propios límites, porque tenía que asegurarme de que los valores incorrectos generaran un error 422.
¿Qué decisión de diseño tomaste que no estaba escrita en el contrato? Decidí guardar los libros en una lista y asignarles un ID automáticamente para poder registrarlos y consultarlos.
¿Qué error detectó la verificación que tú no habías previsto? La verificación me ayudó a comprobar que también debía validar el límite de paginación y rechazar valores como cero, además de validar los datos del libro.
Haz commit de tu cuaderno ejecutado y de tu bitácora.
La sesión termina cuando el resultado está en verde, no cuando el código "parece funcionar".

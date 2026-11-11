# Bitácora de Requerimientos y Auditoría IA — Sesión 13
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Manejo de Sesiones Stateful vs Stateless Tokens  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Amanda Ideth Serrato Carmona]  
**Matrícula:** [23531056]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Simulador de tabla de sesiones en memoria  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad que encontré fue controlar manualmente las sesiones y comprobar si el usuario realmente había iniciado sesión. También se me complicó manejar las cookies, porque tenía que asegurarme de que el servidor reconociera al usuario en cada petición. Otro problema fue eliminar correctamente la sesión cuando se cerraba, para que ya no se pudiera acceder al perfil.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Se está utilizando Python con FastAPI para crear una API que permita iniciar y cerrar sesiones. El trabajo se realiza en Google Colab y las sesiones se almacenan temporalmente en memoria. |
| **Rol (R)** |Actúa como un desarrollador especializado en Python y FastAPI, encargado de implementar un sistema de autenticación mediante sesiones con estado y cookies HttpOnly.|
| **Especificación (E)** | Crear tres rutas:
- POST /api/login: validar el usuario y la contraseña, crear una sesión y enviar una cookie HttpOnly.
- GET /api/perfil: comprobar la cookie y mostrar el usuario si la sesión es válida. Si no, responder con error 401.
- POST /api/logout: eliminar la sesión, borrar la cookie y responder con código 204.|
| **Output (O)** | Entregar el código completo del archivo app.py, utilizando Python y FastAPI, con las tres rutas funcionando y respuestas HTTP de acuerdo con los requisitos de la actividad.|

### 2.2 Prompt Estructurado
```text
[Necesito crear una API para manejar sesiones con estado
(Stateful) utilizando cookies HttpOnly.

El sistema debe cumplir con lo siguiente:

1. Crear la ruta POST /api/login para validar al
usuario ana con contraseña secreta.

2. Cuando los datos sean correctos, generar un
identificador único para la sesión y guardarlo
en una tabla o diccionario en memoria.

3. Enviar una cookie llamada session_id con
HttpOnly, Path=/ y SameSite=Lax.

4. Crear GET /api/perfil para comprobar si la cookie
corresponde a una sesión activa y devolver el usuario.

5. Crear POST /api/logout para eliminar la sesión
del servidor y borrar la cookie.

6. Si la sesión no existe o ya fue cerrada,
devolver HTTP 401.

7. El logout debe responder HTTP 204 sin contenido.

Utiliza FastAPI, Pydantic y Python.
Organiza el código y utiliza respuestas HTTP
correctas. Evita errores internos 500.

Entrega el código completo de app.py y explica
brevemente cómo funciona cada ruta.]
```

---

## 3. Código Devuelto por el Modelo
```python
from fastapi import FastAPI, HTTPException, Response, Cookie
from pydantic import BaseModel
import secrets

app = FastAPI(title="Manejo de Sesiones Stateful")

usuarios = {
    "ana": "secreta"
}

sesiones = {}

class Login(BaseModel):
    usuario: str
    password: str


@app.post("/api/login")
def iniciar_sesion(datos: Login, response: Response):

    if usuarios.get(datos.usuario) != datos.password:
        raise HTTPException(status_code=401)

    session_id = secrets.token_urlsafe(32)
    sesiones[session_id] = datos.usuario

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        samesite="lax",
        path="/"
    )

    return {"mensaje": "sesión iniciada"}


@app.get("/api/perfil")
def obtener_perfil(session_id: str = Cookie(default=None)):

    if not session_id or session_id not in sesiones:
        raise HTTPException(status_code=401)

    return {"usuario": sesiones[session_id]}


@app.post("/api/logout", status_code=204)
def cerrar_sesion(
    response: Response,
    session_id: str = Cookie(default=None)
):

    if session_id:
        sesiones.pop(session_id, None)

    response.delete_cookie(
        key="session_id",
        httponly=True,
        samesite="lax",
        path="/"
    )

    response.status_code = 204
    return response
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de expiración y revocación de sesión

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> Al principio, la verificación me marcó un error en la prueba de cierre de sesión, porque no estaba respondiendo correctamente con el código HTTP 204 No Content. Para solucionarlo, revisé la ruta de logout y agregué el código de respuesta 204 para asegurarme de que cumpliera con lo solicitado.

---
**Firma digital:** [Amanda1Serrato]

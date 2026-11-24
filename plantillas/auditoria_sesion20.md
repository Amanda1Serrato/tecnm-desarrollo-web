# Bitácora de Requerimientos y Auditoría IA — Sesión 20
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Hito 2: API con Inyección de Dependencias, Auth JWT y RBAC  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Amanda Ideth Serrato Carmona]  
**Matrícula:** [23531056]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Integración de autenticación y autorización en API  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad que encontré fue implementar correctamente la autenticación y los permisos de los usuarios, ya que tuve que entender cómo funcionan los tokens JWT y cómo validar que cada usuario tenga acceso únicamente a las rutas que le corresponden. También fue necesario cuidar que las contraseñas se guardaran de forma segura y no aparecieran en las respuestas.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Utilizar Python, FastAPI y Google Colab para desarrollar una API segura.|
| **Rol (R)** | La IA actuará como un asistente técnico especializado en APIs REST y seguridad web.|
| **Especificación (E)** |Implementar registro de usuarios, inicio de sesión, autenticación JWT, perfil protegido y panel administrativo con permisos por roles.|
| **Output (O)** | SObtener un archivo app.py funcional, con contraseñas hasheadas, respuestas HTTP correctas y las 7 pruebas aprobadas.|

### 2.2 Prompt Estructurado
```text
[Actúa como un desarrollador experto en Python y FastAPI,
especializado en seguridad de APIs REST.

Necesito desarrollar una API que incluya autenticación
mediante tokens JWT y autorización basada en roles (RBAC).

Implementa las siguientes funciones:

1. Registro de usuarios con contraseñas hasheadas.
2. Inicio de sesión y generación de tokens JWT.
3. Ruta /api/perfil protegida para usuarios autenticados.
4. Ruta /api/admin/panel exclusiva para administradores.
5. Validación de tokens y permisos de cada usuario.
6. Respuestas HTTP adecuadas: 200, 201, 401, 403 y 409.
7. Evitar que las contraseñas o sus hashes aparezcan
   en las respuestas.]
```

---

## 3. Código Devuelto por el Modelo
```python
%%writefile app.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

app = FastAPI(title="API Hito 2 - Seguridad")

# -----------------------------
# 1. Configuración de seguridad
# -----------------------------
SECRET_KEY = "clave-laboratorio-sesion20-cambiar"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

bearer_scheme = HTTPBearer(auto_error=False)

# -----------------------------
# 2. Modelos de datos
# -----------------------------
class UsuarioEntrada(BaseModel):
    usuario: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=100)

class UsuarioRespuesta(BaseModel):
    usuario: str
    rol: str

class TokenRespuesta(BaseModel):
    access_token: str
    token_type: str

# -----------------------------
# 3. Almacenamiento en memoria
# -----------------------------
usuarios = {}

# Administrador precargado
usuarios["admin"] = {
    "password_hash": pwd_context.hash("admin123"),
    "rol": "admin"
}

# -----------------------------
# 4. Funciones de seguridad
# -----------------------------
def verificar_password(password, password_hash):
    return pwd_context.verify(password, password_hash)

def crear_token(usuario, rol):
    datos = {
        "sub": usuario,
        "rol": rol,
        "exp": datetime.now(timezone.utc)
               + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }

    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)

# -----------------------------
# 5. Dependencia: usuario autenticado
# -----------------------------
def obtener_usuario_actual(
    credenciales: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    if credenciales is None:
        raise HTTPException(
            status_code=401,
            detail="Token requerido",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        payload = jwt.decode(
            credenciales.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        nombre_usuario = payload.get("sub")
        rol = payload.get("rol")

        if not nombre_usuario or not rol:
            raise HTTPException(
                status_code=401,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"}
            )

        usuario = usuarios.get(nombre_usuario)

        if usuario is None or usuario["rol"] != rol:
            raise HTTPException(
                status_code=401,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"}
            )

        return {
            "usuario": nombre_usuario,
            "rol": rol
        }

    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )

# -----------------------------
# 6. Dependencia: solo administrador
# -----------------------------
def obtener_admin(
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    if usuario_actual["rol"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="No tienes permisos de administrador"
        )

    return usuario_actual

# -----------------------------
# 7. Registro
# -----------------------------
@app.post("/api/registro", status_code=201)
def registrar_usuario(datos: UsuarioEntrada):
    if datos.usuario in usuarios:
        raise HTTPException(
            status_code=409,
            detail="El usuario ya existe"
        )

    usuarios[datos.usuario] = {
        "password_hash": pwd_context.hash(datos.password),
        "rol": "user"
    }

    return {
        "usuario": datos.usuario,
        "mensaje": "Usuario registrado"
    }

# -----------------------------
# 8. Login y generación de JWT
# -----------------------------
@app.post("/api/token", response_model=TokenRespuesta)
def login(datos: UsuarioEntrada):
    usuario = usuarios.get(datos.usuario)

    if usuario is None or not verificar_password(
        datos.password,
        usuario["password_hash"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    token = crear_token(datos.usuario, usuario["rol"])

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# -----------------------------
# 9. Perfil protegido
# -----------------------------
@app.get("/api/perfil")
def perfil(
    usuario_actual: dict = Depends(obtener_usuario_actual)
):
    return {
        "usuario": usuario_actual["usuario"],
        "rol": usuario_actual["rol"]
    }

# -----------------------------
# 10. Panel administrativo
# -----------------------------
@app.get("/api/admin/panel")
def panel_admin(
    administrador: dict = Depends(obtener_admin)
):
    return {
        "mensaje": "Acceso autorizado al panel administrativo",
        "usuario": administrador["usuario"],
        "rol": administrador["rol"]
    }
```
==============================================================================

VERIFICACIÓN DEL RESULTADO · 7 casos · app.py

==============================================================================

✅ 01. Registro sin filtrar contraseñas
✅ 02. Login del usuario registrado
✅ 03. El usuario accede a su perfil
✅ 04. El usuario no entra al panel admin
✅ 05. El administrador obtiene su token
✅ 06. El administrador entra al panel
✅ 07. Sin token no hay acceso

------------------------------------------------------------------------------

RESULTADO: 7/7 casos correctos. ¡Resultado logrado!
---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Suite de pruebas con usuarios legítimos e intrusos

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [ x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> Durante las pruebas comprobé que era importante diferenciar entre los errores de autenticación y autorización. El código debía responder con 401 cuando un usuario no tenía un token válido y con 403 cuando tenía un token correcto, pero no contaba con permisos de administrador

---
**Firma digital:** [Amanda1Serrato]

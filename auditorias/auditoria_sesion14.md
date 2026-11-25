# Bitácora de Requerimientos y Auditoría IA — Sesión 14
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Hashing Seguro de Contraseñas (Bcrypt / Argon2)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Amanda Ideth Serrato Carmona]  
**Matrícula:** [23531056]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Cifrado manual con Salting y Factor de Costo  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> 

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | FPython 3.10 o superior, FastAPI y bcrypt, trabajando desde Google Colab. |
| **Rol (R)** | Actuar como un desarrollador especializado en seguridad web y creación de APIs REST.|
| **Especificación (E)** | Crear las rutas de registro y login. Guardar las contraseñas mediante bcrypt, verificar las contraseñas ingresadas y evitar que se repitan los usuarios.|
| **Output (O)** |Entregar el código completo de app.py, con modelos Pydantic, hashing seguro y respuestas HTTP 201, 200, 401 y 409. |

### 2.2 Prompt Estructurado
```text
[Actúa como un desarrollador especializado en Python,
FastAPI y seguridad de aplicaciones web.

Necesito crear una API para registrar usuarios e iniciar
sesión utilizando hashing seguro con bcrypt.

El sistema debe cumplir con los siguientes requisitos:

1. Crear POST /api/registro para recibir usuario y password.

2. Utilizar bcrypt para convertir la contraseña en un hash
seguro, generando un salt automáticamente.

3. Guardar solamente el hash en el servidor.

4. Evitar que un usuario registrado pueda sobrescribir
su contraseña al intentar registrarse nuevamente.

5. Crear POST /api/login para verificar la contraseña
utilizando bcrypt.checkpw().

6. Si los datos son correctos, responder HTTP 200.

7. Si la contraseña es incorrecta, responder HTTP 401.

8. El registro debe responder HTTP 201.

9. Nunca mostrar la contraseña original ni el hash
en las respuestas de la API.

10. Utilizar modelos Pydantic y respuestas JSON.

Entrega el código completo de app.py, organizado,
seguro y fácil de comprender.]
```

---

## 3. Código Devuelto por el Modelo
```python

%%writefile app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import bcrypt

app = FastAPI(title="Registro y Login Seguro")

# Diccionario para guardar los usuarios y sus hashes
usuarios = {}

# Modelo para recibir los datos
class UsuarioEntrada(BaseModel):
    usuario: str = Field(min_length=1)
    password: str = Field(min_length=1)


# Ruta para registrar un usuario
@app.post("/api/registro", status_code=201)
def registrar_usuario(datos: UsuarioEntrada):

    # Comprobar si el usuario ya existe
    if datos.usuario in usuarios:
        raise HTTPException(
            status_code=409,
            detail="El usuario ya existe"
        )

    # Convertir la contraseña en un hash seguro
    password_hash = bcrypt.hashpw(
        datos.password.encode("utf-8"),
        bcrypt.gensalt()
    )

    # Guardar únicamente el hash
    usuarios[datos.usuario] = password_hash

    # Devolver solamente el nombre del usuario
    return {"usuario": datos.usuario}


# Ruta para iniciar sesión
@app.post("/api/login")
def iniciar_sesion(datos: UsuarioEntrada):

    # Buscar el hash del usuario
    password_hash = usuarios.get(datos.usuario)

    # Verificar que exista y comprobar la contraseña
    if password_hash is None or not bcrypt.checkpw(
        datos.password.encode("utf-8"),
        password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Usuario o contraseña incorrectos"
        )

    return {
        "usuario": datos.usuario,
        "autenticado": True
    }

==============================================================================
VERIFICACIÓN DEL RESULTADO · 3 casos · app.py
==============================================================================
✅ 01. El registro responde sin filtrar la contraseña
✅ 02. El login correcto autentica
✅ 03. La contraseña incorrecta se rechaza
------------------------------------------------------------------------------
RESULTADO: 3/3 casos correctos. ¡Resultado logrado!

```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas contra ataques de Rainbow Tables y Timing

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> Un detalle que tuve que revisar fue que las contraseñas no se mostraran en las respuestas de la API y que el sistema no guardara la contraseña original. También comprobé que se utilizara bcrypt para verificar las contraseñas y no una comparación directa de hashes.

---
**Firma digital:** [Amanda1Serrato]

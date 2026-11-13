# Bitácora de Requerimientos y Auditoría IA — Sesión 16
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** OAuth2 Password Flow y Header Authorization Bearer  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Amanda Ideth Serrato Carmona]  
**Matrícula:** [23531056]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Extracción manual del encabezado Authorization  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad que encontré fue identificar y extraer correctamente el token del encabezado Authorization, porque tenía que revisar que estuviera escrito con el formato Bearer y comprobar que fuera válido. También entendí que, si no se enviaba el token o se utilizaba otro tipo de autorización, debía rechazarse la petición con un error 401.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | 	Estoy trabajando con Python y FastAPI en Google Colab. Necesito implementar OAuth2 Password Flow utilizando las herramientas del entorno y cumplir con las pruebas solicitadas.|
| **Rol (R)** |Quiero que la IA actúe como un desarrollador especializado en FastAPI y autenticación mediante OAuth2.|
| **Especificación (E)** | Crear una ruta POST /token que reciba usuario y contraseña mediante formulario. También crear una ruta GET /api/perfil protegida con OAuth2PasswordBearer. El usuario será ana y la contraseña secreta.|
| **Output (O)** | Espero recibir el código completo de app.py, organizado y funcional, que permita iniciar sesión, generar un token y proteger el acceso al perfil del usuario.|

### 2.2 Prompt Estructurado
```text
Actúa como un desarrollador especializado en Python y FastAPI. Necesito implementar el sistema de autenticación OAuth2
Password Flow para una práctica de Desarrollo de Aplicaciones Web. Crea una ruta POST /token que reciba el nombre de usuario y la contraseña mediante un formulario utilizando OAuth2PasswordRequestForm. El usuario de prueba será ana y su contraseña será secreta. Si los datos son correctos, debe devolver un access_token y token_type con el valor bearer.
También crea una ruta GET /api/perfil protegido mediante OAuth2PasswordBearer. Si el usuario envía un token válido, debe permitir el acceso y devolver el usuario ana.Si no envía un token o utiliza un esquema diferente de Bearer, debe responder con HTTP 401 y el encabezado WWW-Authenticate: Bearer. Entrega el código completo de app.py, organizado, con comentarios y compatible con FastAPI.
```

---

## 3. Código Devuelto por el Modelo
```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI(
    title="OAuth2 Password Flow",
    version="1.0.0"
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

USUARIO = "ana"
CONTRASENA = "secreta"

@app.post("/token")
async def iniciar_sesion(
    form_data: OAuth2PasswordRequestForm = Depends()
):
    if form_data.username != USUARIO or form_data.password != CONTRASENA:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {
        "access_token": "token-ana",
        "token_type": "bearer"
    }


@app.get("/api/perfil")
async def obtener_perfil(token: str = Depends(oauth2_scheme)):

    if token != "token-ana":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return {
        "usuario": "ana"
    }
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de acceso no autorizado sin token (HTTP 401)
==============================================================================
VERIFICACIÓN DEL RESULTADO · 4 casos · app.py
==============================================================================
✅ 01. El formulario de login emite token
✅ 02. El token Bearer abre el perfil
✅ 03. Sin token se responde 401 con WWW-Authenticate
✅ 04. Un esquema distinto se rechaza
------------------------------------------------------------------------------
RESULTADO: 4/4 casos correctos. ¡Resultado logrado!

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> La IA inicialmente podía enfocarse solamente en comprobar si el token era correcto, pero también era necesario considerar las peticiones sin token y las que utilizaban otro tipo de autorización

---
**Firma digital:** [Amanda1Serrato]

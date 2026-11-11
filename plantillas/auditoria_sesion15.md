# Bitácora de Requerimientos y Auditoría IA — Sesión 15
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Autenticación Stateless con JSON Web Tokens (JWT)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Amanda Ideth Serrato Carmona]  
**Matrícula:** [23531056]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Codificación Base64Url y firma HMAC-SHA256  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> 

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python 3.10 o superior, FastAPI y la librería python-jose, trabajando desde Google Colab.|
| **Rol (R)** |Actuar como un desarrollador especializado en APIs REST, autenticación y seguridad web.|
| **Especificación (E)** | Crear una ruta para generar tokens JWT y otra para consultar el perfil. Validar las credenciales, firmar el token, establecer su expiración y rechazar tokens incorrectos o alterados.|
| **Output (O)** | Entregar el código completo de app.py, utilizando JWT, respuestas JSON y códigos HTTP 200 y 401.|

### 2.2 Prompt Estructurado
```text
[Actúa como un desarrollador especializado en Python,
FastAPI y seguridad de aplicaciones web.

Necesito crear una API que permita generar y verificar
tokens JWT utilizando firmas HMAC-SHA256.

El sistema debe cumplir con los siguientes requisitos:

1. Crear POST /api/token para recibir usuario y password.

2. Validar al usuario ana con contraseña secreta.

3. Generar un JWT utilizando el algoritmo HS256.

4. Incluir el nombre del usuario y la fecha de
expiración (exp) dentro del token.

5. Devolver access_token y token_type con valor bearer.

6. Crear GET /api/perfil para recibir el token
mediante el encabezado Authorization: Bearer.

7. Verificar la firma del token y su fecha de expiración.

8. Rechazar los tokens alterados o inválidos con HTTP 401.

9. Si no se proporciona un token, impedir el acceso
y responder con HTTP 401.

10. Utilizar una variable de entorno para guardar
la clave secreta.

Utiliza FastAPI, Pydantic y PyJWT.
Entrega el código completo de app.py, organizado,
con validaciones y manejo de errores.]
```

---

## 3. Código Devuelto por el Modelo
```python
token = jwt.encode(
    datos_token,
    SECRET_KEY,
    algorithm="HS256"
)

Verificación de la firma:

payload = jwt.decode(
    token,
    SECRET_KEY,
    algorithms=["HS256"]
)
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas con tokens alterados o firma inválida

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> Un detalle que tuve que revisar fue que los tokens alterados no provocaran un error interno del servidor. Para solucionarlo, agregué un manejo de errores que permite responder con HTTP 401 cuando la firma no es válida o el token está vencido. También comprobé que el sistema rechazara las peticiones cuando no se enviaba el encabezado Authorization o cuando el formato Bearer era incorrecto.

---
**Firma digital:** [Usuario de GitHub]

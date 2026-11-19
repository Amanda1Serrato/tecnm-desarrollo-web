# Bitácora de Requerimientos y Auditoría IA — Sesión 17
**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  
**Tema:** Control de Acceso Basado en Roles (RBAC)  
**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  
**Estudiante:** [Amanda Ideth Serrato Carmona]  
**Matrícula:** [23531056]  
**Track:** [ Python/FastAPI | PHP 8+ ]  

---

## 1. Fase 1: El Artesano (Dificultad Manual)
*Reto:* Verificación manual de permisos de usuario (Admin/User)  
*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*
> La dificultad que encontré fue diferenciar los permisos de cada usuario y validar correctamente el token. Al principio se me complicó identificar cuándo debía responder con un error 401 y cuándo con un 403, porque ambos indican que no se puede acceder a un recurso. Después comprendí que primero se debe verificar la identidad del usuario y luego comprobar si tiene permiso según su rol.

---

## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)

### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)
| Elemento C-R-E-O | Definición Técnica |
| :--- | :--- |
| **Contexto (C)** | Python 3.10+ y FastAPI en Google Colab, utilizando JWT para la autenticación.|
| **Rol (R)** | Arquitecto de software especializado en APIs REST y seguridad web.|
| **Especificación (E)** |Implementar dos usuarios con diferentes roles, incluir el rol en los claims del token y proteger las rutas según sus permisos. El admin puede entrar al panel, el usuario normal recibe 403 y quien no tenga token recibe 401. |
| **Output (O)** | Código completo en app.py, con autenticación JWT, validación de roles y respuestas HTTP correctas.|

### 2.2 Prompt Estructurado
```text
[Actúa como un desarrollador backend especializado en
Python y FastAPI.

Necesito implementar un sistema de control de acceso
basado en roles (RBAC).

Crea dos usuarios de prueba:
- admin con contraseña admin123 y rol admin.
- ana con contraseña secreta y rol user.

La ruta POST /api/token debe recibir los datos
de inicio de sesión en formato JSON, usando los
campos usuario y password.

El token JWT debe incluir el nombre del usuario,
su rol y una fecha de expiración.

La ruta GET /api/admin/panel solo debe permitir
el acceso al usuario con rol admin.

Si un usuario normal intenta entrar debe recibir
HTTP 403 y si no presenta un token válido debe
recibir HTTP 401.

La ruta GET /api/perfil debe funcionar para
cualquier usuario autenticado.

Entrega el código completo en un archivo app.py,
utilizando FastAPI, JWT y respuestas HTTP
correctas. El código debe ser compatible con
las pruebas del verificador del curso.]
```

---

## 3. Código Devuelto por el Modelo
```python
==============================================================================
VERIFICACIÓN DEL RESULTADO · 6 casos · app.py
==============================================================================
✅ 01. El administrador obtiene su token
✅ 02. El usuario normal obtiene su token
✅ 03. El admin entra al panel
✅ 04. El usuario normal recibe 403
✅ 05. Sin token recibe 401
✅ 06. El perfil funciona para el usuario normal
------------------------------------------------------------------------------
RESULTADO: 6/6 casos correctos. ¡Resultado logrado!
```

---

## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)
*Pruebas ejecutadas:* Pruebas de acceso denegado por rol insuficiente (HTTP 403)

* [x] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).
* [x] No existen respuestas HTTP `500 Internal Server Error` no capturadas.
* [x] Encabezados `Content-Type: application/json` correctamente configurados.

### Reporte Crítico
*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*
> El problema que encontré fue que inicialmente el código utilizaba un formulario para iniciar sesión, pero el verificador esperaba recibir los datos en formato JSON. También tuve que corregir la validación para que un usuario sin token recibiera 401 y uno autenticado sin permisos recibiera 403. Ajusté el código para cumplir con esos requisitos y diferenciar correctamente la autenticación de la autorización.

---
**Firma digital:** [Amanda1Serrato]

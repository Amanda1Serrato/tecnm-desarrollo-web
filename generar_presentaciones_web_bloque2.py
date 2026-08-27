#!/usr/bin/env python3
"""
Compilador de Presentaciones Enriquecidas (Bloque 2: Sesiones 11 a 20)
Materia: Desarrollo de Aplicaciones Web (DAB-2201)
Unidad: Lógica de Negocio, Controladores y Autenticación Segura
Autor: MCC. Iván Márquez Larios (ijmarquezl)
TecNM - Campus Cancún
"""

import os

TEORIA_WEB_BLOQUE_2 = {
    11: {
        "tema": "Arquitectura en Capas: Router, Servicio y Capa de Datos",
        "unidad": "Bloque 2: Lógica de Negocio, Controladores y Auth",
        "teoria_principal": {
            "titulo": "Separación de Responsabilidades y Patrón Service Layer",
            "lead": "El desacoplamiento en capas aísla la capa de transporte HTTP de las reglas del negocio y el acceso a la base de datos.",
            "tarjetas": [
                ("01. Capa de Rutas / Controladores", "Recibe la petición HTTP, valida el esquema DTO de entrada y delega la ejecución al servicio.", "No debe contener lógica de negocio ni sentencias SQL directas."),
                ("02. Capa de Servicio (Service Layer)", "Orquesta las reglas de negocio puras, cálculos de dominio y validaciones complejas.", "Es independiente del framework web; puede reutilizarse en scripts CLI, tareas en background o gRPC."),
                ("03. Capa de Acceso a Datos (Repository / DAO)", "Encapsula las operaciones de persistencia (ORM / SQL) y transacciones.", "Permite cambiar el motor de base de datos sin alterar la lógica de negocio.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Flujo Unidireccional de Datos en Memoria",
            "descripcion": "Ciclo de vida de los objetos a través de las capas de la aplicación:",
            "tarjetas": [
                ("Transformación DTO -> Entidad -> DTO", "El Router pasa DTOs al Servicio; el Servicio opera con Entidades de Dominio y devuelve DTOs de salida.", "Previene la fuga accidental de modelos internos o contraseñas al cliente."),
                ("Aislamiento de Pruebas Unitarias", "Permite mockear la capa de datos en memoria para probar las reglas de negocio en milisegundos sin tocar la base de datos.", "Aumenta la cobertura y velocidad del pipeline CI/CD.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Arquitectura en Capas",
            "items": [
                "Controladores 'Gordos' (*Fat Controllers*) con cientos de líneas mezclando parsing HTTP, SQL y lógica de negocio.",
                "Saltarse la capa de servicio invocando consultas de base de datos directamente desde los endpoints.",
                "Dependencia circular entre servicios al no definir interfaces o contratos claros."
            ]
        }
    },
    12: {
        "tema": "Inyección de Dependencias (FastAPI Depends / Contenedor IoC)",
        "unidad": "Bloque 2: Lógica de Negocio, Controladores y Auth",
        "teoria_principal": {
            "titulo": "Inversión de Control (IoC) y Gestión de Recursos",
            "lead": "La inyección de dependencias permite que los componentes reciban sus colaboradores externos en lugar de instanciarlos directamente.",
            "tarjetas": [
                ("01. Inversión de Control (IoC)", "En lugar de hacer `servicio = UsuarioService()` dentro del endpoint, el framework inyecta la instancia lista para usar.", "Promueve el bajo acoplamiento y la alta cohesión del código."),
                ("02. Sistema `Depends()` en FastAPI", "Declara dependencias como parámetros de función evaluados automáticamente en cada request.", "Permite componer grafos de dependencias jerárquicos (ej. Auth -> Permisos -> Base de Datos)."),
                ("03. Ciclo de Vida por Petición (Request-Scoped)", "Garantiza que recursos compartidos (como conexiones de DB) se abran al inicio de la petición y se cierren al terminar.", "Utiliza generadores (`yield`) para asegurar limpieza determinista de recursos.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Gestión de Contexto y Limpieza Automática",
            "descripcion": "Patrón Context Manager en dependencias web:",
            "tarjetas": [
                ("Dependencias con Yield", "`def get_db(): db = Session(); try: yield db; finally: db.close()`.", "El bloque `finally` se ejecuta siempre, incluso si el endpoint lanza una excepción HTTP."),
                ("Sustitución en Pruebas (Dependency Overrides)", "`app.dependency_overrides[get_db] = get_test_db`.", "Permite inyectar bases de datos SQLite en memoria durante las pruebas automatizadas.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla en Inyección de Dependencias",
            "items": [
                "Instanciar conexiones de base de datos como variables globales sin control de pool ni cierre por petición.",
                "Dependencias con estado mutable compartido entre hilos (*Race Conditions* en concurrencia).",
                "Olvidar el bloque `finally` provocando fugas de conexiones (*Connection Leaks*) en la base de datos."
            ]
        }
    },
    13: {
        "tema": "Manejo de Sesiones Stateful vs Stateless Tokens",
        "unidad": "Bloque 2: Lógica de Negocio, Controladores y Auth",
        "teoria_principal": {
            "titulo": "Paradigmas de Autenticación y Escalabilidad Web",
            "lead": "La elección entre sesiones basadas en servidor (Stateful) o tokens criptográficos (Stateless) define la arquitectura de escalado del sistema.",
            "tarjetas": [
                ("01. Sesiones Stateful (Cookies de Sesión)", "El servidor guarda el estado del usuario en RAM/Redis y emite un `session_id` opaco en una cookie.", "Requiere replicación de memoria o almacenamiento centralizado cuando se escala horizontalmente a múltiples servidores."),
                ("02. Autenticación Stateless (Tokens)", "El estado viaja firmado digitalmente dentro del token que porta el cliente en cada petición.", "Cualquier nodo del clúster puede verificar la firma sin consultar una base de datos centralizada."),
                ("03. Criterio de Revocación", "Las sesiones stateful se revocan al instante borrando el ID del servidor; los tokens stateless requieren listas de bloqueo (*Blacklists*).", "Balance crítico entre rendimiento y control de revocación inmediata.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Escalabilidad Horizontal y Servidores Stateless",
            "descripcion": "Comportamiento bajo balanceadores de carga (Load Balancers):",
            "tarjetas": [
                ("Problema de 'Sticky Sessions'", "En arquitecturas stateful, el balanceador debe enrutar al usuario siempre al mismo servidor físico.", "Si ese nodo colapsa, la sesión del usuario se pierde."),
                ("Arquitectura Shared-Nothing", "Con tokens stateless, las peticiones pueden distribuirse aleatoriamente entre decenas de contenedores independientes.", "Facilita el auto-escalado elástico en la nube (AWS / Render / GCP).")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Gestión de Sesiones",
            "items": [
                "Almacenar objetos de sesión gigantes en memoria saturando la RAM del proceso web.",
                "Tokens stateless con tiempos de expiración infinitos que no pueden ser invalidados ante un robo de credenciales.",
                "Transmitir identificadores de sesión en la URL en lugar de encabezados o cookies seguras."
            ]
        }
    },
    14: {
        "tema": "Hashing Seguro de Contraseñas (Bcrypt / Argon2)",
        "unidad": "Bloque 2: Lógica de Negocio, Controladores y Auth",
        "teoria_principal": {
            "titulo": "Criptografía Aplicada y Protección de Credenciales",
            "lead": "Las contraseñas nunca deben almacenarse en texto plano ni con algoritmos de hash rápidos diseñados para integridad (MD5, SHA-256).",
            "tarjetas": [
                ("01. Algoritmos Lentos Adaptativos (Bcrypt / Argon2)", "Diseñados intencionalmente para consumir tiempo de CPU y memoria, mitigando ataques de fuerza bruta masiva.", "Argon2 es el estándar ganador de la Password Hashing Competition (PHC)."),
                ("02. Salting Criptográfico Automático", "Secuencia aleatoria única de bytes generada para cada contraseña antes de aplicar el hash.", "Invalida por completo el uso de tablas precalculadas (*Rainbow Tables*)."),
                ("03. Factor de Costo de Trabajo (Work Factor)", "Parámetro configurable que duplica el tiempo de cómputo por cada incremento unitario.", "Permite ajustar la dificultad del algoritmo conforme el hardware se vuelve más rápido con los años.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Prevención de Ataques de Tiempo (Timing Attacks)",
            "descripcion": "Verificación de hashes en tiempo constante:",
            "tarjetas": [
                ("Comparación en Tiempo Constante", "La función `verify()` tarda exactamente el mismo tiempo sin importar cuántos caracteres coincidan.", "Evita que un atacante deduzca la contraseña midiendo microsegundos de respuesta del servidor."),
                ("Estructura Modular del Hash", "Cadena compacta: `$2b$12$salthex...hashbytes...` que incluye algoritmo, costo, sal y resultado.", "Permite verificar contraseñas antiguas y actualizarlas al nuevo costo de forma transparente.")
            ]
        },
        "casos_borde": {
            "titulo": "Vulnerabilidades Críticas en Hashing",
            "items": [
                "Usar algoritmos obsoletos como MD5 o SHA-1 vulnerables a colisiones y cracking instantáneo por GPUs.",
                "Aplicar 'doble hash' manual (`md5(sha256(pwd))`), reduciendo la entropía del algoritmo.",
                "Registrar contraseñas en texto plano en los archivos de logs o trazas de depuración del servidor."
            ]
        }
    },
    15: {
        "tema": "Autenticación Stateless con JSON Web Tokens (JWT)",
        "unidad": "Bloque 2: Lógica de Negocio, Controladores y Auth",
        "teoria_principal": {
            "titulo": "Estructura, Firma Digital y Validación de JWT",
            "lead": "Un JWT (RFC 7519) es un contenedor compacto y seguro que transporta afirmaciones (*claims*) verificables entre partes.",
            "tarjetas": [
                ("01. Las 3 Secciones del Token", "`Header.Payload.Signature` codificadas individualmente en formato Base64Url.", "El Header indica el algoritmo (`HS256`); el Payload contiene los claims del usuario; la Firma valida la autenticidad."),
                ("02. Firma Criptográfica HMAC-SHA256", "Calculada como: `HMACSHA256(base64(Header) + '.' + base64(Payload), SECRET_KEY)`.", "Cualquier modificación al Payload por parte del cliente invalida la firma matemática."),
                ("03. Claims Estándar de Seguridad", "`sub` (ID del usuario), `iat` (fecha de emisión), `exp` (fecha de expiración estricta).", "El servidor rechaza automáticamente cualquier token cuyo tiempo actual supere `exp`.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Decodificación y Validación en Servidor",
            "descripcion": "Pipeline de verificación criptográfica sin consultar base de datos:",
            "tarjetas": [
                ("Verificación de Firma en Memoria", "El servidor recalcula el hash con su `SECRET_KEY` privada; si coincide con la firma recibida, el token es legítimo.", "Operación puramente matemática en memoria RAM con costo sub-milisegundo."),
                ("Manejo de Excepciones JWT", "Captura de `ExpiredSignatureError` (HTTP 401) y `JWTError` (firma manipulada).", "Garantiza mensajes de error claros sin filtrar detalles internos.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla y Vulnerabilidades JWT",
            "items": [
                "Guardar información sensible (contraseñas, tarjetas de crédito) en el Payload, recordando que Base64 no es cifrado.",
                "Usar claves secretas débiles (`SECRET_KEY = '123456'`) susceptibles a ataques de diccionario offline.",
                "Aceptar el algoritmo `'none'` en el Header desactivando la verificación de firma."
            ]
        }
    },
    16: {
        "tema": "OAuth2 Password Flow y Header Authorization Bearer",
        "unidad": "Bloque 2: Lógica de Negocio, Controladores y Auth",
        "teoria_principal": {
            "titulo": "Protocolo de Autorización Estándar y Esquema Bearer",
            "lead": "OAuth2 define flujos estandarizados para que las aplicaciones intercambien credenciales por tokens de acceso.",
            "tarjetas": [
                ("01. Endpoint `/token` (OAuth2 Password Flow)", "Recibe credenciales mediante `application/x-www-form-urlencoded` con campos `username` y `password`.", "Valida las credenciales contra la base de datos y devuelve un JSON con `access_token` y `token_type: bearer`."),
                ("02. Encabezado `Authorization: Bearer <token>`", "El estándar HTTP para enviar el token de acceso en cada petición protegida subsecuente.", "Separado del cuerpo de datos para facilitar el filtrado en proxies y firewalls."),
                ("03. Código HTTP 401 Unauthorized", "Emitido con el encabezado `WWW-Authenticate: Bearer` cuando el token está ausente, vencido o es inválido.", "Indica al cliente que debe re-autenticarse para obtener un nuevo token.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Integración con OpenAPI y Swagger UI",
            "descripcion": "Esquema `OAuth2PasswordBearer` en FastAPI:",
            "tarjetas": [
                ("Inyección de Seguridad en Swagger", "Agrega el botón interactivo 'Authorize' en la documentación `/docs`.", "Swagger UI almacena el token y lo inyecta automáticamente en los encabezados de cada prueba."),
                ("Dependencia `get_current_user`", "Función central reutilizable que extrae el token, verifica el JWT y retorna el usuario autenticado.", "Se inyecta con `Depends(get_current_user)` en cualquier ruta protegida.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Flujos OAuth2",
            "items": [
                "Enviar credenciales en parámetros de consulta URL (`?user=x&pass=y`) quedando expuestas en logs de servidores proxy.",
                "Omitir el encabezado `WWW-Authenticate` en respuestas 401 violando el estándar RFC 6750.",
                "No renovar tokens mediante Refresh Tokens obligando al usuario a iniciar sesión repetidamente."
            ]
        }
    },
    17: {
        "tema": "Control de Acceso Basado en Roles (RBAC)",
        "unidad": "Bloque 2: Lógica de Negocio, Controladores y Auth",
        "teoria_principal": {
            "titulo": "Autorización Granular y Jerarquía de Privilegios",
            "lead": "La autenticación responde '¿Quién eres?'; la autorización responde '¿Tienes permiso para ejecutar esta acción?'.",
            "tarjetas": [
                ("01. Modelo RBAC (Role-Based Access Control)", "Los usuarios se asocian a roles (`admin`, `docente`, `estudiante`), y los roles poseen permisos sobre recursos.", "Desacopla la gestión de usuarios individuales de la configuración de permisos."),
                ("02. Claim de Rol en JWT", "El token transporta el rol del usuario: `{'sub': '123', 'rol': 'admin'}`.", "Permite verificar privilegios en memoria sin consultar tablas de permisos en cada petición."),
                ("03. Código HTTP 403 Forbidden vs 401", "HTTP 401: 'No sé quién eres' (No autenticado). HTTP 403: 'Sé quién eres, pero no tienes permiso' (No autorizado).", "Distinción semántica fundamental en APIs REST profesionales.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Decoradores y Factorías de Dependencias RBAC",
            "descripcion": "Restricción declarativa de endpoints por rol:",
            "tarjetas": [
                ("Factoría `require_role(roles_permitidos)`", "Crea una dependencia que inspecciona el usuario autenticado y lanza `HTTPException(403)` si no posee el rol.", "Uso limpio: `@app.delete('/usuarios/{id}', dependencies=[Depends(require_role(['admin']))])`."),
                ("Principio de Menor Privilegio (PoLP)", "Cada rol debe tener acceso exclusivamente a los recursos mínimos necesarios para sus funciones.", "Limita el impacto de seguridad ante el compromiso de una cuenta de usuario.")
            ]
        },
        "casos_borde": {
            "titulo": "Fallas Críticas de Autorización (BOLA / IDOR)",
            "items": [
                "Broken Object Level Authorization (BOLA): Permitir que un usuario modifique el recurso de otro usuario cambiando el ID en la URI.",
                "Retornar HTTP 401 cuando el usuario sí está autenticado pero carece de permisos de administrador (debe ser 403).",
                "Confiar en roles enviados por el cliente en el cuerpo de la petición sin validarlos contra el token firmado."
            ]
        }
    },
    18: {
        "tema": "Rate Limiting, Throttling y Prevención de Abuso",
        "unidad": "Bloque 2: Lógica de Negocio, Controladores y Auth",
        "teoria_principal": {
            "titulo": "Protección de Disponibilidad y Mitigación de DoS",
            "lead": "El Rate Limiting restringe la cantidad de peticiones que un cliente puede realizar en una ventana de tiempo determinada.",
            "tarjetas": [
                ("01. Algoritmos de Ventana (Token Bucket / Sliding Window)", "Permiten ráfagas cortas controladas pero limitan el promedio sostenido de peticiones por minuto.", "Previene la saturación del servidor por scripts automatizados o ataques de denegación de servicio (DoS)."),
                ("02. Identificación del Cliente (IP vs Token)", "Límite por IP para rutas públicas (login/registro) y límite por ID de usuario autenticado para la API interna.", "Evita que un atacante consuma recursos en endpoints de procesamiento pesado."),
                ("03. Código HTTP 429 Too Many Requests", "Respuesta estándar emitida cuando el cliente supera su cuota de peticiones permitidas.", "Debe incluir el encabezado `Retry-After: <segundos>` indicando cuándo puede reintentar.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Almacenamiento de Contadores en Memoria y Redis",
            "descripcion": "Gestión de estado de cuotas de consumo:",
            "tarjetas": [
                ("Contadores en Memoria (Desarrollo)", "Diccionario en RAM con timestamps de peticiones por cliente.", "Fácil de auditar en pruebas unitarias dentro de Google Colab."),
                ("Contadores en Redis con TTL (Producción)", "Claves con expiración atómica (`INCR` + `EXPIRE`) compartidas entre todos los nodos del clúster.", "Garantiza control de tráfico unificado en sistemas distribuidos.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla en Rate Limiting",
            "items": [
                "Bloquear proxies o balanceadores de carga al usar `request.client.host` sin leer encabezados `X-Forwarded-For`.",
                "Omitir el encabezado `Retry-After` provocando que los clientes realicen reintentos inmediatos agresivos.",
                "No aplicar límites estrictos en el endpoint de autenticación permitiendo ataques de fuerza bruta a contraseñas."
            ]
        }
    },
    19: {
        "tema": "Sanitización de Entradas, Prevención de XSS e Inyecciones",
        "unidad": "Bloque 2: Lógica de Negocio, Controladores y Auth",
        "teoria_principal": {
            "titulo": "Defensa en Profundidad y Validación de Datos No Confiables",
            "lead": "Todo dato proveniente del cliente debe tratarse como hostil hasta que sea validado, tipado y sanitizado.",
            "tarjetas": [
                ("01. Cross-Site Scripting (XSS)", "Inyección de código JavaScript malicioso (`<script>alert(1)</script>`) en campos de texto que luego se renderizan en el navegador de otros usuarios.", "Permite a un atacante robar tokens de sesión o suplantar la identidad de la víctima."),
                ("02. Sanitización vs Escape de Salida", "Sanitización: Elimina etiquetas y caracteres peligrosos al entrar a la API. Escape: Codifica entidades HTML (`&lt;`, `&gt;`) al renderizar.", "Ambas capas deben implementarse para una defensa integral."),
                ("03. Inyecciones de Comandos y NoSQL", "Entradas maliciosas que buscan ser ejecutadas como llamadas al sistema operativo o consultas no estructuradas.", "Se neutralizan forzando tipado estricto y listas blancas de caracteres permitidos.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Sanitizadores Automáticos en el Pipeline DTO",
            "descripcion": "Limpieza de cadenas en la capa de deserialización:",
            "tarjetas": [
                ("Limpieza de Espacios y Tags", "Uso de validadores Pydantic que aplican `strip()`, eliminan caracteres de control y escapan HTML.", "Garantiza que la base de datos almacene texto limpio y normalizado."),
                ("Encabezados de Seguridad HTTP", "Inyección de `Content-Security-Policy (CSP)`, `X-Content-Type-Options: nosniff` y `X-Frame-Options: DENY`.", "Instruye al navegador para bloquear la ejecución de scripts no autorizados.")
            ]
        },
        "casos_borde": {
            "titulo": "Vulnerabilidades Frecuentes",
            "items": [
                "Confiar en validaciones hechas solo en el frontend con JavaScript, fácilmente eludibles con herramientas como Postman o cURL.",
                "Almacenar HTML crudo ingresado por usuarios en campos de comentarios o perfiles.",
                "No escapar comillas dobles y simples en atributos HTML generando rupturas de contexto de seguridad."
            ]
        }
    },
    20: {
        "tema": "Hito 2: API con Inyección de Dependencias, Auth JWT y RBAC",
        "unidad": "Bloque 2: Lógica de Negocio, Controladores y Auth",
        "teoria_principal": {
            "titulo": "Integración del Segundo Hito: Seguridad y Control de Acceso",
            "lead": "Culminación del Bloque 2. La API ahora cuenta con arquitectura en capas, autenticación segura con JWT, hashing de contraseñas y autorización por roles (RBAC).",
            "tarjetas": [
                ("01. Pipeline de Autenticación Completo", "Flujo integrado: Registro con Bcrypt -> Login con OAuth2 `/token` -> Emisión de JWT firmado -> Acceso a rutas protegidas con Bearer token.", "Garantiza protección completa de los recursos del sistema."),
                ("02. Control de Acceso por Roles (RBAC)", "Endpoints administrativos bloqueados con HTTP 403 para usuarios comunes; endpoints privados protegidos con HTTP 401 para usuarios anónimos.", "Verificado mediante pruebas automatizadas de intrusión."),
                ("03. Entrega de Hito 2 (Git Tag)", "Etiquetado formal de versión en el repositorio de GitHub del estudiante: `git tag v0.2-hito2`.", "Representa el 25% del Proyecto Integrador Semestral.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Auditoría Integral de Seguridad con Test Harness",
            "descripcion": "Batería de pruebas automatizadas sobre el servidor en Colab:",
            "tarjetas": [
                ("Suite de Intrusión Automatizada", "Pruebas con tokens manipulados, tokens expirados, contraseñas erróneas y accesos con roles insuficientes.", "Certifica que la API no tenga fugas de seguridad ni accesos no autorizados."),
                ("Inspección de Encabezados y Respuestas", "Verificación de que las contraseñas nunca se devuelvan en las respuestas JSON y los errores emitan los códigos HTTP estándar.", "Cumplimiento estricto de las mejores prácticas de la industria.")
            ]
        },
        "casos_borde": {
            "titulo": "Criterios de Rechazo del Hito 2",
            "items": [
                "Almacenar contraseñas en texto plano o con algoritmos no seguros (MD5/SHA).",
                "Permitir el acceso a rutas administrativas a usuarios con roles no autorizados.",
                "Fallas del servidor (HTTP 500) al recibir tokens mal formados o cadenas corruptas en el encabezado Authorization."
            ]
        }
    }
}

def compilar_presentacion_5_slides_web(num, data):
    n_str = f"{num:02d}"
    tema = data["tema"]
    unidad = data["unidad"]
    tp = data["teoria_principal"]
    am = data["arquitectura_memoria"]
    cb = data["casos_borde"]

    cards_s2 = ""
    for t_tit, t_desc, t_det in tp["tarjetas"]:
        cards_s2 += f"""
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span style="color: var(--accent);">{t_tit}</span><span class="expand-hint">[+]</span></div>
          <p>{t_desc}</p>
          <div class="card-details">{t_det}</div>
        </div>"""

    cards_s3 = ""
    for a_tit, a_desc, a_det in am["tarjetas"]:
        cards_s3 += f"""
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span style="color: var(--accent-silver);">{a_tit}</span><span class="expand-hint">[+]</span></div>
          <p>{a_desc}</p>
          <div class="card-details">{a_det}</div>
        </div>"""

    items_s4 = "".join([f"<li><strong>{item}</strong></li>" for item in cb["items"]])

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sesión {n_str}: {tema} | Desarrollo de Aplicaciones Web</title>
  <style>
    :root {{
      --bg: #f4f8fb;
      --card-bg: rgba(255, 255, 255, 0.88);
      --card-bg-hover: rgba(255, 255, 255, 0.98);
      --border: #d0dbe5;
      --border-focus: #0969da;
      --accent: #0969da;
      --accent-green: #1a7f37;
      --accent-silver: #627282;
      --accent-orange: #d29922;
      --text: #334155;
      --text-bright: #0f172a;
      --font-mono: 'Fira Code', monospace;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }}
    header {{
      padding: 12px 28px;
      background: rgba(255, 255, 255, 0.85);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .brand {{ font-weight: 700; color: var(--text-bright); font-size: 0.95rem; }}
    .tag {{
      background-color: #ddf4ff;
      color: var(--accent);
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 0.75rem;
      font-family: var(--font-mono);
      font-weight: 600;
      border: 1px solid #b6e3ff;
    }}
    main {{ flex: 1; display: flex; position: relative; overflow: hidden; }}
    .slide {{
      position: absolute;
      inset: 0;
      padding: 30px 60px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      opacity: 0;
      visibility: hidden;
      transform: translateX(30px);
      transition: all 0.3s ease;
    }}
    .slide.active {{ opacity: 1; visibility: visible; transform: translateX(0); }}
    h1 {{ font-size: 2rem; color: var(--text-bright); margin-bottom: 12px; }}
    h2 {{ font-size: 1.5rem; color: var(--text-bright); margin-bottom: 16px; }}
    p.lead {{ font-size: 1.05rem; line-height: 1.5; max-width: 900px; margin-bottom: 18px; color: #475569; }}
    .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }}
    .grid-2 {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 18px;
      cursor: pointer;
      transition: all 0.25s ease;
      display: flex;
      flex-direction: column;
    }}
    .card:hover {{ background: var(--card-bg-hover); border-color: var(--border-focus); transform: translateY(-2px); }}
    .card.expanded {{ border-color: var(--accent); background: #ffffff; }}
    .card-header {{ font-weight: 600; color: var(--text-bright); margin-bottom: 8px; display: flex; justify-content: space-between; }}
    .expand-hint {{ font-size: 0.75rem; color: var(--accent); font-family: var(--font-mono); }}
    .card p, .card li {{ font-size: 0.88rem; line-height: 1.45; color: var(--text); }}
    .card-details {{ max-height: 0; overflow: hidden; opacity: 0; transition: all 0.3s ease; font-size: 0.82rem; color: #475569; }}
    .card.expanded .card-details {{ max-height: 240px; opacity: 1; margin-top: 10px; padding-top: 10px; border-top: 1px dashed var(--border); }}
    .interactive-box {{
      margin-top: 18px;
      padding: 14px 18px;
      background: #ffffff;
      border: 1px solid var(--border);
      border-left: 4px solid var(--accent);
      border-radius: 6px;
      font-family: var(--font-mono);
      font-size: 0.85rem;
    }}
    footer {{
      padding: 12px 28px;
      background: rgba(255, 255, 255, 0.85);
      border-top: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }}
    .progress {{ font-size: 0.85rem; font-family: var(--font-mono); color: var(--accent); font-weight: 600; }}
    .controls {{ display: flex; gap: 10px; }}
    button {{
      background: #ffffff;
      color: var(--text-bright);
      border: 1px solid var(--border);
      padding: 7px 18px;
      border-radius: 6px;
      cursor: pointer;
      font-weight: 600;
    }}
    button:hover {{ background: #f1f5f9; }}
    button:disabled {{ opacity: 0.4; cursor: not-allowed; }}
  </style>
</head>
<body>
  <header>
    <div class="brand">TecNM Cancún &bull; DAB-2201</div>
    <div class="tag">SESIÓN {n_str} / 40 &bull; {tema}</div>
  </header>

  <main>
    <section class="slide active">
      <div class="tag" style="width: fit-content; margin-bottom: 10px;">{unidad.upper()}</div>
      <h1>{tema}</h1>
      <p class="lead">Sesión {n_str} del curso. Arquitectura en capas, gestión de dependencias, seguridad criptográfica y control de acceso con la Tríada Metodológica.</p>
      <div class="grid-3">
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span style="color: var(--accent);">01. El Artesano</span><span class="expand-hint">[+]</span></div>
          <p>Codificación manual sin IA para experimentar el diseño de controladores desacoplados y hashing.</p>
          <div class="card-details">Desarrolla la intuición técnica de capas de servicio, salting y validación de tokens.</div>
        </div>
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span style="color: var(--accent-silver);">02. El Científico</span><span class="expand-hint">[+]</span></div>
          <p>Especificación formal C-R-E-O para flujos de autenticación OAuth2 y esquemas de roles RBAC.</p>
          <div class="card-details">Define contratos de seguridad con claims JWT y códigos de respuesta semánticos (401, 403, 429).</div>
        </div>
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span style="color: var(--accent-green);">03. El Auditor</span><span class="expand-hint">[+]</span></div>
          <p>Test Harness automatizado con pruebas de intrusión, tokens manipulados y expirados.</p>
          <div class="card-details">Auditoría destructiva sobre rutas protegidas y verificación de permisos en GitHub.</div>
        </div>
      </div>
    </section>

    <section class="slide">
      <h2>00–20 min: Fundamentos Teóricos — {tp["titulo"]}</h2>
      <p class="lead">{tp["lead"]}</p>
      <div class="grid-3">
        {cards_s2}
      </div>
      <div class="interactive-box">
        <strong>Invariante de Seguridad:</strong> La autenticación verifica la identidad; la autorización delimita estrictamente los privilegios sobre cada recurso.
      </div>
    </section>

    <section class="slide">
      <h2>Arquitectura del Servidor y Seguridad: {am["titulo"]}</h2>
      <p class="lead">{am["descripcion"]}</p>
      <div class="grid-2">
        {cards_s3}
      </div>
    </section>

    <section class="slide">
      <h2>{cb["titulo"]}</h2>
      <p class="lead">Puntos críticos de falla y vulnerabilidades que deben protegerse en la implementación y auditarse en la IA:</p>
      <div class="card" style="padding: 24px;">
        <ul style="padding-left: 20px; line-height: 2;">
          {items_s4}
        </ul>
      </div>
    </section>

    <section class="slide">
      <h2>Dinámica del Laboratorio y Protocolo de Entrega</h2>
      <div class="grid-2">
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span>Estructura de la Clase (60 min)</span><span class="expand-hint">[+]</span></div>
          <ul>
            <li><strong>00–20 min:</strong> Fundamento teórico y arquitectura de seguridad.</li>
            <li><strong>20–35 min:</strong> Fase 1: El Artesano (Código manual sin IA).</li>
            <li><strong>35–45 min:</strong> Fase 2: El Científico (Prompt C-R-E-O).</li>
            <li><strong>45–55 min:</strong> Fase 3: El Auditor (Test Harness de Seguridad).</li>
            <li><strong>55–60 min:</strong> Sincronización y commit en GitHub.</li>
          </ul>
          <div class="card-details">Verifica que todas las aserciones de seguridad pasen al 100% antes de subir tu bitácora.</div>
        </div>
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span>Evidencia Evaluada</span><span class="expand-hint">[+]</span></div>
          <p>Tu archivo <code>auditorias/auditoria_sesion{n_str}.md</code> debe contener la matriz C-R-E-O y el reporte crítico.</p>
          <div class="card-details">La entrega de la Sesión 20 concluye formalmente el Hito 2 del Proyecto Integrador.</div>
        </div>
      </div>
      <div class="interactive-box">
        <strong>Docente Titular:</strong> MCC. Iván Márquez Larios (<code>ijmarquezl</code>) &bull; TecNM Cancún
      </div>
    </section>
  </main>

  <footer>
    <div class="progress" id="slideIndicator">SLIDE 1 / 5</div>
    <div class="controls">
      <button id="prevBtn" onclick="prevSlide()" disabled>&larr; Anterior</button>
      <button id="nextBtn" onclick="nextSlide()">Siguiente &rarr;</button>
    </div>
  </footer>

  <script>
    let currentSlide = 0;
    const slides = document.querySelectorAll('.slide');
    const indicator = document.getElementById('slideIndicator');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    function updateSlides() {{
      slides.forEach((slide, index) => slide.classList.toggle('active', index === currentSlide));
      indicator.textContent = `SLIDE ${{currentSlide + 1}} / ${{slides.length}}`;
      prevBtn.disabled = currentSlide === 0;
      nextBtn.disabled = currentSlide === slides.length - 1;
    }}
    function nextSlide() {{ if (currentSlide < slides.length - 1) {{ currentSlide++; updateSlides(); }} }}
    function prevSlide() {{ if (currentSlide > 0) {{ currentSlide--; updateSlides(); }} }}
    function toggleCard(card) {{
      card.classList.toggle('expanded');
      const hint = card.querySelector('.expand-hint');
      if (hint) hint.textContent = card.classList.contains('expanded') ? '[-]' : '[+]';
    }}
    document.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowRight' || e.key === ' ') nextSlide();
      if (e.key === 'ArrowLeft') prevSlide();
    }});
  </script>
</body>
</html>
"""
    return html

def main():
    print("🚀 Compilando presentaciones enriquecidas de Desarrollo Web (Bloque 2: Sesiones 11 a 20)...")
    os.makedirs("presentaciones", exist_ok=True)
    
    for num, data in TEORIA_WEB_BLOQUE_2.items():
        n_str = f"{num:02d}"
        out_path = f"presentaciones/sesion{n_str}.html"
        html_content = compilar_presentacion_5_slides_web(num, data)
        
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"  -> Generada Sesión {n_str}: {data['tema']} (5 slides)")
            
    print("✅ Bloque 2 de presentaciones de Desarrollo Web actualizado exitosamente.")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Compilador de Presentaciones Enriquecidas (Bloque 1: Sesiones 01 a 10)
Materia: Desarrollo de Aplicaciones Web (DAB-2201)
Incluye Encuadre Completo de 6 Slides en Sesión 01 y 5 Slides Teóricos en Sesiones 02-10.
Autor: MCC. Iván Márquez Larios (ijmarquezl)
TecNM - Campus Cancún
"""

import os

TEORIA_WEB_BLOQUE_1 = {
    1: {
        "tema": "Encuadre, Diagnóstico HTTP y Servidores en la Nube",
        "unidad": "Bloque 1: Arquitectura Web, Protocolo HTTP y REST APIs",
        "es_encuadre": True
    },
    2: {
        "tema": "Gestión en GitHub Web y Métodos HTTP (GET, POST, PUT, DELETE)",
        "unidad": "Bloque 1: Arquitectura Web, Protocolo HTTP y REST APIs",
        "es_encuadre": False,
        "teoria_principal": {
            "titulo": "Semántica del Protocolo HTTP y Métodos de Petición",
            "lead": "El protocolo HTTP define acciones estandarizadas sobre recursos identificables mediante verbos con semántica de idempotencia y seguridad.",
            "tarjetas": [
                ("01. GET & DELETE (Lectura y Baja)", "GET recupera una representación del recurso sin alterar su estado; DELETE remueve la entidad.", "Ambos deben ser idempotentes: múltiples peticiones idénticas producen el mismo estado en el servidor."),
                ("02. POST vs PUT / PATCH (Creación vs Edición)", "POST crea recursos subordinados con ID generado por el servidor; PUT reemplaza totalmente el recurso; PATCH realiza modificaciones parciales.", "POST no es idempotente (múltiples POST crean múltiples recursos)."),
                ("03. Código HTTP 405 Method Not Allowed", "Respuesta emitida cuando la URI existe pero el verbo HTTP utilizado no está implementado en la ruta.", "Debe incluir el encabezado 'Allow' informando los métodos aceptados.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Enrutamiento Semántico y Despacho en Servidor",
            "descripcion": "Cómo el servidor web mapea la dupla (Verbo, Ruta) hacia el controlador:",
            "tarjetas": [
                ("Tabla de Rutas (Routing Table)", "Mapeo interno del framework: `(VERBO, PATRON_URI) -> FUNCION_CONTROLADOR`.", "El middleware de ruteo inspecciona la primera línea de la petición HTTP antes de deserializar el payload."),
                ("Idempotencia en APIs REST", "Garantía de que reintentar una petición fallida por problemas de red no corromperá el estado de la base de datos.", "Esencial para construir clientes web resilientes.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Métodos HTTP",
            "items": [
                "Usar GET para modificar o eliminar datos en el servidor (ej. `/api/eliminar_usuario?id=5`), rompiendo la seguridad del protocolo.",
                "Usar POST para todo (Antipatrón 'RPC sobre HTTP') ignorando la semántica de PUT, PATCH y DELETE.",
                "Retornar HTTP 200 OK en respuestas de error de método no permitido."
            ]
        }
    },
    3: {
        "tema": "Headers, Content-Type y Negociación de Contenido",
        "unidad": "Bloque 1: Arquitectura Web, Protocolo HTTP y REST APIs",
        "es_encuadre": False,
        "teoria_principal": {
            "titulo": "Metadatos HTTP y Negociación de Representación",
            "lead": "Los encabezados (*Headers*) transportan metadatos esenciales para la autenticación, almacenamiento en caché y formato de transferencia.",
            "tarjetas": [
                ("01. Content-Type (Formato del Payload)", "Indica el tipo MIME de los bytes transportados en el cuerpo del mensaje (ej. `application/json`, `multipart/form-data`).", "Permite al servidor seleccionar el parser adecuado para deserializar la entrada."),
                ("02. Accept Header (Negociación)", "Enviado por el cliente para indicar qué formatos de respuesta puede procesar (ej. `Accept: application/json`).", "Si el servidor no puede emitir un formato aceptado, debe responder con HTTP 406 Not Acceptable."),
                ("03. Encabezados Personalizados (X-Headers)", "Metadatos adicionales como trazabilidad de peticiones (`X-Request-ID`) o tiempos de ejecución (`X-Process-Time`).", "Proporcionan observabilidad sin alterar el cuerpo JSON del mensaje.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Procesamiento de Streams y Parser MIME",
            "descripcion": "Transformación de flujo de bytes a estructuras en memoria:",
            "tarjetas": [
                ("Deserialización del Stream", "El servidor lee los bytes puros de la conexión TCP y utiliza el `Content-Type` para invocar el decodificador JSON.", "Si los bytes no corresponden a un JSON válido, se emite un error HTTP 400 Bad Request."),
                ("Código HTTP 415 Unsupported Media Type", "Respuesta automática cuando el cliente envía un cuerpo en un formato no soportado por el endpoint.", "Protege al servidor de intentar parsear payloads incompatibles.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla en Negociación de Contenido",
            "items": [
                "Omitir el encabezado `Content-Type: application/json` al enviar payloads JSON en peticiones POST.",
                "Asumir que el cuerpo de la petición es una cadena de texto sin validar la codificación de caracteres (UTF-8).",
                "Retornar respuestas en texto plano cuando el cliente solicitó explícitamente `application/json`."
            ]
        }
    },
    4: {
        "tema": "Anatomía RESTful, URIs Nombres y Recursos",
        "unidad": "Bloque 1: Arquitectura Web, Protocolo HTTP y REST APIs",
        "es_encuadre": False,
        "teoria_principal": {
            "titulo": "Principios de Diseño de APIs RESTful",
            "lead": "REST (Representational State Transfer) organiza la arquitectura web en torno a recursos identificados por URIs jerárquicas y sustantivas.",
            "tarjetas": [
                ("01. URIs Basadas en Sustantivos Plurales", "Las URIs identifican recursos (`/api/v1/usuarios`), nunca acciones (`/api/v1/obtenerUsuarios`).", "La acción a realizar sobre el recurso la determina exclusivamente el verbo HTTP."),
                ("02. Jerarquía y Sub-Recursos", "Representación de relaciones entre entidades mediante anidamiento lógico: `/api/v1/usuarios/{id}/pedidos`.", "Mantiene la estructura de rutas intuitiva y predecible."),
                ("03. Desacoplamiento Cliente-Servidor", "El servidor expone datos y estado; el cliente se encarga de la presentación y la interfaz de usuario.", "Permite reutilizar la misma API para clientes Web, Móviles e Integraciones IoT.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Parámetros de Ruta vs Query Parameters",
            "descripcion": "Selección de canales de entrada según la intención de la búsqueda:",
            "tarjetas": [
                ("Path Parameters (`/recursos/{id}`)", "Se utilizan para identificar un recurso específico de forma única en la jerarquía.", "Su ausencia en la URI provoca un error de ruteo HTTP 404 Not Found."),
                ("Query Parameters (`/recursos?limit=10&page=2`)", "Se utilizan para filtrar, ordenar, paginar o buscar sobre una colección de recursos.", "Son opcionales y no alteran la identidad base de la URI.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Diseño RESTful",
            "items": [
                "Incluir verbos dentro de la URI (ej. `/api/v1/crear_producto` en lugar de `POST /api/v1/productos`).",
                "Anidamiento excesivo de recursos (> 2 niveles de profundidad como `/tiendas/1/estantes/2/cajas/3/productos`), volviendo la API difícil de mantener.",
                "Retornar arreglos JSON crudos en la raíz en lugar de objetos JSON envueltos (`{'data': [...]}`)."
            ]
        }
    },
    5: {
        "tema": "Pydantic v2 / DTOs en PHP y Tipado Estático",
        "unidad": "Bloque 1: Arquitectura Web, Protocolo HTTP y REST APIs",
        "es_encuadre": False,
        "teoria_principal": {
            "titulo": "Data Transfer Objects (DTO) y Validación Estricta",
            "lead": "Un DTO define el esquema rígido de los datos que ingresan o salen de la API, garantizando tipado seguro en tiempo de ejecución.",
            "tarjetas": [
                ("01. Validación en Tiempo de Ejecución", "Python y PHP son dinámicos; Pydantic/DTOs fuerzan la conversión y validación de tipos al recibir el JSON.", "Si la entrada no coincide exactamente con el esquema, la petición es derivada automáticamente a un manejador de errores."),
                ("02. Coerción de Tipos Controlada", "Pydantic v2 convierte cadenas numéricas `\"123\"` a enteros `123` si el esquema lo define como `int`.", "Evita fallos silenciosos en la capa de lógica de negocio."),
                ("03. Deserialización y Serialización", "Transformación bidireccional: `JSON -> DTO (Entrada)` y `Objeto/Model -> DTO -> JSON (Salida)`.", "Aísla el modelo interno de la base de datos de la representación pública enviada al cliente.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Arquitectura de Pydantic v2 (Rust Core)",
            "descripcion": "Rendimiento y seguridad de esquemas de datos:",
            "tarjetas": [
                ("Motor Pydantic-Core (Rust)", "Pydantic v2 ejecuta la validación de esquemas compilada en Rust, alcanzando velocidades de 5x a 50x superiores a v1.", "Garantiza consumo de memoria mínimo bajo tráfico masivo."),
                ("Código HTTP 422 Unprocessable Entity", "Respuesta estándar cuando el JSON es sintácticamente válido pero viola los tipos o restricciones del DTO.", "Devuelve una lista detallada con los campos exactos que fallaron.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla en DTOs",
            "items": [
                "Exponer entidades de base de datos directamente en el endpoint en lugar de usar DTOs de salida.",
                "Permitir la inyección de campos no declarados en el esquema (*Mass Assignment Vulnerability*).",
                "Omitir valores por defecto en campos opcionales causando errores de atributo nulo (`NoneType`)."
            ]
        }
    },
    6: {
        "tema": "Validación Estricta, Constraints y Params Query/Body",
        "unidad": "Bloque 1: Arquitectura Web, Protocolo HTTP y REST APIs",
        "es_encuadre": False,
        "teoria_principal": {
            "titulo": "Reglas de Dominio y Restricciones de Entrada",
            "lead": "La validación no se limita al tipo de dato; debe certificar que los valores respeten las restricciones del dominio del negocio.",
            "tarjetas": [
                ("01. Restricciones Numéricas y de Cadenas", "Uso de `Field(ge=18, le=100)` para límites numéricos y `Field(min_length=3, max_length=50)` para texto.", "Detiene entradas absurdas o maliciosas en la frontera de la API."),
                ("02. Expresiones Regulares (Regex Validation)", "Validación de formatos complejos mediante patrones: emails, RFCs, teléfonos o UUIDs.", "Garantiza la consistencia del formato antes de consultar la base de datos."),
                ("03. Validadores Personalizados (@field_validator)", "Métodos que ejecutan lógica condicional avanzada sobre uno o más campos del DTO.", "Permite verificar reglas como: 'la fecha_fin debe ser posterior a la fecha_inicio'.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Procesamiento de Fuentes de Entrada Múltiples",
            "descripcion": "Extracción simultánea de datos en un solo handler:",
            "tarjetas": [
                ("Anotaciones de Ubicación", "FastAPI/Frameworks diferencian entre `Path()`, `Query()`, `Header()` y `Body()`.", "Garantiza que un parámetro de búsqueda no sea confundido con un atributo del payload JSON."),
                ("Generación de Documentación Automática", "Las restricciones declaradas en `Field()` se compilan directamente en el esquema OpenAPI JSON del servidor.", "Mantiene la documentación viva y sincronizada con el código.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Validación de Entrada",
            "items": [
                "Validar datos manualmente con sentencias `if/else` dentro del controlador en lugar de usar el DTO.",
                "Permitir cadenas compuestas únicamente por espacios en blanco (`\"   \"`) al no aplicar `.strip()`.",
                "No limitar el tamaño máximo de listas o archivos subidos saturando la memoria RAM del servidor."
            ]
        }
    },
    7: {
        "tema": "Especificación OpenAPI (Swagger) y ReDoc",
        "unidad": "Bloque 1: Arquitectura Web, Protocolo HTTP y REST APIs",
        "es_encuadre": False,
        "teoria_principal": {
            "titulo": "Documentación Viva e Interoperabilidad de APIs",
            "lead": "OpenAPI es el estándar industrial neutro para describir APIs RESTful de forma legible tanto por humanos como por máquinas.",
            "tarjetas": [
                ("01. Especificación OpenAPI v3.1", "Documento JSON/YAML que describe rutas, verbos, parámetros, esquemas de payload y códigos de respuesta.", "Sustituye la documentación manual desactualizada por un contrato auditable."),
                ("02. Swagger UI (Cliente Interactivo)", "Interfaz gráfica que permite probar endpoints directamente desde el navegador enviando peticiones HTTP reales.", "Acelera el desarrollo del frontend al proporcionar un entorno de pruebas inmediato."),
                ("03. ReDoc (Documentación Estática Enriquecida)", "Renderizado alternativo enfocado en la lectura limpia de esquemas de datos y contratos técnicos.", "Ideal para publicar portales de desarrolladores y especificaciones oficiales.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Generación Automática del Esquema JSON",
            "descripcion": "Reflexión e inspección de código en el servidor:",
            "tarjetas": [
                ("Endpoint `/openapi.json`", "El servidor inspecciona las rutas registradas y sus tipos Pydantic para construir el JSON OpenAPI dinámicamente.", "Permite a herramientas externas (Postman, SDK Generators) consumir el esquema al instante."),
                ("Generación de SDKs de Cliente", "A partir del documento OpenAPI, es posible autogenerar clientes en TypeScript, Swift o Kotlin sin escribir código de red manual.", "Garantiza sincronización total entre backend y aplicaciones móviles/web.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla en Documentación OpenAPI",
            "items": [
                "Exponer endpoints privados o de diagnóstico interno en el esquema OpenAPI público.",
                "Omitir la documentación de respuestas de error (400, 401, 403, 404, 422) mostrando únicamente la respuesta 200 OK.",
                "Mantener descripciones genéricas en los esquemas sin ejemplos reales de uso."
            ]
        }
    },
    8: {
        "tema": "Respuestas Semánticas y Excepciones HTTP Personalizadas",
        "unidad": "Bloque 1: Arquitectura Web, Protocolo HTTP y REST APIs",
        "es_encuadre": False,
        "teoria_principal": {
            "titulo": "Manejo Global de Errores y Estandarización de Respuestas",
            "lead": "Una API profesional nunca debe colapsar emitiendo un traceback de código o un error HTTP 500 no capturado.",
            "tarjetas": [
                ("01. Excepciones Semánticas (HTTPException)", "Lanzamiento de excepciones estructuradas indicando código de estado y detalle JSON legible.", "Interrumpe la ejecución del handler actual y delega la respuesta al middleware de errores."),
                ("02. Manejadores Globales de Excepciones", "Capturadores centralizados (`@app.exception_handler`) que transforman excepciones no controladas en JSONs uniformes.", "Previene la fuga de información sensible (variables de entorno, rutas de código o passwords) al cliente."),
                ("03. Estructura Estándar de Errores JSON", "Respuesta uniforme de error: `{'status': 'error', 'code': 404, 'detail': '...', 'timestamp': '...'}`.", "Facilita la captura y despliegue de alertas en las aplicaciones frontend.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Flujo de Intercepción de Excepciones",
            "descripcion": "Ciclo de captura dentro de la pila de middlewares del servidor:",
            "tarjetas": [
                ("Captura de Errores no Manejados", "Si ocurre una división por cero o falla de DB, el manejador raíz intercepta el fallo, registra el log interno y emite un HTTP 500 limpio.", "Mantiene la estabilidad del proceso del servidor web."),
                ("Respuestas de Error en Pydantic", "FastAPI captura automáticamente `RequestValidationError` y lo transforma en un HTTP 422 detallado.", "Ahorra código repetitivo de validación manual.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Respuestas de Error",
            "items": [
                "Retornar un traceback de Python o PHP en la respuesta HTTP expuesto al usuario en producción.",
                "Retornar HTTP 200 OK con un cuerpo JSON que contiene `{'error': 'Usuario no encontrado'}`.",
                "Uso indiscriminado de errores HTTP 500 para fallos causados por datos inválidos del cliente (que corresponden a 400/422)."
            ]
        }
    },
    9: {
        "tema": "Middleware Web, Intercepción y Logging de Transacciones",
        "unidad": "Bloque 1: Arquitectura Web, Protocolo HTTP y REST APIs",
        "es_encuadre": False,
        "teoria_principal": {
            "titulo": "Patrón Pipeline y Procesamiento Transversal",
            "lead": "Los middlewares son componentes colocados en la tubería de peticiones que interceptan y modifican Requests y Responses.",
            "tarjetas": [
                ("01. Modelo de Cebolla (Onion Architecture)", "La petición atraviesa cada middleware hacia adentro hasta llegar al handler, y la respuesta regresa atravesando la tubería hacia afuera.", "Permite ejecutar código antes y después de la lógica del endpoint."),
                ("02. Casos de Uso Transversales", "Auditoría de logs, medición de tiempo de ejecución, inyección de encabezados de seguridad, compresión Gzip.", "Desacopla responsabilidades que no pertenecen a la lógica de negocio del endpoint."),
                ("03. Medición de Tiempos y Trazabilidad", "Inyección del encabezado `X-Process-Time` y generación de UUIDs de rastreo (`X-Request-ID`).", "Permite auditar cuellos de botella de rendimiento en entornos distribuidos.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Ciclo de Vida de una Petición Interceptada",
            "descripcion": "Flujo de ejecución del objeto Request a través del pipeline:",
            "tarjetas": [
                ("Pre-procesamiento (Incoming Request)", "El middleware puede leer encabezados, validar tokens o rechazar la petición antes de que consuma recursos en el handler.", "Si rechaza la petición, devuelve una respuesta inmediata cortocircuitando la cadena."),
                ("Post-procesamiento (Outgoing Response)", "El middleware modifica la respuesta generada agregando encabezados de seguridad o registrando métricas en base de datos.", "Asegura que todos los endpoints emitan los mismos encabezados estándar.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla en Middlewares",
            "items": [
                "Consumir el stream del cuerpo de la petición (`request.body()`) en un middleware sin clonarlo, impidiendo que el handler vuelva a leerlo.",
                "Middlewares lentos o bloqueantes que añaden latencia excesiva a absolutamente todas las rutas de la API.",
                "Capturar excepciones dentro del middleware sin re-lanzarlas, ocultando errores del servidor."
            ]
        }
    },
    10: {
        "tema": "Hito 1: Mock API RESTful con OpenAPI y Validation Harness",
        "unidad": "Bloque 1: Arquitectura Web, Protocolo HTTP y REST APIs",
        "es_encuadre": False,
        "teoria_principal": {
            "titulo": "Integración del Primer Hito de Arquitectura Web",
            "lead": "Culminación del Bloque 1. Ensamblaje de una Mock API completa con ruteo semántico, DTOs Pydantic v2, contrato OpenAPI y manejador global de errores.",
            "tarjetas": [
                ("01. API Desacoplada y Contract-First", "Servicio web que cumple strictly con la especificación OpenAPI semántica sin depender aún de una base de datos real.", "Proporciona datos de prueba (*Mock Data*) para acelerar la integración con equipos frontend."),
                ("02. Validation Harness Completo", "Toda entrada es filtrada por esquemas DTO estrictos, rechazando tipos inválidos con HTTP 422 y datos fuera de rango con HTTP 400.", "Garantiza que la API sea inmune a payloads mal formados."),
                ("03. Entrega de Hito 1 (Git Tag)", "Etiquetado formal de versión en el repositorio de GitHub del estudiante: `git tag v0.1-hito1`.", "Representa el 20% del Proyecto Integrador Semestral.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Auditoría Automática de Respuestas HTTP",
            "descripcion": "Evaluación de cumplimiento del protocolo web:",
            "tarjetas": [
                ("Test Harness Integrado con HTTPX", "Batería de pruebas automatizadas que somete al servidor embebido en Colab a peticiones válidas y destructivas.", "Verifica códigos de estado 200, 201, 400, 404, 405 y 422."),
                ("Verificación de Encabezados Semánticos", "Certifica que las respuestas emitan `Content-Type: application/json` y los metadatos de trazabilidad esperados.", "Garantiza calidad de software nivel producción.")
            ]
        },
        "casos_borde": {
            "titulo": "Criterios de Rechazo del Hito 1",
            "items": [
                "Servidor que se desploma o emite errores HTTP 500 ante entradas maliciosas o campos vacíos.",
                "Rutas que incluyen verbos en la URI en lugar de utilizar los métodos HTTP estándar.",
                "Documentación OpenAPI inaccesible en `/docs` o desincronizada del código de los endpoints."
            ]
        }
    }
}

def generar_html_encuadre_sesion1():
    return """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sesión 01: Encuadre, Evaluación y Expectativas | Desarrollo de Aplicaciones Web</title>
  <style>
    :root {
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
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg);
      color: var(--text);
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }
    header {
      padding: 12px 28px;
      background: rgba(255, 255, 255, 0.85);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .brand { font-weight: 700; color: var(--text-bright); font-size: 0.95rem; }
    .tag {
      background-color: #ddf4ff;
      color: var(--accent);
      padding: 4px 12px;
      border-radius: 12px;
      font-size: 0.75rem;
      font-family: var(--font-mono);
      font-weight: 600;
      border: 1px solid #b6e3ff;
    }
    main { flex: 1; display: flex; position: relative; overflow: hidden; }
    .slide {
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
    }
    .slide.active { opacity: 1; visibility: visible; transform: translateX(0); }
    h1 { font-size: 2.1rem; color: var(--text-bright); margin-bottom: 12px; line-height: 1.2; }
    h2 { font-size: 1.6rem; color: var(--text-bright); margin-bottom: 16px; }
    p.lead { font-size: 1.05rem; line-height: 1.5; max-width: 900px; margin-bottom: 18px; color: #475569; }
    .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
    .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
    .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 18px;
      cursor: pointer;
      transition: all 0.25s ease;
      display: flex;
      flex-direction: column;
    }
    .card:hover { background: var(--card-bg-hover); border-color: var(--border-focus); transform: translateY(-2px); }
    .card.expanded { border-color: var(--accent); background: #ffffff; }
    .card-header { font-weight: 600; color: var(--text-bright); margin-bottom: 8px; display: flex; justify-content: space-between; }
    .expand-hint { font-size: 0.75rem; color: var(--accent); font-family: var(--font-mono); }
    .card p, .card li { font-size: 0.88rem; line-height: 1.45; color: var(--text); }
    .card-details { max-height: 0; overflow: hidden; opacity: 0; transition: all 0.3s ease; font-size: 0.82rem; color: #475569; }
    .card.expanded .card-details { max-height: 240px; opacity: 1; margin-top: 10px; padding-top: 10px; border-top: 1px dashed var(--border); }
    .code-block {
      background: #0f172a;
      color: #f8fafc;
      padding: 10px 12px;
      border-radius: 6px;
      font-family: var(--font-mono);
      font-size: 0.78rem;
      line-height: 1.4;
      margin-top: 8px;
      overflow-x: auto;
      border: 1px solid #334155;
    }
    .interactive-box {
      margin-top: 18px;
      padding: 14px 18px;
      background: #ffffff;
      border: 1px solid var(--border);
      border-left: 4px solid var(--accent);
      border-radius: 6px;
      font-family: var(--font-mono);
      font-size: 0.85rem;
    }
    footer {
      padding: 12px 28px;
      background: rgba(255, 255, 255, 0.85);
      border-top: 1px solid var(--border);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .progress { font-size: 0.85rem; font-family: var(--font-mono); color: var(--accent); font-weight: 600; }
    .controls { display: flex; gap: 10px; }
    button {
      background: #ffffff;
      color: var(--text-bright);
      border: 1px solid var(--border);
      padding: 7px 18px;
      border-radius: 6px;
      cursor: pointer;
      font-weight: 600;
    }
    button:hover { background: #f1f5f9; }
    button:disabled { opacity: 0.4; cursor: not-allowed; }
  </style>
</head>
<body>

  <header>
    <div class="brand">TecNM Cancún &bull; DAB-2201</div>
    <div class="tag">SESIÓN 01 / 40 &bull; ENCUADRE Y CONTRATO PEDAGÓGICO</div>
  </header>

  <main>
    <!-- Slide 1: Portada y Propósito -->
    <section class="slide active">
      <div class="tag" style="width: fit-content; margin-bottom: 10px;">DAB-2201 &bull; DESARROLLO DE APLICACIONES WEB</div>
      <h1>Encuadre, Arquitectura de Aprendizaje y Expectativas</h1>
      <p class="lead">Bienvenido al curso. No aprenderemos a "pegar plantillas", sino a diseñar y construir arquitecturas backend seguras, escalables y orientadas a servicios con estándares profesionales de la industria.</p>
      
      <div class="grid-3">
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header">
            <span style="color: var(--accent);">01. Desarrollo en la Nube</span>
            <span class="expand-hint">[+]</span>
          </div>
          <p>Cero instalaciones locales. Laboratorios en Google Colab y portafolio en GitHub Web.</p>
          <div class="card-details">
            Ahorramos semanas de configuración de servidores locales (XAMPP/Docker) para enfocarnos directamente en la lógica del protocolo HTTP y la persistencia de datos.
          </div>
        </div>

        <div class="card" onclick="toggleCard(this)">
          <div class="card-header">
            <span style="color: var(--accent-silver);">02. Doble Track Tecnológico</span>
            <span class="expand-hint">[+]</span>
          </div>
          <p>Elige tu stack de especialización: <strong>Python (FastAPI)</strong> o <strong>PHP 8+</strong>.</p>
          <div class="card-details">
            FastAPI para arquitecturas asíncronas de microservicios modernas, o PHP 8+ para dominar el desarrollo modular estructurado en servidores web.
          </div>
        </div>

        <div class="card" onclick="toggleCard(this)">
          <div class="card-header">
            <span style="color: var(--accent-green);">03. Tríada Metodológica</span>
            <span class="expand-hint">[+]</span>
          </div>
          <p>De la intuición manual al diseño formal de especificaciones y auditoría crítica de IA.</p>
          <div class="card-details">
            Aprenderás a interactuar con la IA como un científico: formulando contratos OpenAPI y auditando con Test Harness automatizados.
          </div>
        </div>
      </div>
    </section>

    <!-- Slide 2: Dinámica Diaria -->
    <section class="slide">
      <h2>Estructura de la Clase Diaria (60 Minutos)</h2>
      <p class="lead">Un ritmo ágil y estructurado para asegurar aprendizaje activo y entrega diaria de evidencias.</p>
      
      <div class="grid-3">
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header">
            <span>00–20 min: Estudio Inicial</span>
            <span class="expand-hint">[+]</span>
          </div>
          <p>Presentación interactiva en vivo. Planteamiento del problema de arquitectura y protocolos web.</p>
          <div class="card-details">
            Analizaremos los conceptos clave del día: negociación de contenido, autenticación JWT, transacciones ACID o seguridad contra inyecciones SQL.
          </div>
        </div>

        <div class="card" onclick="toggleCard(this)">
          <div class="card-header">
            <span>20–35 min: El Artesano</span>
            <span class="expand-hint">[+]</span>
          </div>
          <p>Codificación manual en Colab <strong>sin asistencia de IA</strong> para forjar intuición técnica.</p>
          <div class="card-details">
            15 minutos de programación pura para enfrentarse directamente al reto sintáctico y a las restricciones del protocolo.
          </div>
        </div>

        <div class="card" onclick="toggleCard(this)">
          <div class="card-header">
            <span>35–60 min: Científico &amp; Auditor</span>
            <span class="expand-hint">[+]</span>
          </div>
          <p>Diseño de especificación C-R-E-O, consulta a la IA y batería de pruebas destructivas (Test Harness).</p>
          <div class="card-details">
            Verificamos códigos de estado HTTP (200, 400, 422), sanitización de entradas y subimos la bitácora a GitHub.
          </div>
        </div>
      </div>

      <div class="interactive-box">
        <strong>Regla de Trabajo:</strong> Toda sesión concluye con un commit en tu Fork personal respaldando tu bitácora de auditoría.
      </div>
    </section>

    <!-- Slide 3: Expectativas de Rigor e IA -->
    <section class="slide">
      <h2>Expectativas del Curso y Política de Inteligencia Artificial</h2>
      <p class="lead">La IA generativa es una herramienta de ingeniería, no un sustituto de tu razonamiento crítico.</p>
      
      <div class="grid-3">
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header">
            <span style="color: var(--accent-orange);">01. IA como Copiloto Auditado</span>
            <span class="expand-hint">[+]</span>
          </div>
          <p>Prohibido el "Copy-Paste ciego". Todo código devuelto por un LLM debe ser probado y justificado.</p>
          <div class="card-details">
            Si la IA genera código vulnerable a SQL Injection o con códigos de estado HTTP incorrectos, la responsabilidad técnica es del estudiante.
          </div>
        </div>

        <div class="card" onclick="toggleCard(this)">
          <div class="card-header">
            <span style="color: var(--accent);">02. Trazabilidad en GitHub</span>
            <span class="expand-hint">[+]</span>
          </div>
          <p>Tus bitácoras en <code>auditorias/</code> documentan tu proceso de pensamiento e ingeniería de prompts.</p>
          <div class="card-details">
            Evaluamos el historial de tus commits y la profundidad con la que detectaste casos límite no contemplados por el modelo.
          </div>
        </div>

        <div class="card" onclick="toggleCard(this)">
          <div class="card-header">
            <span style="color: var(--accent-green);">03. Puntualidad y Constancia</span>
            <span class="expand-hint">[+]</span>
          </div>
          <p>40 sesiones intensivas. La constancia diaria es el único camino para dominar el desarrollo web moderno.</p>
          <div class="card-details">
            El flujo en la nube te permite avanzar desde cualquier lugar sin pretextos de dependencias rotas en tu máquina.
          </div>
        </div>
      </div>

      <div class="interactive-box">
        <strong>Estándar de Calidad:</strong> Un ingeniero no solo sabe hacer que el código funcione; sabe demostrar por qué es seguro y escalable.
      </div>
    </section>

    <!-- Slide 4: Modelo C-R-E-O -->
    <section class="slide">
      <h2>Fase 2: El Científico — Ingeniería de Requerimientos con C-R-E-O</h2>
      <p class="lead">Para obtener código de nivel de producción de un LLM, debes suministrar una especificación técnica formal.</p>
      
      <div class="grid-4">
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header">
            <span style="color: var(--accent);">C &bull; Contexto</span>
            <span class="expand-hint">[+]</span>
          </div>
          <p>Framework y versión.</p>
          <div class="card-details">
            "FastAPI 0.110+ con Python 3.10+ y Pydantic v2" o "PHP 8.2 con servidor integrado".
          </div>
        </div>

        <div class="card" onclick="toggleCard(this)">
          <div class="card-header">
            <span style="color: var(--accent-silver);">R &bull; Rol</span>
            <span class="expand-hint">[+]</span>
          </div>
          <p>Postura técnica esperada.</p>
          <div class="card-details">
            "Actúa como un arquitecto senior de APIs RESTful especialista en seguridad y validación de esquemas".
          </div>
        </div>

        <div class="card" onclick="toggleCard(this)">
          <div class="card-header">
            <span style="color: var(--accent-orange);">E &bull; Especificación</span>
            <span class="expand-hint">[+]</span>
          </div>
          <p>Contrato del Endpoint.</p>
          <div class="card-details">
            Verbo HTTP, ruta <code>POST /api/saludo</code>, validación de longitudes y códigos de estado (200, 400, 422).
          </div>
        </div>

        <div class="card" onclick="toggleCard(this)">
          <div class="card-header">
            <span style="color: var(--accent-green);">O &bull; Output</span>
            <span class="expand-hint">[+]</span>
          </div>
          <p>Formato de respuesta.</p>
          <div class="card-details">
            Únicamente el código modular de la ruta sin texto introductorio innecesario.
          </div>
        </div>
      </div>

      <div class="interactive-box">
        <code>Prompt Modelo: "Rol: Arquitecto API. Contexto: FastAPI. Especificación: POST /saludo que valide nombre >= 3 chars, emita 200 o 422. Output: Solo código."</code>
      </div>
    </section>

    <!-- Slide 5: Ponderación y Ecosistema -->
    <section class="slide">
      <h2>Ponderación Oficial y Ecosistema Tecnológico</h2>
      <div class="grid-2">
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header">
            <span>Criterios de Evaluación</span>
            <span class="expand-hint">[+]</span>
          </div>
          <ul>
            <li><strong>40% Laboratorios Diarios:</strong> Cuadernos Colab ejecutados + bitácoras en GitHub.</li>
            <li><strong>30% Proyecto Integrador:</strong> API RESTful Full-Stack con persistencia y frontend.</li>
            <li><strong>20% Evaluaciones Prácticas:</strong> 4 hitos prácticos de unidad.</li>
            <li><strong>10% Participación Activa:</strong> Sesiones síncronas en MS Teams.</li>
          </ul>
          <div class="card-details">
            La evaluación es continua y acumulativa; tu repositorio en GitHub es tu portafolio oficial de acreditación.
          </div>
        </div>

        <div class="card" onclick="toggleCard(this)">
          <div class="card-header">
            <span>Herramientas del Curso</span>
            <span class="expand-hint">[+]</span>
          </div>
          <ul>
            <li><strong>MS Teams:</strong> Aula virtual y grabaciones diarias de clase.</li>
            <li><strong>Moodle TecNM:</strong> Registro de calificaciones y entrega de enlaces.</li>
            <li><strong>Google Colab:</strong> Servidores embebidos y pruebas automatizadas diarias.</li>
            <li><strong>GitHub Web:</strong> Control de versiones y portafolio del estudiante.</li>
          </ul>
          <div class="card-details">
            En las semanas 7 y 8 integraremos <strong>GitHub Codespaces</strong> y <strong>Render</strong> para el despliegue final en producción.
          </div>
        </div>
      </div>
    </section>

    <!-- Slide 6: El Reto de Hoy -->
    <section class="slide">
      <h2>Laboratorio de Hoy: Preparación de Entorno y Diagnóstico HTTP</h2>
      <p class="lead">Sigue estos pasos en tu navegador para configurar tu repositorio personal e iniciar la práctica 01.</p>
      
      <div class="grid-2">
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header">
            <span style="color: var(--accent);">Paso 1: Fork en GitHub Web</span>
            <span class="expand-hint">[+]</span>
          </div>
          <p>Crea tu copia de trabajo en el navegador:</p>
          <div class="code-block">
1. Entra a: github.com/ijmarquezl/tecnm-desarrollo-web<br>
2. Clic en "Fork" &rarr; "Create fork"<br>
3. Abre README.md &rarr; Edita tu Nombre, Matrícula y Track<br>
4. Haz clic en "Commit changes..." para guardar
          </div>
          <div class="card-details">
            Desde tu repositorio podrás abrir el cuaderno con el botón <strong>"Open in Colab"</strong>.
          </div>
        </div>

        <div class="card" onclick="toggleCard(this)">
          <div class="card-header">
            <span style="color: var(--accent-green);">Paso 2: Servidor Diagnóstico y Test</span>
            <span class="expand-hint">[+]</span>
          </div>
          <p>Ejecuta la práctica 01 en Google Colab:</p>
          <div class="code-block">
1. Ejecuta el Paso 0 para verificar FastAPI o PHP<br>
2. Resuelve el endpoint manual (El Artesano)<br>
3. Formula tu matriz C-R-E-O (El Científico)<br>
4. Ejecuta el Test Harness HTTP (El Auditor)<br>
5. Sube tu bitácora auditorias/auditoria_sesion01.md
          </div>
          <div class="card-details">
            Verifica que el Test Harness devuelva códigos de estado válidos antes de hacer commit en tu repositorio.
          </div>
        </div>
      </div>

      <div class="interactive-box">
        <strong>Docente Titular:</strong> MCC. Iván Márquez Larios (<code>ijmarquezl</code>) &bull; TecNM Cancún
      </div>
    </section>
  </main>

  <footer>
    <div class="progress" id="slideIndicator">SLIDE 1 / 6</div>
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

    function updateSlides() {
      slides.forEach((slide, index) => {
        slide.classList.toggle('active', index === currentSlide);
      });
      indicator.textContent = `SLIDE ${currentSlide + 1} / ${slides.length}`;
      prevBtn.disabled = currentSlide === 0;
      nextBtn.disabled = currentSlide === slides.length - 1;
    }

    function nextSlide() {
      if (currentSlide < slides.length - 1) {
        currentSlide++;
        updateSlides();
      }
    }

    function prevSlide() {
      if (currentSlide > 0) {
        currentSlide--;
        updateSlides();
      }
    }

    function toggleCard(cardElement) {
      cardElement.classList.toggle('expanded');
      const hint = cardElement.querySelector('.expand-hint');
      if (hint) {
        hint.textContent = cardElement.classList.contains('expanded') ? '[-]' : '[+]';
      }
    }

    document.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight' || e.key === ' ') nextSlide();
      if (e.key === 'ArrowLeft') prevSlide();
    });
  </script>
</body>
</html>
"""

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
      <p class="lead">Sesión {n_str} del curso. Exploración conceptual, arquitectura del protocolo HTTP y diseño de servicios web con la Tríada Metodológica.</p>
      <div class="grid-3">
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span style="color: var(--accent);">01. El Artesano</span><span class="expand-hint">[+]</span></div>
          <p>Codificación manual sin IA para comprender el procesamiento de bajo nivel de la petición HTTP.</p>
          <div class="card-details">Desarrolla la intuición técnica de parseo de payloads, verbos y encabezados web.</div>
        </div>
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span style="color: var(--accent-silver);">02. El Científico</span><span class="expand-hint">[+]</span></div>
          <p>Formalización de contratos de API mediante especificación C-R-E-O y esquemas DTO/OpenAPI.</p>
          <div class="card-details">Define tipos, validaciones de rango y códigos de respuesta semánticos antes de pedir código al LLM.</div>
        </div>
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span style="color: var(--accent-green);">03. El Auditor</span><span class="expand-hint">[+]</span></div>
          <p>Test Harness automatizado en Colab para auditar códigos de estado HTTP y robustez del servidor.</p>
          <div class="card-details">Somete el endpoint a pruebas destructivas (400, 404, 422) y registra la bitácora en GitHub.</div>
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
        <strong>Invariante Web:</strong> Los encabezados y códigos de estado HTTP son el lenguaje universal de comunicación entre servicios desacoplados.
      </div>
    </section>

    <section class="slide">
      <h2>Arquitectura del Servidor y Protocolo: {am["titulo"]}</h2>
      <p class="lead">{am["descripcion"]}</p>
      <div class="grid-2">
        {cards_s3}
      </div>
    </section>

    <section class="slide">
      <h2>{cb["titulo"]}</h2>
      <p class="lead">Puntos críticos de falla que deben protegerse en la API y auditarse en las respuestas del LLM:</p>
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
            <li><strong>00–20 min:</strong> Estudio inicial e invariantes del protocolo.</li>
            <li><strong>20–35 min:</strong> Fase 1: El Artesano (Código manual sin IA).</li>
            <li><strong>35–45 min:</strong> Fase 2: El Científico (Prompt C-R-E-O).</li>
            <li><strong>45–55 min:</strong> Fase 3: El Auditor (Test Harness HTTP).</li>
            <li><strong>55–60 min:</strong> Sincronización y commit en GitHub.</li>
          </ul>
          <div class="card-details">Verifica que las pruebas del Test Harness terminen en verde antes de hacer commit.</div>
        </div>
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span>Evidencia Evaluada</span><span class="expand-hint">[+]</span></div>
          <p>Tu archivo <code>auditorias/auditoria_sesion{n_str}.md</code> debe contener la matriz C-R-E-O y el reporte crítico.</p>
          <div class="card-details">Cada entrega acumulada cuenta para el 40% de laboratorios y alimenta tu Proyecto Integrador.</div>
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
    print("🚀 Compilando presentaciones enriquecidas de Desarrollo Web (Bloque 1: Sesiones 01 a 10)...")
    os.makedirs("presentaciones", exist_ok=True)
    
    for num, data in TEORIA_WEB_BLOQUE_1.items():
        n_str = f"{num:02d}"
        out_path = f"presentaciones/sesion{n_str}.html"
        
        if data.get("es_encuadre", False):
            html_content = generar_html_encuadre_sesion1()
            print(f"  -> Generada Sesión {n_str}: Encuadre Formal Restaurado (6 slides)")
        else:
            html_content = compilar_presentacion_5_slides_web(num, data)
            print(f"  -> Generada Sesión {n_str}: {data['tema']} (5 slides)")
            
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)
            
    print("✅ Bloque 1 de presentaciones de Desarrollo Web actualizado exitosamente.")

if __name__ == "__main__":
    main()
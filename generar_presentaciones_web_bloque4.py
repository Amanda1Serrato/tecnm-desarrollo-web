#!/usr/bin/env python3
"""
Compilador de Presentaciones Enriquecidas (Bloque 4: Sesiones 31 a 40)
Materia: Desarrollo de Aplicaciones Web (DAB-2201)
Unidad: Despliegue en Producción, Cliente Fetch / SPA, Pruebas E2E e Hito Final
Autor: MCC. Iván Márquez Larios (ijmarquezl)
TecNM - Campus Cancún
"""

import os

TEORIA_WEB_BLOQUE_4 = {
    31: {
        "tema": "Contenedorización Básica con Docker y Dockerfiles",
        "unidad": "Bloque 4: Despliegue, Frontend SPA y Pruebas E2E",
        "teoria_principal": {
            "titulo": "Contenedorización, Inmutabilidad y Aislamiento de Entornos",
            "lead": "Docker empaqueta el código, el runtime, las dependencias del sistema y la configuración en un contenedor inmutable.",
            "tarjetas": [
                ("01. Contenedores vs Máquinas Virtuales", "Los contenedores comparten el kernel del sistema operativo anfitrión, siendo órdenes de magnitud más ligeros y rápidos que una VM.", "Garantiza el principio 'corre exactamente igual en mi máquina que en producción'."),
                ("02. Anatomía de un Dockerfile", "Instrucciones base: `FROM python:3.11-slim`, `WORKDIR /app`, `COPY requirements.txt .`, `RUN pip install`, `COPY . .`, `CMD [...]`.", "Cada instrucción genera una capa de solo lectura en el sistema de archivos de la imagen."),
                ("03. Construcción Multi-Etapa (Multi-Stage Builds)", "Separa el entorno de compilación (con compiladores pesados) del entorno final de ejecución ligero.", "Reduce el tamaño de la imagen de producción de cientos de MB a menos de 50 MB.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Caché de Capas y Optimización de Imágenes",
            "descripcion": "Estrategias de construcción eficiente en Docker:",
            "tarjetas": [
                ("Orden de Instrucciones para Caché", "Copiar e instalar `requirements.txt` o `composer.json` antes de copiar el código fuente de la aplicación.", "Evita reinstalar dependencias en cada cambio de código, acelerando los builds en segundos."),
                ("Archivo `.dockerignore`", "Excluye `.git`, `__pycache__`, `.env` y carpetas de pruebas de la imagen final.", "Previene la fuga accidental de credenciales y reduce el contexto de construcción.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Contenedorización",
            "items": [
                "Ejecutar el contenedor como usuario `root` en producción, exponiendo el host a riesgos de escalamiento de privilegios.",
                "Copiar archivos de entorno `.env` con contraseñas dentro de la imagen pública de Docker.",
                "Usar tags genéricos como `latest` en lugar de versiones fijas (`python:3.11.8-slim`), provocando roturas inesperadas."
            ]
        }
    },
    32: {
        "tema": "Despliegue en la Nube (Render / Codespaces) y Env Vars",
        "unidad": "Bloque 4: Despliegue, Frontend SPA y Pruebas E2E",
        "teoria_principal": {
            "titulo": "Metodología 12-Factor App y Despliegue Continuo (CD)",
            "lead": "El despliegue moderno desacopla la configuración del código fuente mediante variables de entorno inyectadas en tiempo de ejecución.",
            "tarjetas": [
                ("01. The Twelve-Factor App (Configuración)", "Toda configuración que cambie entre entornos (Dev, Staging, Prod) debe residir en variables de entorno del sistema operativo.", "El código base es estrictamente el mismo en todos los despliegues."),
                ("02. Plataformas PaaS (Render / Codespaces)", "Plataformas que automatizan la construcción, aprovisionamiento de certificados SSL/TLS y despliegue directo desde Git.", "Cada `git push origin main` dispara una compilación y despliegue sin tiempo de inactividad (*Zero-Downtime*)."),
                ("03. Gestión de Secretos y Variables Sensibles", "Las claves secretas (`SECRET_KEY`, `DATABASE_URL`) se configuran en el panel de la nube, nunca en el repositorio.", "Protege las credenciales corporativas ante repositorios públicos o filtraciones de código.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Carga de Variables en Tiempo de Arranque",
            "descripcion": "Lectura segura con `pydantic-settings` o `getenv`:",
            "tarjetas": [
                ("Validación de Configuración al Arrancar", "La aplicación valida que todas las variables requeridas existan antes de abrir puertos de red.", "Falla rápido (*Fail-Fast*) si falta una variable crítica de base de datos."),
                ("Terminación SSL/TLS Automática", "El PaaS gestiona los certificados HTTPS mediante Let's Encrypt de forma automática en el borde de la red.", "Cifra todo el tráfico entre el navegador del cliente y el balanceador del PaaS.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla en Despliegues Cloud",
            "items": [
                "Hacer commit del archivo `.env` local en GitHub exponiendo contraseñas de producción.",
                "Codificar rutas locales fijas (`C:\\Users\\...` o `/home/ivan/...`) que no existen en el contenedor Linux de producción.",
                "No configurar el puerto dinámico asignado por el PaaS mediante la variable `$PORT`."
            ]
        }
    },
    33: {
        "tema": "Servidores ASGI / WSGI en Producción (Uvicorn / Nginx)",
        "unidad": "Bloque 4: Despliegue, Frontend SPA y Pruebas E2E",
        "teoria_principal": {
            "titulo": "Arquitectura de Servidores Web de Alto Rendimiento",
            "lead": "En producción, la aplicación web se ejecuta detrás de un servidor de aplicaciones concurrente coordinado por un Proxy Inverso.",
            "tarjetas": [
                ("01. ASGI (Asynchronous Server Gateway Interface)", "Estándar asíncrono para Python que maneja miles de conexiones concurrentes I/O mediante un bucle de eventos.", "Uvicorn implementa ASGI sobre uvloop (escrito en C) para máxima velocidad de despacho."),
                ("02. Gestor de Procesos Worker (Gunicorn / Uvicorn Workers)", "Un proceso maestro coordina múltiples procesos trabajadores (*workers*) aprovechando todos los núcleos de la CPU.", "Si un worker colapsa por un error fatal, el maestro levanta uno nuevo instantáneamente."),
                ("03. Proxy Inverso (Nginx)", "Servidor frontal que maneja SSL/TLS, compresión Gzip, archivos estáticos y balanceo hacia los workers de la API.", "Protege a los servidores de aplicaciones de ataques directos de saturación lenta (*Slowloris*).")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Modelo de Procesos Multi-Worker en Producción",
            "descripcion": "Distribución de carga sobre núcleos de hardware:",
            "tarjetas": [
                ("Fórmula de Workers de CPU", "`Num_Workers = (2 * Num_Cores) + 1`.", "Maximiza el uso de CPU manteniendo un worker activo mientras otros esperan operaciones de I/O de base de datos."),
                ("Buffers y Timeouts de Nginx", "Nginx absorbe peticiones lentas de clientes móviles y las entrega a Uvicorn a velocidad de red local.", "Optimiza el rendimiento del runtime de backend.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Configuración de Servidores",
            "items": [
                "Ejecutar `uvicorn main:app --reload` en producción (la bandera `--reload` consume memoria y degrada el rendimiento).",
                "Configurar un solo worker en servidores multi-core desaprovechando la capacidad de la máquina.",
                "Servir archivos multimedia o estáticos pesados directamente desde FastAPI/PHP en lugar de usar Nginx o un CDN."
            ]
        }
    },
    34: {
        "tema": "Integración Frontend: Fetch API y JavaScript Asíncrono",
        "unidad": "Bloque 4: Despliegue, Frontend SPA y Pruebas E2E",
        "teoria_principal": {
            "titulo": "Consumo de APIs REST desde el Navegador Cliente",
            "lead": "La API `fetch()` nativa permite al navegador realizar peticiones HTTP asíncronas sin recargar la página web.",
            "tarjetas": [
                ("01. Promesas y Sintaxis `async / await`", "Manejo limpio de operaciones asíncronas no bloqueantes en JavaScript.", "Permite escribir código asíncrono de red con estructura secuencial y legible."),
                ("02. Configuración de Encabezados y Verbos", "Envío explicito de `method: 'POST'`, `headers: {'Content-Type': 'application/json'}` y `body: JSON.stringify(data)`.", "Conecta directamente la interfaz de usuario con los contratos de la API backend."),
                ("03. Inyección del Token Authorization Bearer", "Extracción del JWT desde `localStorage` o memoria y envío en el encabezado `Authorization: Bearer ${token}`.", "Permite al cliente acceder a rutas privadas autenticadas.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Ciclo de Respuesta y Parseo de JSON en Navegador",
            "descripcion": "Transformación de respuesta HTTP a objetos JavaScript:",
            "tarjetas": [
                ("Parseo en Dos Fases", "`const response = await fetch(...); const data = await response.json();`.", "La primera fase valida el código de estado (`response.ok`); la segunda deserializa el payload JSON."),
                ("Manejo de Errores de Red vs HTTP", "`catch()` solo captura fallos de red físicos (sin conexión); los errores 4xx y 5xx deben validarse con `if (!response.ok)`.", "Garantiza mensajes de error adecuados para el usuario.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla en Consumo de APIs",
            "items": [
                "Olvidar usar `JSON.stringify()` al enviar objetos en el body, enviando `[object Object]` corrupto.",
                "No capturar errores HTTP 401 para redirigir automáticamente al usuario a la pantalla de login.",
                "Almacenar tokens sensibles en variables globales accesibles fácilmente por scripts de terceros."
            ]
        }
    },
    35: {
        "tema": "Renderizado Dinámico del DOM y Estado del Cliente",
        "unidad": "Bloque 4: Despliegue, Frontend SPA y Pruebas E2E",
        "teoria_principal": {
            "titulo": "Manipulación del DOM y Reactividad Ligera",
            "lead": "El cliente web moderno actualiza dinámicamente secciones específicas de la interfaz en respuesta a cambios de datos.",
            "tarjetas": [
                ("01. Document Object Model (DOM)", "Representación en árbol de nodos de la estructura HTML que JavaScript puede mutar en tiempo real.", "Permite insertar, modificar o eliminar elementos sin refrescar el navegador."),
                ("02. Template Literals para Renderizado", "Uso de plantillas con backticks: `container.innerHTML = users.map(u => `<li>${u.nombre}</li>`).join('')`.", "Construye vistas dinámicas a partir de los arreglos JSON recibidos de la API."),
                ("03. Gestión de Estado en Cliente (Client State)", "Objeto JavaScript centralizado que almacena los datos activos de la sesión y la vista actual.", "Cualquier mutación del estado dispara el re-renderizado de la interfaz correspondiente.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Flujo de Renderizado Reactivo en Navegador",
            "descripcion": "Sincronización entre datos del backend y la pantalla:",
            "tarjetas": [
                ("Event Delegation en el DOM", "Escuchar eventos en un contenedor padre en lugar de asignar cientos de listeners a elementos hijos dinámicos.", "Optimiza el consumo de memoria en interfaces con tablas o listas extensas."),
                ("Prevención de XSS en Renderizado", "Uso de `textContent` o funciones de escape en lugar de insertar cadenas no confiables directamente con `innerHTML`.", "Protege a los usuarios de scripts inyectados en la interfaz.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Manipulación del DOM",
            "items": [
                "Reescribir todo el `document.body.innerHTML` en cada cambio de datos, destruyendo el foco del usuario y el estado de formularios.",
                "Fugas de memoria por no desvincular event listeners en elementos eliminados.",
                "Insertar entradas de usuarios directamente con `innerHTML` permitiendo vulnerabilidades XSS en el cliente."
            ]
        }
    },
    36: {
        "tema": "Arquitectura Single Page Application (SPA) Ligera",
        "unidad": "Bloque 4: Despliegue, Frontend SPA y Pruebas E2E",
        "teoria_principal": {
            "titulo": "Navegación Sin Recarga y Ruteo del Lado del Cliente",
            "lead": "Una SPA carga un solo documento HTML inicial y actualiza las vistas dinámicamente interceptando la navegación.",
            "tarjetas": [
                ("01. Ruteo por Hash (`#route`) y History API", "El navegador detecta cambios de ruta mediante `window.onhashchange` o `history.pushState()` sin solicitar una página nueva al servidor.", "Proporciona una experiencia de usuario fluida idéntica a una aplicación de escritorio."),
                ("02. Arquitectura Basada en Componentes Vistas", "Cada ruta (`#/login`, `#/dashboard`, `#/usuarios`) se mapea a una función renderizadora independiente.", "Mantiene el código frontend modular, escalable y fácil de mantener."),
                ("03. Desacoplamiento Total Frontend/Backend", "El frontend es un conjunto de archivos estáticos (HTML/CSS/JS); el backend es exclusivamente una API REST JSON.", "Permite alojar el frontend en servicios CDN ultrarrápidos (GitHub Pages / Vercel).")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Ruteador Minimalista en JavaScript",
            "descripcion": "Mapeo declarativo de rutas cliente:",
            "tarjetas": [
                ("Diccionario de Rutas", "`const routes = { '#/': HomeView, '#/login': LoginView, '#/perfil': ProfileView };`.", "El despachador lee `location.hash` e invoca la vista correspondiente en el contenedor principal."),
                ("Guardias de Navegación (Route Guards)", "Funciones que verifican la existencia del JWT antes de renderizar una vista protegida.", "Si el usuario no está autenticado, redirige automáticamente a `#/login`.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla en SPAs",
            "items": [
                "Fallo de recarga en servidores al usar History API sin configurar el fallback a `index.html` (error 404 en refresco).",
                "Permitir que el usuario navegue a vistas privadas mediante manipulación del hash sin validar el token con la API.",
                "Acumular datos en memoria entre cambios de pantalla sin limpiar formularios ni tablas."
            ]
        }
    },
    37: {
        "tema": "Pruebas Automatizadas E2E con Postman / Newman CLI",
        "unidad": "Bloque 4: Despliegue, Frontend SPA y Pruebas E2E",
        "teoria_principal": {
            "titulo": "Pruebas de Integración End-to-End y Automatización CI/CD",
            "lead": "Las pruebas E2E verifican que el sistema completo (red, auth, lógica y base de datos) funcione armónicamente de inicio a fin.",
            "tarjetas": [
                ("01. Colecciones de Pruebas en Postman", "Flujos secuenciales de peticiones HTTP: 1. Registro -> 2. Login -> 3. Guardar Token -> 4. Crear Recurso -> 5. Consultar Recurso.", "Simula el comportamiento real de un usuario interactuando con la API."),
                ("02. Aserciones JavaScript en Postman Tests", "Scripts de validación: `pm.response.to.have.status(200)`, `pm.expect(pm.response.json().status).to.eql('success')`.", "Valida automáticamente tanto los códigos de estado como el contenido de los payloads."),
                ("03. Ejecución Automatizada con Newman CLI", "Herramienta de línea de comandos para ejecutar colecciones de Postman dentro de pipelines de GitHub Actions o scripts locales.", "Bloquea el paso a producción si alguna prueba de la suite falla.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Variables Dinámicas de Entorno en Pruebas",
            "descripcion": "Paso de datos entre pasos de prueba consecutivos:",
            "tarjetas": [
                ("Extracción Automática de Tokens", "`pm.environment.set('token', pm.response.json().access_token);`.", "Inyecta el token obtenido en el login directamente en las peticiones subsecuentes de la colección."),
                ("Reportes de Cobertura y Fallos", "Newman emite reportes en formato CLI, HTML o JUnit XML.", "Facilita la auditoría visual y la trazabilidad de regresiones en el código.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Pruebas E2E",
            "items": [
                "Pruebas interdependientes que fallan si no se ejecutan en un orden estricto específico.",
                "No limpiar los datos de prueba creados en la base de datos tras la ejecución de la suite.",
                "Escribir aserciones que solo verifican el código HTTP (200) sin validar la estructura del JSON devuelto."
            ]
        }
    },
    38: {
        "tema": "Tareas en Segundo Plano (Background Tasks) Asíncronas",
        "unidad": "Bloque 4: Despliegue, Frontend SPA y Pruebas E2E",
        "teoria_principal": {
            "titulo": "Procesamiento Diferido y Operaciones No Bloqueantes",
            "lead": "Las tareas pesadas (envío de correos, generación de reportes, procesamiento de imágenes) deben ejecutarse fuera del ciclo Request/Response.",
            "tarjetas": [
                ("01. Respuesta Inmediata (HTTP 202 Accepted)", "El servidor acepta la petición, delega el procesamiento a un worker en segundo plano y responde al cliente de inmediato.", "Reduce la latencia de respuesta de segundos a milisegundos."),
                ("02. FastAPI `BackgroundTasks`", "Mecanismo nativo ligero para ejecutar funciones asíncronas inmediatamente después de devolver la respuesta HTTP.", "Ideal para operaciones secundarias que no requieren colas distribuidas complejas."),
                ("03. Colas Distribuidas (Celery / Redis / RabbitMQ)", "Arquitectura industrial para procesamiento masivo distribuido con reintentos y persistencia de tareas.", "Permite procesar millones de trabajos en paralelo desacoplados de la API web.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Ciclo de Ejecución en Background",
            "descripcion": "Separación del hilo web y el worker de procesamiento:",
            "tarjetas": [
                ("Inyección de `BackgroundTasks`", "`def registrar(user: UserDTO, bg: BackgroundTasks): bg.add_task(enviar_email, user.email); return {'ok': True}`.", "El email se procesa después de enviar los bytes de respuesta al cliente."),
                ("Manejo de Errores en Tareas Asíncronas", "Las excepciones en background no afectan la respuesta enviada al usuario.", "Requiere registro centralizado de logs para auditar fallos en tareas diferidas.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla en Background Tasks",
            "items": [
                "Pasar sesiones de base de datos activas a tareas en background que se cierran al terminar la petición HTTP.",
                "Saturar el pool de hilos del servidor con tareas intensivas en CPU que bloquean el bucle de eventos.",
                "Perder tareas críticas en memoria si el servidor se reinicia antes de ejecutarlas (requiere colas persistentes)."
            ]
        }
    },
    39: {
        "tema": "Monitoreo, Métricas de Salud (/health) y Profiling Web",
        "unidad": "Bloque 4: Despliegue, Frontend SPA y Pruebas E2E",
        "teoria_principal": {
            "titulo": "Observabilidad, Healthchecks y Métricas en Producción",
            "lead": "Una aplicación en producción debe exponer su estado interno para que balanceadores y sistemas de monitoreo puedan supervisarla.",
            "tarjetas": [
                ("01. Endpoint de Salud (`/health` o `/status`)", "Ruta estandarizada que verifica la conectividad con la base de datos, memoria disponible y servicios externos.", "Devuelve `HTTP 200 OK` si el sistema está operativo o `HTTP 503 Service Unavailable` si hay fallas."),
                ("02. Liveness vs Readiness Probes", "Liveness: '¿El proceso del servidor está vivo?'. Readiness: '¿El servidor está listo para recibir tráfico y la DB conectada?'.", "Estándar utilizado por Kubernetes, Render y AWS para reiniciar contenedores colgados."),
                ("03. Métricas de Rendimiento (Latencia P95 / P99)", "Monitoreo del percentil de tiempo de respuesta para identificar el 5% o 1% de peticiones más lentas del sistema.", "Permite detectar cuellos de botella antes de que afecten a la mayoría de los usuarios.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Diagnóstico y Profiling en Tiempo Real",
            "descripcion": "Inspección de salud del servicio web:",
            "tarjetas": [
                ("Estructura JSON de Healthcheck", "`{'status': 'healthy', 'db': 'connected', 'version': '1.0.0', 'uptime': 3600}`.", "Permite a herramientas como UptimeRobot o Prometheus alertar incidentes en tiempo real."),
                ("Profiling de Endpoints Lentos", "Uso de middlewares de tiempo para identificar qué consultas de base de datos consumen más de 500 ms.", "Guía las optimizaciones de índices y caché en la aplicación.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Monitoreo Web",
            "items": [
                "Healthchecks pesados que ejecutan consultas masivas en la base de datos en cada sondeo cada 5 segundos.",
                "Retornar HTTP 200 en `/health` a pesar de que la base de datos esté desconectada.",
                "Exponer información sensible de infraestructura (versiones exactas de kernels o contraseñas) en el endpoint público de salud."
            ]
        }
    },
    40: {
        "tema": "Hito 4: Demostración API Full-Stack en Producción con SPA",
        "unidad": "Bloque 4: Despliegue, Frontend SPA y Pruebas E2E",
        "teoria_principal": {
            "titulo": "Evaluación Integradora y Demostración de la Plataforma Web",
            "lead": "Culminación del curso. Demostración práctica de una plataforma web Full-Stack completa, segura y desplegada en la nube con SPA reactiva.",
            "tarjetas": [
                ("01. Sistema Full-Stack Integrado", "Backend RESTful asíncrono con base de datos relacional, auth JWT, RBAC, validación estricta y frontend SPA dinámico.", "Demuestra el dominio de la arquitectura web de extremo a extremo."),
                ("02. Despliegue Público en Producción", "API y cliente web accesibles públicamente con HTTPS en la nube (Render / Codespaces / GitHub Pages).", "Evidencia formal de software desplegado con estándares profesionales de la industria."),
                ("03. Entrega Final y Release en GitHub", "Etiquetado formal de la versión definitiva en el repositorio: `git tag v1.0-final`.", "Concluye el 30% del Proyecto Integrador y la acreditación final del curso.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Auditoría Final y Criterios de Acreditación",
            "descripcion": "Verificación del ecosistema en vivo:",
            "tarjetas": [
                ("Suite E2E Automatizada Exitosa", "Ejecución al 100% de la colección de pruebas en Newman/Postman validando todos los flujos de usuario.", "Certifica la solidez técnica y ausencia de regresiones en la plataforma."),
                ("Documentación de Arquitectura Completa", "Especificación OpenAPI viva, esquemas de base de datos, diagrama de capas y bitácoras de auditoría en GitHub.", "Constituye el portafolio profesional de evidencias del estudiante.")
            ]
        },
        "casos_borde": {
            "titulo": "Criterios de Acreditación del Hito 4",
            "items": [
                "La aplicación debe estar desplegada en la nube y accesible mediante HTTPS sin errores de servidor.",
                "El frontend SPA debe consumir la API REST de forma reactiva con manejo de tokens JWT y roles.",
                "El repositorio en GitHub debe contener las 40 bitácoras de auditoría completas y el tag `v1.0-final`."
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
      <p class="lead">Sesión {n_str} del curso. Despliegue en producción, arquitectura SPA en cliente, pruebas E2E y observabilidad con la Tríada Metodológica.</p>
      <div class="grid-3">
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span style="color: var(--accent);">01. El Artesano</span><span class="expand-hint">[+]</span></div>
          <p>Codificación manual sin IA para experimentar el consumo con Fetch, manejo de DOM y Dockerfiles.</p>
          <div class="card-details">Desarrolla la intuición técnica de peticiones de red asíncronas, estado cliente y contenedores.</div>
        </div>
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span style="color: var(--accent-silver);">02. El Científico</span><span class="expand-hint">[+]</span></div>
          <p>Especificación C-R-E-O para arquitecturas de despliegue PaaS, SPA sin recarga y suites E2E.</p>
          <div class="card-details">Define contratos de integración frontend-backend, tareas en background y healthchecks estandarizados.</div>
        </div>
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span style="color: var(--accent-green);">03. El Auditor</span><span class="expand-hint">[+]</span></div>
          <p>Test Harness automatizado con Newman CLI, verificación de latencia y pruebas de estado en vivo.</p>
          <div class="card-details">Somete la plataforma web completa a pruebas de estrés y registra el release final en GitHub.</div>
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
        <strong>Invariante de Producción:</strong> Una aplicación web profesional debe ser observable, escalable y reproducible en cualquier infraestructura.
      </div>
    </section>

    <section class="slide">
      <h2>Arquitectura de Despliegue y Frontend: {am["titulo"]}</h2>
      <p class="lead">{am["descripcion"]}</p>
      <div class="grid-2">
        {cards_s3}
      </div>
    </section>

    <section class="slide">
      <h2>{cb["titulo"]}</h2>
      <p class="lead">Puntos críticos de falla que deben prevenirse en producción y auditarse en las respuestas del LLM:</p>
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
            <li><strong>00–20 min:</strong> Fundamento teórico y arquitectura de producción.</li>
            <li><strong>20–35 min:</strong> Fase 1: El Artesano (Código manual sin IA).</li>
            <li><strong>35–45 min:</strong> Fase 2: El Científico (Prompt C-R-E-O).</li>
            <li><strong>45–55 min:</strong> Fase 3: El Auditor (Test Harness / Newman E2E).</li>
            <li><strong>55–60 min:</strong> Sincronización y commit en GitHub.</li>
          </ul>
          <div class="card-details">Verifica que las pruebas E2E terminen con 0 fallos antes de hacer el commit final.</div>
        </div>
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span>Evidencia Evaluada</span><span class="expand-hint">[+]</span></div>
          <p>Tu archivo <code>auditorias/auditoria_sesion{n_str}.md</code> debe contener la matriz C-R-E-O y el reporte crítico.</p>
          <div class="card-details">La entrega de la Sesión 40 concluye formalmente el Hito 4 y la acreditación final del curso.</div>
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
    print("🚀 Compilando presentaciones enriquecidas de Desarrollo Web (Bloque 4: Sesiones 31 a 40)...")
    os.makedirs("presentaciones", exist_ok=True)
    
    for num, data in TEORIA_WEB_BLOQUE_4.items():
        n_str = f"{num:02d}"
        out_path = f"presentaciones/sesion{n_str}.html"
        html_content = compilar_presentacion_5_slides_web(num, data)
        
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"  -> Generada Sesión {n_str}: {data['tema']} (5 slides)")
            
    print("✅ Bloque 4 de presentaciones de Desarrollo Web actualizado exitosamente. Las 40 sesiones están completas.")

if __name__ == "__main__":
    main()
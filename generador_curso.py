#!/usr/bin/env python3
"""
Generador Maestro del Curso: Desarrollo de Aplicaciones Web (DAB-2201)
Autor: MCC. Iván Márquez Larios (ijmarquezl)
TecNM - Campus Cancún
"""

import os
import json

MATRIZ_SESIONES = [
    # Bloque 1: Arquitectura Web, Protocolo HTTP y REST APIs
    (1, "Encuadre, Diagnóstico HTTP y Servidor en Colab", "Procesamiento manual de JSON de petición sin IA", "Contrato OpenAPI básico para endpoints POST", "Pruebas de códigos de estado HTTP 200, 400 y 422"),
    (2, "Gestión en GitHub Web y Métodos HTTP (GET, POST, PUT, DELETE)", "Enrutamiento manual por verbo HTTP", "Especificación semántica de verbos e idempotencia", "Pruebas de métodos no permitidos (HTTP 405)"),
    (3, "Headers, Content-Type y Negociación de Contenido", "Lectura y emisión manual de encabezados HTTP", "Invariantes de negociación (Content-Type vs Accept)", "Pruebas con tipos de contenido no soportados (415)"),
    (4, "Anatomía RESTful, URIs Nombres y Recursos", "Diseño de URIs jerárquicas sin verbos en la ruta", "Mapeo formal de recursos y parámetros de ruta", "Pruebas de peticiones a recursos inexistentes (404)"),
    (5, "Pydantic v2 / DTOs en PHP y Tipado Estático", "DTO manual con validación de tipos primitivos", "Esquema Pydantic v2 con validadores personalizados", "Pruebas de tipos incompatibles y coerción"),
    (6, "Validación Estricta, Constraints y Params Query/Body", "Filtro manual de rangos y longitudes de texto", "Validaciones Pydantic Field(ge=18, min_length=3)", "Pruebas de desbordamiento de cadenas y números negativos"),
    (7, "Especificación OpenAPI (Swagger) y ReDoc", "Anotación manual de metadata de endpoints", "Contrato Swagger/OpenAPI v3.1 interactivo", "Verificación de renderizado de interfaz Swagger UI"),
    (8, "Respuestas Semánticas y Excepciones HTTP Personalizadas", "Lanzamiento manual de excepciones estructuradas", "Manejador global de HTTPException y JSON response", "Pruebas de captura de errores sin crashing (HTTP 500)"),
    (9, "Middleware Web, Intercepción y Logging de Transacciones", "Middleware manual de tiempo de respuesta (X-Process-Time)", "Interceptor de peticiones y auditoría de IP/User-Agent", "Pruebas de inyección de encabezados de rastreo"),
    (10, "Hito 1: Mock API RESTful con OpenAPI y Validation Harness", "Integración de Router y esquemas de validación", "Contrato formal de API de primer hito semestral", "Suite integral de 10 pruebas HTTP destructivas"),

    # Bloque 2: Lógica de Negocio, Controladores y Autenticación Segura
    (11, "Arquitectura en Capas: Router, Servicio y Capa de Datos", "Separación manual de controladores y lógica", "Patrón Service Layer desacoplado", "Pruebas de aislamiento de errores en lógica de negocio"),
    (12, "Inyección de Dependencias (FastAPI Depends / PHP Container)", "Inyector de dependencias manual por funciones", "Contenedor IoC con Depends() en endpoints", "Pruebas de ciclo de vida de dependencias por request"),
    (13, "Manejo de Sesiones Stateful vs Stateless Tokens", "Simulador de tabla de sesiones en memoria", "Comparativa de arquitectura JWT vs Cookies de Sesión", "Pruebas de expiración y revocación de sesión"),
    (14, "Hashing Seguro de Contraseñas (Bcrypt / Argon2)", "Cifrado manual con Salting y Factor de Costo", "Hashing con passlib / password_hash() de PHP", "Pruebas contra ataques de Rainbow Tables y Timing"),
    (15, "Autenticación Stateless con JSON Web Tokens (JWT)", "Codificación Base64Url y firma HMAC-SHA256", "Generación y verificación de tokens JWT con PyJWT", "Pruebas con tokens alterados o firma inválida"),
    (16, "OAuth2 Password Flow y Header Authorization Bearer", "Extracción manual del encabezado Authorization", "Esquema OAuth2PasswordBearer y endpoint /token", "Pruebas de acceso no autorizado sin token (HTTP 401)"),
    (17, "Control de Acceso Basado en Roles (RBAC)", "Verificación manual de permisos de usuario (Admin/User)", "Middleware de roles dinámico basado en claims JWT", "Pruebas de acceso denegado por rol insuficiente (HTTP 403)"),
    (18, "Rate Limiting, Throttling y Prevención de Abuso", "Contador manual de peticiones por IP en memoria", "Rate Limiter deslizante con encabezados Retry-After", "Pruebas de ráfaga masiva y bloqueo temporal (HTTP 429)"),
    (19, "Sanitización de Entradas, Prevención de XSS e Inyecciones", "Limpieza manual de HTML y caracteres especiales", "Sanitizador de entradas y escapes de salida JSON/HTML", "Pruebas de inyección de scripts en payloads"),
    (20, "Hito 2: API con Inyección de Dependencias, Auth JWT y RBAC", "Integración de autenticación y autorización en API", "Contrato de seguridad y protección de rutas privadas", "Suite de pruebas con usuarios legítimos e intrusos"),

    # Bloque 3: Persistencia Relacional, ORM y Seguridad OWASP
    (21, "Fundamentos de Persistencia: SQLite / PostgreSQL y Drivers", "Conexión manual y ejecución de sentencias SQL", "Patrón Singleton de pool de conexiones asíncronas", "Pruebas de recuperación ante desconexión de DB"),
    (22, "Modelado Relacional (1:1, 1:N, N:M) con ORMs", "Definición de tablas relacionales en código", "Modelos SQLAlchemy 2.0 / Doctrine ORM con llaves foráneas", "Pruebas de integridad referencial y cascadas"),
    (23, "Operaciones CRUD Transaccionales y Async Sessions", "Operaciones de inserción y consulta manual", "Repositorio asíncrono con AsyncSession y commit", "Pruebas de inserción doble y manejo de llaves únicas"),
    (24, "Migraciones de Base de Datos con Alembic / Phinx", "Script SQL de actualización de esquema", "Control de versiones de base de datos con Alembic", "Pruebas de actualización (upgrade) y reversión (downgrade)"),
    (25, "Consultas Complejas, Joins y Carga Ansiosa (Eager Loading)", "Consulta SQL con INNER JOIN manual", "Consultas ORM con selectinload / joinedload", "Prevención del problema N+1 de consultas en bucle"),
    (26, "Transacciones ACID, Aislamiento y Rollback", "Bloque try/except con rollback() explicito", "Manejador transaccional con nivel de aislamiento serializable", "Pruebas de aborto por falla intermedia y consistencia"),
    (27, "Blindaje OWASP: Prevención Total de SQL Injection (SQLi)", "Demostración de vulnerabilidad SQLi en consulta cruda", "Consultas parametrizadas obligatorias y ORM seguro", "Auditoría con payloads de inyección SQL destructivos"),
    (28, "Blindaje Web: Cross-Origin Resource Sharing (CORS)", "Encabezados manuales Access-Control-Allow-Origin", "Middleware CORSMiddleware configurado con orígenes válidos", "Pruebas de peticiones pre-flight OPTIONS entre dominios"),
    (29, "Protección Anti-CSRF y Cookies HttpOnly / SameSite", "Manejador de tokens CSRF en formularios", "Configuración de Cookies seguras Secure; HttpOnly; SameSite=Lax", "Pruebas de falsificación de peticiones entre sitios"),
    (30, "Hito 3: API Persistente con ORM, Migraciones y Blindaje OWASP", "Integración de capa de datos persistente y seguridad", "Contrato completo de API transaccional auditada", "Batería de pruebas de penetración y estrés de datos"),

    # Bloque 4: Despliegue en Producción, Client Fetch / SPA y Pruebas E2E
    (31, "Contenedorización Básica con Docker y Dockerfiles", "Escribir Dockerfile manual para la aplicación web", "Multi-stage build optimizado para Python/PHP en producción", "Pruebas de construcción e inspección de imagen Docker"),
    (32, "Despliegue en la Nube (Render / Codespaces) y Env Vars", "Lector manual de variables de entorno .env", "Configuración de despliegue continuo (CD) desde GitHub", "Pruebas de disponibilidad pública de endpoint en la nube"),
    (33, "Servidores ASGI / WSGI en Producción (Uvicorn / Nginx)", "Configuración de ejecución con múltiples workers", "Proxy inverso Nginx canalizando tráfico hacia Uvicorn", "Pruebas de manejo de concurrencia y conexiones sostenidas"),
    (34, "Integración Frontend: Fetch API y JavaScript Asíncrono", "Petición fetch() manual con async/await en navegador", "Manejador de respuestas JSON y renderizado en DOM", "Pruebas de captura de errores de red y HTTP 4xx/5xx"),
    (35, "Renderizado Dinámico del DOM y Estado del Cliente", "Actualización dinámica de elementos HTML sin recargar", "Gestor de estado ligero en JavaScript para la interfaz", "Pruebas de reactividad ante cambios de datos en la API"),
    (36, "Arquitectura Single Page Application (SPA) Ligera", "Ruteador JavaScript por Hash (#route) manual", "SPA completa interactuando con la API backend REST", "Pruebas de navegación sin recarga de página (No-Reload)"),
    (37, "Pruebas Automatizadas E2E con Postman / Newman CLI", "Colección de pruebas Postman con aserciones JS", "Ejecución automatizada de suite E2E en CLI con Newman", "Pruebas integrales de flujo completo de usuario"),
    (38, "Tareas en Segundo Plano (Background Tasks) Asíncronas", "Procesamiento diferido manual en hilo secundario", "Background Tasks de FastAPI para envío de emails/procesamiento", "Pruebas de respuesta inmediata (HTTP 202) sin bloqueo"),
    (39, "Monitoreo, Métricas de Salud (/health) y Profiling Web", "Endpoint de diagnóstico manual de estado de DB y memoria", "Healthcheck estandarizado con tiempos de respuesta de servicios", "Pruebas de simulación de caídas de servicios externos"),
    (40, "Hito 4: Demostración API Full-Stack en Producción con SPA", "Sistema Full-Stack completo en producción", "Reporte final de arquitectura, seguridad y despliegue", "Demostración en vivo de plataforma web cliente-servidor")
]

def construir_html(num, tema, artesano, cientifico, auditor):
    n_str = f"{num:02d}"
    lineas = [
        "<!DOCTYPE html>",
        '<html lang="es">',
        "<head>",
        '  <meta charset="UTF-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f"  <title>Sesión {n_str}: {tema} | Desarrollo de Aplicaciones Web</title>",
        "  <style>",
        "    :root {",
        "      --bg: #f4f8fb; --card-bg: rgba(255, 255, 255, 0.88); --card-bg-hover: rgba(255, 255, 255, 0.98);",
        "      --border: #d0dbe5; --border-focus: #0969da; --accent: #0969da; --accent-green: #1a7f37;",
        "      --accent-silver: #627282; --text: #334155; --text-bright: #0f172a; --font-mono: 'Fira Code', monospace;",
        "    }",
        "    * { box-sizing: border-box; margin: 0; padding: 0; }",
        "    body { background-color: var(--bg); color: var(--text); font-family: -apple-system, sans-serif; height: 100vh; overflow: hidden; display: flex; flex-direction: column; }",
        "    header { padding: 12px 28px; background: rgba(255, 255, 255, 0.85); border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }",
        "    .brand { font-weight: 700; color: var(--text-bright); font-size: 0.95rem; }",
        "    .tag { background-color: #ddf4ff; color: var(--accent); padding: 4px 12px; border-radius: 12px; font-size: 0.75rem; font-family: var(--font-mono); font-weight: 600; }",
        "    main { flex: 1; display: flex; position: relative; overflow: hidden; }",
        "    .slide { position: absolute; inset: 0; padding: 30px 60px; display: flex; flex-direction: column; justify-content: center; opacity: 0; visibility: hidden; transform: translateX(30px); transition: all 0.3s ease; }",
        "    .slide.active { opacity: 1; visibility: visible; transform: translateX(0); }",
        "    h1 { font-size: 2rem; color: var(--text-bright); margin-bottom: 12px; }",
        "    h2 { font-size: 1.5rem; color: var(--text-bright); margin-bottom: 16px; }",
        "    p.lead { font-size: 1.05rem; line-height: 1.5; max-width: 900px; margin-bottom: 18px; color: #475569; }",
        "    .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }",
        "    .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }",
        "    .card { background: var(--card-bg); border: 1px solid var(--border); border-radius: 10px; padding: 18px; cursor: pointer; transition: all 0.25s ease; }",
        "    .card:hover { background: var(--card-bg-hover); border-color: var(--border-focus); transform: translateY(-2px); }",
        "    .card.expanded { border-color: var(--accent); background: #ffffff; }",
        "    .card-header { font-weight: 600; color: var(--text-bright); margin-bottom: 8px; display: flex; justify-content: space-between; }",
        "    .expand-hint { font-size: 0.75rem; color: var(--accent); font-family: var(--font-mono); }",
        "    .card p, .card li { font-size: 0.88rem; line-height: 1.45; color: var(--text); }",
        "    .card-details { max-height: 0; overflow: hidden; opacity: 0; transition: all 0.3s ease; font-size: 0.82rem; color: #475569; }",
        "    .card.expanded .card-details { max-height: 240px; opacity: 1; margin-top: 10px; padding-top: 10px; border-top: 1px dashed var(--border); }",
        "    .interactive-box { margin-top: 18px; padding: 14px 18px; background: #ffffff; border: 1px solid var(--border); border-left: 4px solid var(--accent); border-radius: 6px; font-family: var(--font-mono); font-size: 0.85rem; }",
        "    footer { padding: 12px 28px; background: rgba(255, 255, 255, 0.85); border-top: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }",
        "    .progress { font-size: 0.85rem; font-family: var(--font-mono); color: var(--accent); font-weight: 600; }",
        "    .controls { display: flex; gap: 10px; }",
        "    button { background: #ffffff; color: var(--text-bright); border: 1px solid var(--border); padding: 7px 18px; border-radius: 6px; cursor: pointer; font-weight: 600; }",
        "    button:hover { background: #f1f5f9; }",
        "    button:disabled { opacity: 0.4; cursor: not-allowed; }",
        "  </style>",
        "</head>",
        "<body>",
        "  <header>",
        "    <div class=\"brand\">TecNM Cancún &bull; DAB-2201</div>",
        f"    <div class=\"tag\">SESIÓN {n_str} / 40 &bull; {tema}</div>",
        "  </header>",
        "  <main>",
        '    <section class="slide active">',
        '      <div class="tag" style="width: fit-content; margin-bottom: 10px;">DESARROLLO DE APLICACIONES WEB</div>',
        f"      <h1>{tema}</h1>",
        f"      <p class=\"lead\">Sesión {n_str} del curso. Desarrollo de servicios web, arquitectura de backend y seguridad con la Tríada Metodológica.</p>",
        '      <div class="grid-3">',
        '        <div class="card" onclick="toggleCard(this)">',
        '          <div class="card-header"><span style="color: var(--accent);">01. El Artesano</span><span class="expand-hint">[+]</span></div>',
        f"          <p>Codificación manual sin IA: <strong>{artesano}</strong>.</p>",
        '          <div class="card-details">Desarrolla la intuición técnica del protocolo HTTP y manejo directo de payloads antes de usar librerías avanzadas.</div>',
        "        </div>",
        '        <div class="card" onclick="toggleCard(this)">',
        '          <div class="card-header"><span style="color: var(--accent-silver);">02. El Científico</span><span class="expand-hint">[+]</span></div>',
        f"          <p>Especificación C-R-E-O: <strong>{cientifico}</strong>.</p>",
        '          <div class="card-details">Define el contrato OpenAPI formal, esquemas de validación y estructura del prompt técnico.</div>',
        "        </div>",
        '        <div class="card" onclick="toggleCard(this)">',
        '          <div class="card-header"><span style="color: var(--accent-green);">03. El Auditor</span><span class="expand-hint">[+]</span></div>',
        f"          <p>Test Harness Automatizado: <strong>{auditor}</strong>.</p>",
        '          <div class="card-details">Somete el servidor web en Colab a peticiones automatizadas y verifica respuestas semánticas en GitHub.</div>',
        "        </div>",
        "      </div>",
        "    </section>",
        '    <section class="slide">',
        "      <h2>Dinámica de la Sesión y Entregables</h2>",
        '      <div class="grid-2">',
        '        <div class="card" onclick="toggleCard(this)">',
        '          <div class="card-header"><span>Estructura de la Clase (60 min)</span><span class="expand-hint">[+]</span></div>',
        "          <ul>",
        "            <li><strong>00–20 min:</strong> Fundamento conceptual y arquitectura del protocolo.</li>",
        "            <li><strong>20–35 min:</strong> Fase 1: El Artesano (Código manual).</li>",
        "            <li><strong>35–45 min:</strong> Fase 2: El Científico (Prompt C-R-E-O).</li>",
        "            <li><strong>45–55 min:</strong> Fase 3: El Auditor (Test Harness HTTP).</li>",
        "            <li><strong>55–60 min:</strong> Sincronización y commit en GitHub.</li>",
        "          </ul>",
        '          <div class="card-details">Asegúrate de verificar los códigos de estado HTTP en el Test Harness antes de guardar la bitácora.</div>',
        "        </div>",
        '        <div class="card" onclick="toggleCard(this)">',
        '          <div class="card-header"><span>Evidencia Evaluada</span><span class="expand-hint">[+]</span></div>',
        f"          <p>Tu archivo <code>auditorias/auditoria_sesion{n_str}.md</code> debe contener la matriz C-R-E-O y el reporte crítico.</p>",
        '          <div class="card-details">El progreso acumulado cuenta para el 40% de laboratorios y alimenta tu Proyecto Integrador.</div>',
        "        </div>",
        "      </div>",
        '      <div class="interactive-box">',
        '        <strong>Docente Titular:</strong> MCC. Iván Márquez Larios (<code>ijmarquezl</code>) &bull; TecNM Cancún',
        "      </div>",
        "    </section>",
        "  </main>",
        "  <footer>",
        '    <div class="progress" id="slideIndicator">SLIDE 1 / 2</div>',
        '    <div class="controls">',
        '      <button id="prevBtn" onclick="prevSlide()" disabled>&larr; Anterior</button>',
        '      <button id="nextBtn" onclick="nextSlide()">Siguiente &rarr;</button>',
        "    </div>",
        "  </footer>",
        "  <script>",
        "    let currentSlide = 0;",
        "    const slides = document.querySelectorAll('.slide');",
        "    const indicator = document.getElementById('slideIndicator');",
        "    const prevBtn = document.getElementById('prevBtn');",
        "    const nextBtn = document.getElementById('nextBtn');",
        "    function updateSlides() {",
        "      slides.forEach((slide, index) => slide.classList.toggle('active', index === currentSlide));",
        "      indicator.textContent = `SLIDE ${currentSlide + 1} / ${slides.length}`;",
        "      prevBtn.disabled = currentSlide === 0;",
        "      nextBtn.disabled = currentSlide === slides.length - 1;",
        "    }",
        "    function nextSlide() { if (currentSlide < slides.length - 1) { currentSlide++; updateSlides(); } }",
        "    function prevSlide() { if (currentSlide > 0) { currentSlide--; updateSlides(); } }",
        "    function toggleCard(card) {",
        "      card.classList.toggle('expanded');",
        "      const hint = card.querySelector('.expand-hint');",
        "      if (hint) hint.textContent = card.classList.contains('expanded') ? '[-]' : '[+]';",
        "    }",
        "    document.addEventListener('keydown', (e) => {",
        "      if (e.key === 'ArrowRight' || e.key === ' ') nextSlide();",
        "      if (e.key === 'ArrowLeft') prevSlide();",
        "    });",
        "  </script>",
        "</body>",
        "</html>"
    ]
    return "\n".join(lineas)

def construir_ipynb(num, tema, artesano, cientifico, auditor):
    n_str = f"{num:02d}"
    nb = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"# Desarrollo de Aplicaciones Web (DAB-2201)\n",
                    f"## Sesión {n_str}: {tema}\n",
                    f"**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)\n",
                    f"**Repositorio Maestro:** `https://github.com/ijmarquezl/tecnm-desarrollo-web`\n",
                    f"\n---\n",
                    f"### Protocolo de la Sesión\n",
                    f"1. **Fase 1 (El Artesano):** Resolver a mano: *{artesano}*.\n",
                    f"2. **Fase 2 (El Científico):** Definir contrato C-R-E-O: *{cientifico}* y formular prompt.\n",
                    f"3. **Fase 3 (El Auditor):** Someter el servidor al Test Harness: *{auditor}*.\n",
                    f"4. **Entrega:** Documentar en `auditorias/auditoria_sesion{n_str}.md`."
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": ["### Paso 0: Inicialización del Entorno (FastAPI y PHP 8+)"]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import os\n",
                    "print('⏳ Instalando FastAPI, Uvicorn y HTTPX para pruebas...')\n",
                    "!pip install -q fastapi uvicorn httpx pydantic passlib python-jose[cryptography] sqlalchemy alembic\n",
                    "if os.system('which php > /dev/null 2>&1') != 0:\n",
                    "    print('⏳ Instalando PHP CLI...')\n",
                    "    !apt-get update -qq && apt-get install -y -qq php-cli > /dev/null 2>&1\n",
                    "print('✅ Entorno Web listo:')\n",
                    "!python3 --version\n",
                    "!php -v | head -n 1"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"---\n",
                    f"## SECCIÓN A: TRACK PYTHON / FASTAPI\n",
                    f"### Fase 1: El Artesano (15 min - Sin IA)\n",
                    f"**Reto:** {artesano}"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    f"%%writefile app_artesano.py\n",
                    "from fastapi import FastAPI, HTTPException, status\n",
                    "from pydantic import BaseModel\n",
                    "\n",
                    "app = FastAPI(title=\"API Artesano\")\n",
                    "\n",
                    "class PayloadRequest(BaseModel):\n",
                    "    dato: str\n",
                    "\n",
                    "# TODO (El Artesano): Implementar lógica manual del endpoint\n",
                    "@app.post(\"/api/recurso\")\n",
                    "def procesar_recurso(payload: PayloadRequest):\n",
                    "    if not payload.dato.strip():\n",
                    "        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=\"Dato vacio\")\n",
                    "    return {\"status\": \"success\", \"mensaje\": f\"Procesado: {payload.dato}\"}\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"### Fase 2: El Científico (Prompting C-R-E-O)\n",
                    f"Pega aquí la implementación optimizada propuesta por la IA:"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    f"%%writefile app_ia.py\n",
                    "from fastapi import FastAPI\n",
                    "\n",
                    "# Pega aquí el código generado por la IA para auditarlo\n"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"### Fase 3: El Auditor (Test Harness HTTP)\n",
                    f"Pruebas de servidor: {auditor}"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import threading\n",
                    "import time\n",
                    "import uvicorn\n",
                    "import httpx\n",
                    "from app_artesano import app\n",
                    "\n",
                    "def run_server():\n",
                    "    uvicorn.run(app, host=\"127.0.0.1\", port=8000, log_level=\"warning\")\n",
                    "\n",
                    "server_thread = threading.Thread(target=run_server, daemon=True)\n",
                    "server_thread.start()\n",
                    "time.sleep(1.5)\n",
                    "\n",
                    "client = httpx.Client(base_url=\"http://127.0.0.1:8000\")\n",
                    f"print(\"=== AUDITORIA CRITICA WEB: SESION {n_str} ===\\n\")\n",
                    "r = client.post(\"/api/recurso\", json={\"dato\": \"Prueba Test Harness\"})\n",
                    "print(f\"Respuesta Servidor: HTTP {r.status_code} - {r.json()}\")\n",
                    "assert r.status_code == 200\n",
                    "print(\"PASO ✅ - Test Harness HTTP ejecutado con exito.\")\n"
                ]
            }
        ],
        "metadata": {"language_info": {"name": "python"}},
        "nbformat": 4,
        "nbformat_minor": 2
    }
    return json.dumps(nb, indent=2, ensure_ascii=False)

def construir_md(num, tema, artesano, cientifico, auditor):
    n_str = f"{num:02d}"
    lineas = [
        f"# Bitácora de Requerimientos y Auditoría IA — Sesión {n_str}",
        "**Materia:** Desarrollo de Aplicaciones Web (DAB-2201)  ",
        f"**Tema:** {tema}  ",
        "**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  ",
        "**Estudiante:** [Nombre Completo]  ",
        "**Matrícula:** [No. de Control]  ",
        "**Track:** [ Python/FastAPI | PHP 8+ ]  ",
        "",
        "---",
        "",
        "## 1. Fase 1: El Artesano (Dificultad Manual)",
        f"*Reto:* {artesano}  ",
        "*Describe qué dificultad encontraste al procesar la petición HTTP o validar campos a mano:*",
        "> ",
        "",
        "---",
        "",
        "## 2. Fase 2: El Científico (Ingeniería de Requerimientos C-R-E-O)",
        "",
        "### 2.1 Matriz de Especificación Formal (Contrato OpenAPI / DTO)",
        "| Elemento C-R-E-O | Definición Técnica |",
        "| :--- | :--- |",
        "| **Contexto (C)** | FastAPI 0.110+ (Python 3.10+) o PHP 8.2 con servidor embebido |",
        "| **Rol (R)** | Arquitecto de software senior especialista en APIs RESTful y Seguridad Web |",
        f"| **Especificación (E)** | {cientifico} |",
        "| **Output (O)** | Solo código modular, esquemas Pydantic/DTO y códigos HTTP semánticos |",
        "",
        "### 2.2 Prompt Estructurado",
        "```text",
        "[Pega aquí el prompt formal que redactaste para la IA]",
        "```",
        "",
        "---",
        "",
        "## 3. Código Devuelto por el Modelo",
        "```python",
        "# Código devuelto por el LLM",
        "```",
        "",
        "---",
        "",
        "## 4. Fase 3: El Auditor (Resultados del Test Harness HTTP)",
        f"*Pruebas ejecutadas:* {auditor}",
        "",
        "* [ ] Respuestas semánticas correctas (`200 OK`, `201 Created`, `400 Bad Request`, `422 Unprocessable`).",
        "* [ ] No existen respuestas HTTP `500 Internal Server Error` no capturadas.",
        "* [ ] Encabezados `Content-Type: application/json` correctamente configurados.",
        "",
        "### Reporte Crítico",
        "*¿Qué código de estado HTTP o falla de seguridad omitió la IA y cómo lo corregiste?*",
        "> ",
        "",
        "---",
        "**Firma digital:** [Usuario de GitHub]"
    ]
    return "\n".join(lineas)

def main():
    print("🚀 Generando estructura completa del curso Desarrollo de Aplicaciones Web...")
    os.makedirs("presentaciones", exist_ok=True)
    os.makedirs("plantillas", exist_ok=True)
    os.makedirs("auditorias", exist_ok=True)
    os.makedirs("proyecto_integrador/docs", exist_ok=True)
    os.makedirs("proyecto_integrador/src", exist_ok=True)
    os.makedirs("proyecto_integrador/tests", exist_ok=True)

    readme_rows = []

    for num, tema, artesano, cientifico, auditor in MATRIZ_SESIONES:
        n_str = f"{num:02d}"
        lab_dir = f"laboratorios/sesion{n_str}"
        os.makedirs(lab_dir, exist_ok=True)

        html_path = f"presentaciones/sesion{n_str}.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(construir_html(num, tema, artesano, cientifico, auditor))

        ipynb_path = f"{lab_dir}/sesion{n_str}_laboratorio.ipynb"
        with open(ipynb_path, "w", encoding="utf-8") as f:
            f.write(construir_ipynb(num, tema, artesano, cientifico, auditor))

        md_path = f"plantillas/auditoria_sesion{n_str}.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(construir_md(num, tema, artesano, cientifico, auditor))

        colab_badge = f"[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ijmarquezl/tecnm-desarrollo-web/blob/main/{ipynb_path})"
        slides_link = f"[Ver Diapositivas](https://ijmarquezl.github.io/tecnm-desarrollo-web/{html_path})"
        readme_rows.append(f"| **Sesión {n_str}** | {tema} | {slides_link} | {colab_badge} |")

    encabezado_readme = [
        "# Desarrollo de Aplicaciones Web (DAB-2201)",
        "",
        "Repositorio oficial y entorno de laboratorio interactivo para el curso de **Desarrollo de Aplicaciones Web** del Tecnológico Nacional de México / Instituto Tecnológico de Cancún.",
        "",
        "**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)",
        "",
        "---",
        "",
        "## 🚀 Flujo de Trabajo en la Nube (100% en Navegador)",
        "1. Realiza un **Fork** de este repositorio a tu cuenta personal de GitHub.",
        "2. Identifícate editando este `README.md` con tu nombre, matrícula y track (**Python/FastAPI** o **PHP 8+**).",
        "3. Abre la sesión correspondiente con el botón **Open in Colab**.",
        "4. Sigue el ciclo **El Artesano** $\\to$ **El Científico** $\\to$ **El Auditor**.",
        "5. Copia la plantilla de `plantillas/auditoria_sesionXX.md` a `auditorias/auditoria_sesionXX.md` en tu Fork y realiza el commit.",
        "",
        "---",
        "",
        "## 🏗️ Proyecto Integrador Semestral (30%)",
        "* **Hito 1 (Sesión 10):** Mock API RESTful con Especificación OpenAPI y Validation Harness.",
        "* **Hito 2 (Sesión 20):** API con Inyección de Dependencias, Autenticación JWT y Roles (RBAC).",
        "* **Hito 3 (Sesión 30):** API Persistente con Base de Datos Relacional, Migraciones y Blindaje OWASP.",
        "* **Hito 4 (Sesión 40):** Demostración API Full-Stack Desplegada en Producción con Client Frontend.",
        "",
        "---",
        "",
        "## 📚 Índice General de las 40 Sesiones",
        "",
        "| Sesión | Tema Principal | Presentación | Laboratorio |",
        "| :--- | :--- | :---: | :---: |"
    ]

    pie_readme = [
        "",
        "---",
        "",
        "## 📋 Criterios de Evaluación Oficial",
        "* **40% Laboratorios Diarios:** Cuadernos Colab ejecutados y bitácoras en GitHub.",
        "* **30% Proyecto Integrador:** API RESTful Full-Stack con persistencia y frontend (4 hitos).",
        "* **20% Evaluaciones Prácticas:** 4 hitos prácticos de unidad.",
        "* **10% Participación Activa:** Sesiones síncronas en MS Teams.",
        "",
        "---",
        "**Docente Titular:** MCC. Iván Márquez Larios (`ijmarquezl`)  ",
        "**Tecnológico Nacional de México — Campus Cancún**"
    ]

    readme_final = "\n".join(encabezado_readme + readme_rows + pie_readme)
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_final)

    print("✅ Generación completa exitosa: 40 HTMLs, 40 IPYNBs, 40 MDs y README.md listos para Desarrollo Web.")

if __name__ == "__main__":
    main()
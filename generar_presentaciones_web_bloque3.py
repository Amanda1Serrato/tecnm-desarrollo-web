#!/usr/bin/env python3
"""
Compilador de Presentaciones Enriquecidas (Bloque 3: Sesiones 21 a 30)
Materia: Desarrollo de Aplicaciones Web (DAB-2201)
Unidad: Persistencia Relacional, ORM, Migraciones y Blindaje OWASP
Autor: MCC. Iván Márquez Larios (ijmarquezl)
TecNM - Campus Cancún
"""

import os

TEORIA_WEB_BLOQUE_3 = {
    21: {
        "tema": "Fundamentos de Persistencia: SQLite / PostgreSQL y Drivers",
        "unidad": "Bloque 3: Persistencia Relacional, ORM y OWASP",
        "teoria_principal": {
            "titulo": "Persistencia Relacional, Motores y Drivers Asíncronos",
            "lead": "La capa de persistencia garantiza que el estado de la aplicación sobreviva al reinicio del servidor o proceso web.",
            "tarjetas": [
                ("01. Motores SQLite vs PostgreSQL", "SQLite es un motor embebido basado en archivos para desarrollo/testing; PostgreSQL es un SGBD relacional cliente-servidor para producción.", "Ambos implementan el estándar SQL pero difieren en concurrencia y tipos avanzadores."),
                ("02. Drivers y Conectores (psycopg3 / aiorsqlite)", "Bibliotecas de bajo nivel que gestionan la comunicación por sockets TCP o archivos con el motor SQL.", "Los drivers asíncronos evitan bloquear el bucle de eventos del servidor web durante lecturas/escrituras."),
                ("03. Pool de Conexiones (Connection Pooling)", "Administración de un conjunto reutilizable de conexiones abiertas a la base de datos.", "Elimina la latencia de handshakes TCP y autenticación en cada petición HTTP.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Gestión del Pool de Conexiones en Memoria",
            "descripcion": "Ciclo de vida de sockets hacia la base de datos:",
            "tarjetas": [
                ("Concurrencia sin Agotamiento", "El pool limita el número máximo de conexiones abiertas simultáneamente (ej. `max_overflow=10`).", "Previene que ráfagas de tráfico tumben el servidor de base de datos por saturación de conexiones."),
                ("Patrón Singleton en la Engine", "Instancia única `create_async_engine()` compartida en toda la aplicación.", "Garantiza un control centralizado de los parámetros de reconexión y timeouts.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Conectividad a Bases de Datos",
            "items": [
                "Crear una nueva instancia de `Engine` o reconectar a la DB dentro de cada llamada a handler HTTP.",
                "Dejar conexiones colgadas sin devolver al pool al ocurrir excepciones en la ejecución de la consulta.",
                "Usar SQLite en producción con peticiones de escritura concurrentes masivas provocando bloqueos de base de datos (`database is locked`)."
            ]
        }
    },
    22: {
        "tema": "Modelado Relacional (1:1, 1:N, N:M) con ORMs",
        "unidad": "Bloque 3: Persistencia Relacional, ORM y OWASP",
        "teoria_principal": {
            "titulo": "Mapeo Objeto-Relacional (ORM) y Relaciones",
            "lead": "Un ORM (Object-Relational Mapping) traduce tablas y filas de SQL a clases y objetos en el lenguaje de programación.",
            "tarjetas": [
                ("01. Mapeo Tablas -> Clases (SQLAlchemy 2.0)", "Las tablas se declaran como clases derivadas de `DeclarativeBase` con atributos tipados `Mapped[T]`.", "Aísla la estructura de código de las peculiaridades del dialecto SQL subyacente."),
                ("02. Llaves Foráneas e Integridad Referencial", "Uso de `ForeignKey('tabla.id')` para vincular registros entre tablas relacionales.", "El motor SQL rechaza automáticamente la inserción de huérfanos o relaciones inexistentes."),
                ("03. Tipos de Relaciones (1:1, 1:N, N:M)", "Declaración explicita con `relationship()` e hiper-tablas intermedias de asociación para relaciones N:M.", "Permite navegar el grafo de objetos directamente en código: `usuario.pedidos`.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Mapeo de Clases a Tablas Físicas",
            "descripcion": "Metadatos del ORM y sincronización de estado:",
            "tarjetas": [
                ("Registro `MetaData`", "Contiene el catálogo dinámico de todas las tablas y restricciones registradas en la aplicación.", "Utilizado por el ORM para generar sentencias `CREATE TABLE` o scripts de migración."),
                ("Opciones Cascade (`cascade='all, delete-orphan'`)", "Define el comportamiento al eliminar un registro padre sobre sus entidades secundarias relacionadas.", "Garantiza limpieza automática de registros en cascada en la base de datos.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla en Modelado ORM",
            "items": [
                "Definir relaciones bidireccionales sin especificar `back_populates` causando desincronización de objetos en memoria.",
                "Omitir índices explícitos (`index=True`) en llaves foráneas y campos de búsqueda frecuente.",
                "Intentar mapear tablas N:M sin una tabla de asociación explicita con llaves compuestas."
            ]
        }
    },
    23: {
        "tema": "Operaciones CRUD Transaccionales y Async Sessions",
        "unidad": "Bloque 3: Persistencia Relacional, ORM y OWASP",
        "teoria_principal": {
            "titulo": "Sesiones Asíncronas y Patrón Unit of Work",
            "lead": "La sesión del ORM actúa como un espacio de trabajo (*Unit of Work*) que rastrea cambios sobre objetos antes de persistirlos.",
            "tarjetas": [
                ("01. Asincronía con `AsyncSession`", "Uso de `await session.execute()`, `await session.commit()` y `await session.refresh()`.", "Libera el hilo principal del evento web mientras la base de datos procesa la consulta."),
                ("02. Estados de Objetos en el ORM", "Un objeto atraviesa estados: Transient (nuevo), Pending (agregado), Persistent (guardado) y Detached (cerrado).", "El ORM solo emite sentencias SQL `UPDATE` sobre atributos que hayan sufrido modificaciones reales."),
                ("03. Ciclo de Vida por Petición HTTP", "La sesión se crea al recibir el Request y se cierra obligatoriamente al terminar mediante inyección de dependencias.", "Garantiza un aislamiento estricto de transacciones entre peticiones de distintos usuarios.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Identity Map y Cache de Sesión",
            "descripcion": "Seguimiento de unificación de objetos en memoria:",
            "tarjetas": [
                ("Patrón Identity Map", "Garantiza que dentro de la misma sesión, dos consultas al mismo ID retornen exactamente la misma instancia en RAM.", "Evita inconsistencias de estado si dos partes del código modifican la misma entidad."),
                ("Flush vs Commit", "`flush()` envía las sentencias SQL pendientes a la DB sin cerrar la transacción; `commit()` las consolida permanentemente.", "Permite obtener IDs autogenerados antes de confirmar la transacción final.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Operaciones CRUD",
            "items": [
                "Acceder a atributos con carga perezosa (*Lazy Loading*) fuera de la sesión asíncrona lanzando `MissingGreenlet` error.",
                "No ejecutar `await session.rollback()` tras una excepción dejando la sesión en estado corrupto.",
                "Olvidar llamar `await session.refresh(obj)` para obtener valores autogenerados por la base de datos (timestamps, IDs)."
            ]
        }
    },
    24: {
        "tema": "Migraciones de Base de Datos con Alembic / Phinx",
        "unidad": "Bloque 3: Persistencia Relacional, ORM y OWASP",
        "teoria_principal": {
            "titulo": "Control de Versiones de Esquema de Base de Datos",
            "lead": "Las migraciones permiten evolucionar la estructura de la base de datos mediante cambios incrementales, reversibles y auditables.",
            "tarjetas": [
                ("01. Problemática de Cambios Manuales", "Modificar tablas con SQL directo rompe la sincronización entre el código de producción y los entornos de desarrollo.", "Inviable en equipos distribuidos y sistemas de despliegue continuo (CD)."),
                ("02. Scripts de Migración (Upgrade / Downgrade)", "Cada revisión contiene dos funciones: `upgrade()` (aplica cambios) y `downgrade()` (los revierte).", "Permite avanzar o retroceder el esquema a cualquier punto de la historia del proyecto."),
                ("03. Autogeneración de Revision Script", "Alembic compara los modelos de SQLAlchemy contra la base de datos real y genera la migración automáticamente.", "Acelera el desarrollo reduciendo la escritura manual de DDL.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Tabla de Versiones `alembic_version`",
            "descripcion": "Rastreo de estado de la base de datos:",
            "tarjetas": [
                ("Tabla Centinela `alembic_version`", "Tabla especial en la DB que almacena una sola fila con el hash de la versión activa (`version_num`).", "Informa a Alembic qué revisiones faltan por aplicar durante el despliegue automático."),
                ("Integración con CI/CD", "Ejecución de `alembic upgrade head` en el pipeline de despliegue antes de reiniciar el servidor web.", "Asegura que las nuevas tablas existan antes de que el nuevo código reciba tráfico.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla en Migraciones",
            "items": [
                "Agregar columnas `NOT NULL` sin definir un valor por defecto (*default*) en tablas que ya contienen datos.",
                "Editar modelos sin generar el script de migración correspondiente desincronizando código y DB.",
                "Eliminar columnas en migraciones sin haber migrado previamente los datos existentes a una nueva estructura."
            ]
        }
    },
    25: {
        "tema": "Consultas Complejas, Joins y Carga Ansiosa (Eager Loading)",
        "unidad": "Bloque 3: Persistencia Relacional, ORM y OWASP",
        "teoria_principal": {
            "titulo": "Optimización de Consultas ORM y Problema N+1",
            "lead": "El uso ingenuo de relaciones en ORMs puede desencadenar cientos de consultas repetitivas degradando drásticamente el rendimiento.",
            "tarjetas": [
                ("01. El Problema del N+1", "Ocurre cuando se consulta 1 lista de N elementos y luego el ORM emite N consultas individuales para traer sus hijos.", "Convierte una operación de milisegundos en segundos de latencia de red."),
                ("02. Carga Ansiosa (`selectinload` / `joinedload`)", "Estrategias de precarga que traen el objeto y sus relaciones en 1 o 2 consultas SQL optimizadas.", "`selectinload` usa `WHERE id IN (...)`; `joinedload` realiza un `LEFT OUTER JOIN`."),
                ("03. Filtros, Agregaciones y Paginación", "Uso de `select()`, `where()`, `group_by()`, `func.count()`, `limit()` y `offset()`.", "Sustituye el procesamiento en RAM de Python/PHP por el motor optimizado de SQL.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Estrategias de Prefetching en Memoria",
            "descripcion": "Comparativa de rendimiento en consultas relacionales:",
            "tarjetas": [
                ("Diferencia entre Joined vs Selectin", "`joinedload` es ideal para relaciones 1:1 o M:1; `selectinload` es óptimo para relaciones 1:N y N:M.", "Evita la multiplicación cartesiana de filas en arreglos grandes."),
                ("Paginación Eficiente (`offset` / `limit`)", "Obligatoria en colecciones masivas para no cargar cientos de miles de registros en RAM.", "Reduce la huella de memoria del proceso del servidor.")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Consultas ORM",
            "items": [
                "Iterar sobre una colección de objetos sin usar `selectinload`, disparando el problema N+1.",
                "Cargar colecciones enteras con `.all()` sin paginar en endpoints públicos.",
                "Realizar filtrado de listas en memoria con Python (`[x for x in res if x.activo]`) en lugar de usar cláusulas `where()` en SQL."
            ]
        }
    },
    26: {
        "tema": "Transacciones ACID, Aislamiento y Rollback",
        "unidad": "Bloque 3: Persistencia Relacional, ORM y OWASP",
        "teoria_principal": {
            "titulo": "Garantías de Consistencia A.C.I.D. en la Base de Datos",
            "lead": "Las transacciones agrupan múltiples operaciones de escritura bajo una garantía de todo-o-nada.",
            "tarjetas": [
                ("01. Propiedades A.C.I.D.", "Atomicidad (todo o nada), Consistencia (respeta reglas), Aislamiento (concurrencia), Durabilidad (persistencia en disco).", "Garantía fundamental en sistemas bancarios, reservas y comercio electrónico."),
                ("02. Niveles de Aislamiento (Isolation Levels)", "Read Committed, Repeatable Read, Serializable.", "Controlan la visibilidad de cambios no confirmados entre consultas concurrentes."),
                ("03. Manejo Estricto de Rollback", "Si ocurre cualquier error dentro del bloque transaccional, se invoca `await session.rollback()`.", "Descarta todos los cambios pendientes devolviendo la base de datos a su estado consistente previo.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Manejador Transaccional Implícito",
            "descripcion": "Bloque `async with session.begin()`:",
            "tarjetas": [
                ("Gestión de Transacción Automática", "Abre la transacción al entrar; si el bloque concluye sin excepciones, emite `commit()`; si hay error, ejecuta `rollback()`.", "Elimina el código repetitivo de manejo manual de excepciones."),
                ("Bloqueos Pessimistic vs Optimistic Locking", "Bloqueos explícitos (`SELECT FOR UPDATE`) para prevenir condiciones de carrera en inventarios o saldos.", "Garantiza exclusión mutua durante la modificación concorriente.")
            ]
        },
        "casos_borde": {
            "titulo": "Puntos de Falla Transaccionales",
            "items": [
                "Condiciones de carrera (*Race Conditions*) por no usar transacciones o bloqueos al actualizar recursos escasos.",
                "Bloqueos mutuos (*Deadlocks*) causados por acceder a múltiples tablas en orden inverso en transacciones paralelas.",
                "Ignorar excepciones transaccionales y continuar ejecutando la lógica como si la escritura hubiese sido exitosa."
            ]
        }
    },
    27: {
        "tema": "Blindaje OWASP: Prevención Total de SQL Injection (SQLi)",
        "unidad": "Bloque 3: Persistencia Relacional, ORM y OWASP",
        "teoria_principal": {
            "titulo": "Inyección SQL (OWASP Top 10 A03) y Consultas Parametrizadas",
            "lead": "SQL Injection ocurre cuando entradas no confiables se concatenan directamente en cadenas de consulta SQL.",
            "tarjetas": [
                ("01. Mecánica del Ataque SQLi", "Un atacante ingresa `' OR '1'='1` alterando la lógica del parser SQL para saltarse la autenticación o extraer tablas enteras.", "Es una de las vulnerabilidades más destructivas en la historia de la web."),
                ("02. Consultas Parametrizadas (Prepared Statements)", "Separación física entre el código de la consulta y los datos de entrada.", "El motor SQL compila la plantilla primero; los datos se tratan estrictamente como valores literales, nunca como código ejecutable."),
                ("03. Protección Nativa del ORM", "Los ORMs como SQLAlchemy compilan todas las consultas utilizando sentencias preparadas por defecto.", "Neutralizan automáticamente los intentos de inyección SQL sin esfuerzo adicional del desarrollador.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Compilación de Sentencias Preparadas",
            "descripcion": "Diferencia entre concatenación frágil y parametrización:",
            "tarjetas": [
                ("Concatenación Vulnerable (Prohibida)", "`sql = 'SELECT * FROM users WHERE email = ' + input_usuario`.", "El texto del usuario altera el árbol sintáctico de la consulta SQL."),
                ("Parametrización Segura", "`sql = 'SELECT * FROM users WHERE email = :email'`, `params={'email': input_usuario}`.", "El motor trata `:email` como un contenedor aislado de datos de texto.")
            ]
        },
        "casos_borde": {
            "titulo": "Vulnerabilidades Frecuentes de SQLi",
            "items": [
                "Uso de SQL crudo con interpolación de cadenas `f'SELECT * FROM {tabla}'` o `text(...)` mal utilizado en ORMs.",
                "Concatenar nombres de columnas o tablas dinámicamente desde parámetros de la URL.",
                "Confiar en filtros de palabras clave manuales (`replace('UNION', '')`) en lugar de usar sentencias preparadas."
            ]
        }
    },
    28: {
        "tema": "Blindaje Web: Cross-Origin Resource Sharing (CORS)",
        "unidad": "Bloque 3: Persistencia Relacional, ORM y OWASP",
        "teoria_principal": {
            "titulo": "Política de Mismo Origen (SOP) y Configuración CORS",
            "lead": "CORS es un mecanismo de seguridad de los navegadores para restringir solicitudes HTTP originadas desde un dominio distinto.",
            "tarjetas": [
                ("01. Same-Origin Policy (SOP)", "Los navegadores bloquean por defecto que un script de `app.com` lea respuestas de `api.com` a menos que la API lo autorice.", "Protege a los usuarios de que sitios maliciosos consuman sus APIs privadas en segundo plano."),
                ("02. Encabezados CORS (`Access-Control-Allow-*`)", "Respuestas enviadas por el servidor indicando dominios permitidos (`Origin`), métodos (`Methods`) y encabezados (`Headers`).", "Permite que la Single Page Application (SPA) se comunique legítimamente con el backend."),
                ("03. Peticiones Pre-flight (OPTIONS)", "Petición preliminar automática del navegador para verificar si la operación real es segura antes de enviarla.", "El servidor debe responder con HTTP 200/204 y los encabezados CORS correspondientes.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Middleware CORS en Servidor Web",
            "descripcion": "Inyección centralizada de encabezados de origen:",
            "tarjetas": [
                ("Configuración con Lista Blanca", "`CORSMiddleware(allow_origins=['https://midominio.com'], allow_credentials=True)`.", "Define explícitamente qué orígenes tienen acceso a los recursos."),
                ("Peligro del Comodín `allow_origins=['*']`", "Permite que cualquier sitio web del mundo consuma la API.", "Incompatible y peligroso cuando se combina con envío de credenciales (`allow_credentials=True`).")
            ]
        },
        "casos_borde": {
            "titulo": "Antipatrones en Configuración CORS",
            "items": [
                "Usar `allow_origins=['*']` en APIs de producción que manejan autenticación con cookies o tokens de usuario.",
                "Olvidar incluir encabezados personalizados (ej. `Authorization`, `X-Custom-Header`) en `allow_headers` provocando bloqueos en el cliente.",
                "Configurar CORS en el servidor web sin manejar correctamente las peticiones preliminares `OPTIONS`."
            ]
        }
    },
    29: {
        "tema": "Protección Anti-CSRF y Cookies HttpOnly / SameSite",
        "unidad": "Bloque 3: Persistencia Relacional, ORM y OWASP",
        "teoria_principal": {
            "titulo": "Falsificación de Peticiones (CSRF) y Seguridad de Cookies",
            "lead": "CSRF fuerza al navegador de una víctima autenticada a enviar peticiones no deseadas a una aplicación web confiable.",
            "tarjetas": [
                ("01. Mecánica del Ataque CSRF", "Si la autenticación usa Cookies automáticas, un sitio malicioso puede incluir un formulario oculto hacia `banco.com/transferir`.", "El navegador adjunta la Cookie de sesión automáticamente ejecutando la transacción sin el conocimiento del usuario."),
                ("02. Flags de Seguridad en Cookies", "`HttpOnly` (impide acceso desde JavaScript/XSS), `Secure` (exige HTTPS), `SameSite=Lax/Strict` (restringe envío trans-sitio).", "`SameSite=Lax` es la defensa moderna más efectiva contra ataques CSRF."),
                ("03. Tokens Anti-CSRF (Pattern Synchronizer Token)", "Token aleatorio único adjunto a la sesión que debe enviarse en el cuerpo/encabezado de cada petición mutable.", "Invalida peticiones originadas desde sitios externos que no poseen el token.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Atributos de Cookies de Sesión Seguras",
            "descripcion": "Configuración del encabezado `Set-Cookie`:",
            "tarjetas": [
                ("Set-Cookie Header Estandarizado", "`Set-Cookie: session=xyz; Secure; HttpOnly; SameSite=Lax; Path=/; Max-Age=3600`.", "Blindaje multicapa que protege la sesión tanto en tránsito como en reposo en el cliente."),
                ("Tokens Stateless vs CSRF", "Las APIs que leen el JWT exclusivamente desde el encabezado `Authorization: Bearer` son inmunes a CSRF de forma natural.", "El navegador no adjunta encabezados Authorization automáticamente.")
            ]
        },
        "casos_borde": {
            "titulo": "Vulnerabilidades de Sesión y Cookies",
            "items": [
                "Omitir el flag `HttpOnly` permitiendo que un script XSS robe el identificador de sesión mediante `document.cookie`.",
                "Usar `SameSite=None` sin configurar la bandera `Secure` (rechazado por los navegadores modernos).",
                "Confiar únicamente en el encabezado `Referer` para validar el origen de la petición en lugar de tokens Anti-CSRF o cookies SameSite."
            ]
        }
    },
    30: {
        "tema": "Hito 3: API Persistente con ORM, Migraciones y Blindaje OWASP",
        "unidad": "Bloque 3: Persistencia Relacional, ORM y OWASP",
        "teoria_principal": {
            "titulo": "Integración del Tercer Hito: Persistencia y Seguridad Total",
            "lead": "Culminación del Bloque 3. La API cuenta con base de datos relacional, modelos ORM, migraciones de esquemas y protección OWASP.",
            "tarjetas": [
                ("01. Capa de Datos Transaccional Completa", "API que realiza operaciones CRUD sobre PostgreSQL/SQLite utilizando SQLAlchemy asíncrono, migraciones Alembic y repositorios desacoplados.", "Soporta consultas relacionales complejas sin incurrir en el problema N+1."),
                ("02. Blindaje OWASP Verificado", "Protección completa contra SQLi (consultas parametrizadas), CORS configurado con listas blancas, cookies `HttpOnly; SameSite` y sanitización.", "Garantiza resiliencia técnica ante intentos de intrusión y ataques de inyección."),
                ("03. Entrega de Hito 3 (Git Tag)", "Etiquetado formal de versión en el repositorio de GitHub del estudiante: `git tag v0.3-hito3`.", "Representa el 25% del Proyecto Integrador Semestral.")
            ]
        },
        "arquitectura_memoria": {
            "titulo": "Auditoría de Integridad de Persistencia y Seguridad",
            "descripcion": "Evaluación con el Test Harness de Base de Datos y Pen-Testing:",
            "tarjetas": [
                ("Pruebas de Estrés Transaccional y Penetración", "Ejecución automatizada de payloads SQLi, pruebas de rollbacks ante fallos, migraciones `upgrade/downgrade` y carga de datos.", "Certifica que la base de datos se mantenga consistente y la API inmune a exploits."),
                ("Verificación de Conexiones y Migraciones", "Asegura que las migraciones se apliquen limpiamente con `alembic upgrade head` sin pérdida de información.", "Garantiza un entorno listo para el despliegue final en la nube.")
            ]
        },
        "casos_borde": {
            "titulo": "Criterios de Rechazo del Hito 3",
            "items": [
                "API vulnerable a SQL Injection o que utilice consultas crudas concatenadas con cadenas.",
                "Fallas de consistencia transaccional (datos huérfanos o commit parcial tras una excepción).",
                "Incapacidad de ejecutar las migraciones de base de datos desde cero en una instancia limpia."
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
      <p class="lead">Sesión {n_str} del curso. Persistencia relacional, ORM asíncrono, control de migraciones y blindaje OWASP con la Tríada Metodológica.</p>
      <div class="grid-3">
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span style="color: var(--accent);">01. El Artesano</span><span class="expand-hint">[+]</span></div>
          <p>Codificación manual sin IA para comprender consultas SQL directas, transacciones y esquemas relacionales.</p>
          <div class="card-details">Desarrolla la intuición técnica de modelos relacionales, migraciones y prevención de vulnerabilidades.</div>
        </div>
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span style="color: var(--accent-silver);">02. El Científico</span><span class="expand-hint">[+]</span></div>
          <p>Especificación C-R-E-O para modelos SQLAlchemy/Doctrine, migraciones Alembic y protección Anti-SQLi.</p>
          <div class="card-details">Define contratos formales de datos, relaciones de entidad y políticas de seguridad CORS/CSRF.</div>
        </div>
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span style="color: var(--accent-green);">03. El Auditor</span><span class="expand-hint">[+]</span></div>
          <p>Test Harness automatizado con pruebas de penetración SQLi, auditoría transaccional y rollbacks.</p>
          <div class="card-details">Somete la capa de datos a estrés de concurrencia y registra la bitácora en GitHub.</div>
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
        <strong>Invariante de Datos:</strong> Toda operación de escritura debe preservar la integridad relacional y ejecutarse bajo garantías A.C.I.D.
      </div>
    </section>

    <section class="slide">
      <h2>Arquitectura de Persistencia y Seguridad: {am["titulo"]}</h2>
      <p class="lead">{am["descripcion"]}</p>
      <div class="grid-2">
        {cards_s3}
      </div>
    </section>

    <section class="slide">
      <h2>{cb["titulo"]}</h2>
      <p class="lead">Puntos críticos de falla y vulnerabilidades de seguridad a prevenir en la implementación y auditar en la IA:</p>
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
            <li><strong>00–20 min:</strong> Fundamento teórico y arquitectura de datos.</li>
            <li><strong>20–35 min:</strong> Fase 1: El Artesano (Código manual sin IA).</li>
            <li><strong>35–45 min:</strong> Fase 2: El Científico (Prompt C-R-E-O).</li>
            <li><strong>45–55 min:</strong> Fase 3: El Auditor (Test Harness de DB/OWASP).</li>
            <li><strong>55–60 min:</strong> Sincronización y commit en GitHub.</li>
          </ul>
          <div class="card-details">Verifica que las migraciones y pruebas SQL pass al 100% antes de subir tu bitácora.</div>
        </div>
        <div class="card" onclick="toggleCard(this)">
          <div class="card-header"><span>Evidencia Evaluada</span><span class="expand-hint">[+]</span></div>
          <p>Tu archivo <code>auditorias/auditoria_sesion{n_str}.md</code> debe contener la matriz C-R-E-O y el reporte crítico.</p>
          <div class="card-details">La entrega de la Sesión 30 concluye formalmente el Hito 3 del Proyecto Integrador.</div>
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
    print("🚀 Compilando presentaciones enriquecidas de Desarrollo Web (Bloque 3: Sesiones 21 a 30)...")
    os.makedirs("presentaciones", exist_ok=True)
    
    for num, data in TEORIA_WEB_BLOQUE_3.items():
        n_str = f"{num:02d}"
        out_path = f"presentaciones/sesion{n_str}.html"
        html_content = compilar_presentacion_5_slides_web(num, data)
        
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"  -> Generada Sesión {n_str}: {data['tema']} (5 slides)")
            
    print("✅ Bloque 3 de presentaciones de Desarrollo Web actualizado exitosamente.")

if __name__ == "__main__":
    main()
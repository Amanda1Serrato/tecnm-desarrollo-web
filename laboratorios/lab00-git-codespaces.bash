# 1. Crear el archivo de presentación de Sesión 02
cat << 'EOF' > presentaciones/sesion02.html
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Sesión 02: Gestión en GitHub Web y Métodos HTTP (GET, POST, PUT, DELETE) | Desarrollo de Aplicaciones Web</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/theme/black.css">
</head>
<body>
  <div class="reveal">
    <div class="slides">
      <section>
        <h2>Sesión 02</h2>
        <h3>Gestión en GitHub Web, Codespaces y Métodos HTTP</h3>
        <p><strong>Desarrollo de Aplicaciones Web (AEB-1055)</strong></p>
        <p>Prof. Iván Márquez Larios</p>
      </section>

      <section>
        <h3>El Taller en la Nube: GitHub Codespaces</h3>
        <ul>
          <li>Entorno Linux (Ubuntu/Debian) completo en tu navegador.</li>
          <li>Sin problemas de instalación local: Python, Git y curl preinstalados.</li>
          <li><strong>Regla de oro:</strong> Tu trabajo solo existe si está sincronizado en GitHub.</li>
        </ul>
      </section>

      <section>
        <h3>El Ciclo de Vida en Git</h3>
        <ol>
          <li><code>git status</code> — Inspeccionar archivos modificados.</li>
          <li><code>git add &lt;archivo&gt;</code> — Preparar cambios en el área de montaje.</li>
          <li><code>git commit -m "mensaje"</code> — Sellar y documentar el avance.</li>
          <li><code>git push origin main</code> — Sincronizar con el repositorio central.</li>
        </ol>
      </section>

      <section>
        <h3>Fundamento HTTP: Métodos Principales</h3>
        <ul>
          <li><strong>GET:</strong> Solicitar y recuperar información (idempotente y seguro).</li>
          <li><strong>POST:</strong> Enviar datos para crear un nuevo recurso en el servidor.</li>
          <li><strong>PUT / PATCH:</strong> Actualizar un recurso existente de forma total o parcial.</li>
          <li><strong>DELETE:</strong> Eliminar un recurso del servidor.</li>
        </ol>
      </section>

      <section>
        <h3>¡Manos al Código!</h3>
        <p>Ve a la guía de <code>laboratorios/lab01-git-codespaces.md</code> para ejecutar tu primer script, verificarlo con peticiones y completar tu primer push en verde.</p>
      </section>
    </div>
  </div>
  <script src="https://cdn.jsdelivr.net/npm/reveal.js@4.5.0/dist/reveal.js"></script>
  <script>Reveal.initialize();</script>
</body>
</html>
EOF

# 2. Crear la carpeta y guía del laboratorio
mkdir -p laboratorios
cat << 'EOF' > laboratorios/lab01-git-codespaces.md
# Laboratorio 01: Configuración de Entorno, Primer Script y Ciclo Git

**Asignatura:** Desarrollo de Aplicaciones Web (AEB-1055)  
**Profesor:** M. en C. Iván José Márquez Larios

---

## Objetivo
Configurar el entorno en GitHub Codespaces, ejecutar un script en Python que simule un despachador básico de métodos HTTP, realizar modificaciones en el código y completar el ciclo de confirmación y sincronización en Git (`add`, `commit`, `push`).

---

## Instrucciones Paso a Paso

### Paso 1: Crear el script base
Crea un archivo llamado `app_http_test.py` con el siguiente contenido:

```python
import sys

def procesar_metodo(metodo: str):
    metodos_validos = {
        "GET": "200 OK - Lectura de recurso exitosa",
        "POST": "201 Created - Nuevo recurso creado",
        "PUT": "200 OK - Recurso actualizado",
        "DELETE": "204 No Content - Recurso eliminado"
    }
    return metodos_validos.get(metodo.upper(), "405 Method Not Allowed")

if __name__ == "__main__":
    metodo_prueba = sys.argv[1] if len(sys.argv) > 1 else "GET"
    print(f"[Simulador HTTP] Petición recibida: {metodo_prueba}")
    print(f"Respuesta del Servidor: {procesar_metodo(metodo_prueba)}")

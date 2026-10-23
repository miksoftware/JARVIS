# MIK-JARVIS 🤖

<div align="center">
  <h3><i>Asistente Inteligente de IA — Desarrollado por MIK Software</i></h3>
  <p>
    <b>Solución integral de IA conectada a la infraestructura y modelos de MIK Software.</b>
  </p>
</div>

---

## 🚀 Descripción del Proyecto

**MIK-JARVIS** es la plataforma modular de Inteligencia Artificial para **MIK Software**. Proporciona capacidades avanzadas de asistencia virtual, ejecución de código, investigación profunda, conexión a fuentes de datos y agentes autónomos, tanto a través de una interfaz gráfica web moderna como por terminal y API REST OpenAI-compatible.

---

## ⚡ Conexión a la API de IA

MIK-JARVIS está integrado de forma predeterminada con el enrutador de IA de **MIK Software (FreeLLMAPI)**:

* **Endpoint Base**: `https://ai.miksoftwarecol.com/v1`
* **Motor por Defecto**: `freellmapi`
* **Modelo por Defecto**: `auto` (enrutamiento dinámico automático entre más de 280 modelos de IA disponibles)
* **Configuración de credenciales**: Almacenada en `.env` y `~/.openjarvis/cloud-keys.env`.

---

## 💻 Formas de Ejecución

### Opción 1: Interfaz Gráfica Web (Recomendado)
* **Doble clic en**: `iniciar-gui.bat`
* **O por terminal**:
  ```powershell
  uv run mik-jarvis gui
  ```
  *Inicia el backend y abre automáticamente el navegador en la interfaz de chat interactiva.*

### Opción 2: Servidor API y Web
* **Doble clic en**: `iniciar-servidor.bat`
* **O por terminal**:
  ```powershell
  uv run mik-jarvis serve --host 127.0.0.1 --port 8000
  ```
  *Disponible en [http://localhost:8000](http://localhost:8000).*

### Opción 3: Chat Interactivo en la Terminal (CLI)
* **Doble clic en**: `iniciar-chat.bat`
* **O por terminal**:
  ```powershell
  uv run mik-jarvis chat
  ```

### Opción 4: Pregunta Directa por Terminal
```powershell
uv run mik-jarvis ask "¿Qué servicios ofrece MIK Software?"
```

Para consultar usando un modelo específico de tu catálogo:
```powershell
uv run mik-jarvis ask -m claude-sonnet-4-5 "Analiza esta lógica de negocio"
uv run mik-jarvis ask -m gemini-3.8-flash "Explica qué es una API REST"
```

---

## 🩺 Diagnóstico y Verificación

Para verificar la salud del sistema y los motores de IA conectados:
```powershell
uv run mik-jarvis doctor
```

---

## 📁 Estructura del Proyecto

* `frontend/`: Interfaz web moderna (React 19 + TypeScript + Vite + TailwindCSS).
* `src/openjarvis/`: Núcleo de agentes, herramientas, servidores y motores de inferencia.
* `configs/`: Plantillas y archivos de configuración.
* `iniciar-gui.bat`: Script de inicio rápido de la interfaz gráfica.
* `iniciar-servidor.bat`: Script de inicio rápido del servidor API.
* `iniciar-chat.bat`: Script de chat rápido en terminal.
* `.env`: Variables de entorno y configuración de conexión con FreeLLMAPI.

---

## 🏢 Propiedad y Créditos

Proyecto adaptado, configurado y mantenido por **MIK Software** ([miksoftwarecol.com](https://ai.miksoftwarecol.com)).

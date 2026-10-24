# MIK-JARVIS 🤖

<div align="center">
  <h3><i>Asistente Inteligente de IA y Copiloto Holográfico — MIK Software</i></h3>
  <p>
    <b>Plataforma integral de IA conectada a la infraestructura y modelos de alto rendimiento de MIK Software.</b>
  </p>
  <p>
    <img src="https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue?logo=python" alt="Python Version" />
    <img src="https://img.shields.io/badge/FastAPI-0.110+-009688?logo=fastapi" alt="FastAPI" />
    <img src="https://img.shields.io/badge/License-Apache%202.0-green.svg" alt="License" />
    <img src="https://img.shields.io/badge/Security-Protected%20Secrets-brightgreen" alt="Security" />
  </p>
</div>

---

## 🚀 Descripción del Proyecto

**MIK-JARVIS** es un ecosistema avanzado y modular de Inteligencia Artificial desarrollado para **MIK Software**. Proporciona capacidades completas de asistencia virtual, ejecución de tareas, procesamiento de voz en tiempo real, chat interactivo y modos holográficos inspirados en la interfaz de **J.A.R.V.I.S. (Iron Man)**, compatible tanto con terminales como con navegadores web e interfaces gráficas.

---

## 🔒 Seguridad, Endpoint de IA y Gestión de Secretos

### ¿Cómo funciona la conexión con FreeLLMAPI?
El sistema se conecta de forma nativa al enrutador de IA de **MIK Software (FreeLLMAPI)**:
* **Endpoint Base**: `https://ai.miksoftwarecol.com/v1`
* **Modelos Disponibles**: Catálogo multi-modelo con enrutamiento inteligente (`auto`, `gemini-3.5-flash-lite`, `gemma-4-31b-it`, `claude-sonnet-4-5`, etc.).

> [!NOTE]
> **Sobre la seguridad del Endpoint:**
> El endpoint `https://ai.miksoftwarecol.com` es un servicio protegido que **requiere autenticación estricta mediante API Key**. Nadie puede interactuar con el servidor ni consumir recursos sin una clave válida.
> 
> **Tus credenciales y claves privadas NUNCA deben subirse al repositorio:**
> 1. Todas las claves se almacenan exclusivamente en el archivo local `.env` (el cual está listado y protegido dentro de `.gitignore`).
> 2. Los archivos de código fuente (`servidor_ironman.py`, `modo_ironman.py`, etc.) leen las credenciales mediante variables de entorno y no contienen claves privadas quemadas en el código.
> 3. En el repositorio solo se comparte la plantilla pública `.env.example` con valores de ejemplo genéricos.

---

## 📋 Requisitos Previos

Antes de instalar, asegúrate de contar con lo siguiente en tu sistema:

1. **Python**: Versión `3.10`, `3.11`, `3.12` o `3.13` (64 bits).
2. **Administrador de paquetes `uv`** (Altamente recomendado por su velocidad instantánea):
   ```powershell
   # Instalación rápida de uv en Windows (PowerShell):
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```
   *(También puedes usar `pip` si lo prefieres).*
3. **Node.js 22 o superior** *(Únicamente necesario si deseas compilar y ejecutar la interfaz web de React mediante `iniciar-gui.bat`)*.
4. **Micrófono y Altavoces / Auriculares**: Para interactuar por voz en el Modo Iron Man.

---

## 🛠️ Guía de Instalación Paso a Paso

Sigue estos pasos detallados para poner en marcha MIK-JARVIS desde cero:

### 1. Clonar o descargar el repositorio
Abre tu terminal en la carpeta de proyectos:
```powershell
git clone <URL_DE_TU_REPOSITORIO> JARVIS
cd JARVIS
```

### 2. Configurar las Variables de Entorno (`.env`)
Crea tu archivo `.env` a partir de la plantilla `.env.example`:
```powershell
# En Windows (PowerShell):
Copy-Item .env.example .env

# O en símbolo del sistema (CMD):
copy .env.example .env
```

Abre el archivo `.env` recién creado con tu editor de texto favorito y coloca tu clave de API:
```env
# Enrutador / Servidor Remoto de IA (FreeLLMAPI - MIK Software)
FREELLMAPI_HOST=https://ai.miksoftwarecol.com
FREELLMAPI_API_KEY=tu_clave_secreta_freellmapi_aqui

# Fallback OpenAI
OPENAI_BASE_URL=https://ai.miksoftwarecol.com/v1
OPENAI_API_KEY=tu_clave_secreta_freellmapi_aqui

# Servidor OpenJarvis Estándar
OPENJARVIS_HOST=127.0.0.1
OPENJARVIS_PORT=8000

# Puerto de la Interfaz Holográfica Iron Man
JARVIS_HUD_PORT=5000

# (Opcional) Voz ultrarrealista con ElevenLabs (Sergio):
ELEVENLABS_API_KEY=
ELEVENLABS_VOICE_ID=SHkfxEDcLXK31yPii5xM
```

> [!TIP]
> Si no cuentas con una clave de ElevenLabs, déjala vacía. El sistema activará automáticamente el sintetizador de voz local de Windows (SAPI5 en español) sin ningún costo adicional.

### 3. Instalar Dependencias del Proyecto

Utilizando `uv` (Recomendado):
```powershell
uv sync --extra desktop
```
*(Este comando creará automáticamente el entorno virtual e instalará todas las dependencias necesarias para los módulos de voz, servidor web FastAPI, rich terminal, Whisper y audio).*

Si utilizas `pip`:
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -e .[desktop]
```

---

## ⚡ Formas de Ejecución e Iniciadores (.bat)

El proyecto cuenta con **5 scripts ejecutables directos (`.bat`)** para iniciar cualquier modo con solo dar doble clic:

```
JARVIS/
├── iniciar-modo-ironman.bat          # 🌟 Interfaz Holográfica Arc Reactor (Web HUD)
├── iniciar-modo-ironman-consola.bat  # 🎙️ Modo Asistente de Voz por Consola (Wake Word)
├── iniciar-gui.bat                   # 💻 Interfaz Gráfica Web React OpenJarvis
├── iniciar-servidor.bat              # ⚙️ Servidor API Backend REST (Puerto 8000)
└── iniciar-chat.bat                  # 💬 Chat interactivo en Terminal CLI
```

### 1. 🌟 Interfaz Holográfica Arc Reactor (Recomendado)
* **Doble clic en**: `iniciar-modo-ironman.bat`
* **O por terminal**:
  ```powershell
  uv run python servidor_ironman.py
  ```
* **¿Qué hace?**:
  - Levanta un servidor local en `http://localhost:5000` y abre automáticamente tu navegador.
  - Ofrece una interfaz animada futurista de Iron Man con:
    - **Reactor Arc central** con visualizador de pulsos de energía y estados dinámicos (Escuchando, Procesando, Hablando).
    - **Reconocimiento de voz por navegador**: Modos *Push-to-Talk* (mantener pulsado espacio o clic en el reactor) y *Modo Manos Libres*.
    - **Visualizador holográfico de frecuencias de audio (FFT Spectrum)** en tiempo real.
    - **Panel de telemetría**: Monitoreo de CPU, RAM, latencia y reloj cibernético.
    - **Historial conversacional interactivo**: Cajón deslizable con memoria de turnos.
    - **Configuración de ElevenLabs integrada**: Permite ingresar y probar voces ultrarrealistas directamente desde la interfaz.

---

### 2. 🎙️ Modo Asistente de Voz por Consola
* **Doble clic en**: `iniciar-modo-ironman-consola.bat`
* **O por terminal**:
  ```powershell
  uv run python modo_ironman.py
  ```
* **¿Qué hace?**:
  - Inicia el asistente de voz autónomo con auto-calibración acústica en tiempo real adaptada al ruido ambiente de tu habitación.
  - **Modos de escucha**:
    - **Modo Libre**: Habla con total naturalidad; el sistema detecta tus frases automáticamente.
    - **Modo Centinela**: Permanece en silencio esperando palabras clave como *"Jarvis"*, *"Hola Jarvis"* u *"Oye Jarvis"*.
  - **VU-Metro interactivo**: Dibuja el nivel acústico y la energía RMS en vivo en la consola.
  - **Atajos en teclado**:
    - `[M]`: Alternar entre Modo Libre y Modo Centinela.
    - `[Espacio]`: Forzar turno de escucha inmediata.
    - `[+]` / `[-]`: Ajustar la sensibilidad del micrófono en vivo.
    - `[Q]`: Salir del asistente.

---

### 3. 💻 Interfaz Gráfica Web OpenJarvis (React)
* **Doble clic en**: `iniciar-gui.bat`
* **O por terminal**:
  ```powershell
  uv run mik-jarvis gui
  ```
* **¿Qué hace?**:
  - Compila y lanza la interfaz web moderna construida en React 19 + TypeScript + Vite + TailwindCSS.
  - Conecta automáticamente el frontend con el backend API.

---

### 4. 💬 Chat Rápido en Terminal (CLI)
* **Doble clic en**: `iniciar-chat.bat`
* **O por terminal**:
  ```powershell
  uv run mik-jarvis chat
  ```
* **¿Qué hace?**:
  - Inicia una sesión conversacional interactiva directamente en la consola con renderizado en Markdown y colores Rich.

---

### 5. ⚙️ Servidor API Backend REST (OpenAI-Compatible)
* **Doble clic en**: `iniciar-servidor.bat`
* **O por terminal**:
  ```powershell
  uv run mik-jarvis serve --host 127.0.0.1 --port 8000
  ```
* **¿Qué hace?**:
  - Expone los endpoints compatibles con el estándar de OpenAI en [http://localhost:8000](http://localhost:8000) para conectar extensiones, clientes de chat externos, SDKs o bots.

---

## 🔍 Comandos Adicionales por Terminal

### Pregunta Rápida (One-shot)
```powershell
uv run mik-jarvis ask "¿Qué servicios ofrece MIK Software?"
```

### Consultar con un Modelo Específico
```powershell
uv run mik-jarvis ask -m claude-sonnet-4-5 "Analiza esta arquitectura de software"
uv run mik-jarvis ask -m gemini-3.5-flash-lite "Genera un script en Python"
```

### Diagnóstico de Motores y Entorno (Doctor)
```powershell
uv run mik-jarvis doctor
```

---

## 📁 Estructura del Repositorio

```
JARVIS/
├── ironman_hud/                  # Aplicación de Interfaz Holográfica Arc Reactor
│   └── index.html               # Canvas animado, Web Audio API y HUD futurista
├── servidor_ironman.py          # Servidor FastAPI para el HUD Holográfico (Puerto 5000)
├── modo_ironman.py              # Asistente de voz por consola (Whisper + SoundDevice + VU-metro)
├── frontend/                    # Aplicación web completa en React 19 + TypeScript + Vite
├── src/openjarvis/              # Núcleo modular: motores, agentes, herramientas y CLI
├── configs/                     # Plantillas de configuración del sistema
├── iniciar-modo-ironman.bat     # Lanzador: HUD Holográfico
├── iniciar-modo-ironman-consola.bat # Lanzador: Modo Consola por Voz
├── iniciar-gui.bat              # Lanzador: GUI Web React
├── iniciar-servidor.bat         # Lanzador: Servidor REST API
├── iniciar-chat.bat             # Lanzador: Chat Terminal
├── .env.example                 # Plantilla pública y segura de configuración
├── .gitignore                   # Protección estricta contra subida de credenciales y archivos locales
└── pyproject.toml               # Especificación de dependencias del proyecto
```

---

## 🛡️ Lista de Verificación Antes de Subir al Repositorio

Para garantizar que **no se filtren credenciales o secretos** a GitHub/GitLab:

1. ✅ **Verifica que tu archivo `.env` exista localmente pero NO esté en seguimiento:**
   - `.gitignore` ya contiene la regla `.env` y `.env.*`.
2. ✅ **No coloques claves privadas directamente en archivos `.py`, `.js` o `.bat`.**
   - Siempre utiliza `os.environ.get("NOMBRE_VARIABLE")`.
3. ✅ **Plantilla `.env.example` limpia:**
   - Solo debe contener cadenas de marcador de posición (`tu_clave_freellmapi_aqui`).
4. ✅ **El endpoint `https://ai.miksoftwarecol.com` es seguro de compartir:**
   - Al requerir autenticación obligatoria por API Key, nadie puede utilizarlo sin su propia clave autorizada.

---

## 🏢 Propiedad y Créditos

Proyecto adaptado, configurado y mantenido por **MIK Software** ([miksoftwarecol.com](https://ai.miksoftwarecol.com)).
Licencia bajo términos **Apache 2.0**.

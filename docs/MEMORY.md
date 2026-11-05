# Memoria Persistente del Sistema — MIK-JARVIS

## 🛠️ Stack Tecnológico
- **Lenguajes**: Python (3.10 - 3.13), TypeScript, Rust (PyO3), HTML5/CSS3/Canvas WebGL.
- **Backend**: FastAPI, Uvicorn, HTTPX, Pydantic, Rich Terminal UI.
- **Audio & Voz**: Faster-Whisper (ASR int8 en CPU/CUDA), SoundDevice, PyTTSx3 (SAPI5 local en español), ElevenLabs (Voz de estudio: Sergio `SHkfxEDcLXK31yPii5xM`).
- **Frontend**: React 19, Vite, TailwindCSS, Base UI, Motion, Lucide Icons.
- **Desktop**: Tauri 2 (Rust bridge multiplataforma).
- **Inferencia de IA**: Enrutador remoto FreeLLMAPI de MIK Software (`https://ai.miksoftwarecol.com/v1`).

## 🏛️ Arquitectura y Módulos Principales
- `ironman_hud/`: Interfaz holográfica web animada inspirada en Arc Reactor (Iron Man), con analizador de espectro de audio FFT, Web Audio API y modos Push-to-Talk y Manos Libres.
- `servidor_ironman.py`: Servidor API FastAPI (puerto 5000) que sirve el HUD holográfico y procesa peticiones de chat y TTS conectando con FreeLLMAPI y ElevenLabs.
- `modo_ironman.py`: Copiloto conversacional por terminal con Whisper local, auto-calibración acústica de sala y visualización de volumen mediante VU-Metro dinámico.
- `src/openjarvis/`: Núcleo modular del asistente que gestiona motores de inferencia, herramientas (MCP), agentes, canales y CLI (`mik-jarvis`).
- `frontend/`: Interfaz web moderna con dashboard de telemetría, gestión de conversaciones y panel de configuración.
- `desktop/` y `frontend/src-tauri/`: Empaquetado nativo de escritorio para Windows, macOS y Linux.

## 🧠 Modelos y Almacenamiento
- **Proveedor IA**: FreeLLMAPI de MIK Software (`https://ai.miksoftwarecol.com`).
- **Modelos Principales**: `gemini-3.5-flash-lite`, `gemma-4-31b-it`, `claude-sonnet-4-5`, `auto`.
- **Persistencia**: Base de datos SQLite local para memoria persistente multi-sesión (`~/.openjarvis/memory.db`) y almacenamiento local en navegador (`localStorage`).

## 📋 Reglas de Negocio e Identidad
- **Titularidad y Marca**: Todo el ecosistema pertenece y está firmado exclusivamente bajo la marca **MIK Software** y el nombre del proyecto **MIK-JARVIS**.
- **Gestión de Secretos**: Ninguna credencial ni clave de API (`FREELLMAPI_API_KEY`, `ELEVENLABS_API_KEY`) se almacena directamente en el código; se consumen de forma segura desde el archivo `.env` local protegido por `.gitignore`.
- **Personalidad del Asistente**: Tono cercano, proactivo, inteligente y elocuente al estilo del copiloto de Iron Man, optimizado para interacción por voz en español y respuestas dinámicas.

## 📅 Changelog
- **2026-11-05**: Estandarización y auditoría de marca bajo MIK Software / MIK-JARVIS en LICENSE, pyproject.toml, .env.example, README.md, frontend (package.json, tauri.conf.json, Cargo.toml, vistas UI), servidor FastAPI y documentación base.


"""
MIK-JARVIS — Servidor Backend para Interfaz Holográfica Iron Man
Desarrollado para MIK Software (https://ai.miksoftwarecol.com)

Conecta la interfaz web futurista (Arc Reactor HUD) con:
1. FreeLLMAPI (ai.miksoftwarecol.com) para razonamiento y respuestas inteligentes.
2. ElevenLabs (Voz Sergio: SHkfxEDcLXK31yPii5xM) para síntesis de audio de calidad estudio.
3. Servidor local FastAPI en http://localhost:5000 con apertura automática del navegador.
"""

from __future__ import annotations

import os
import sys
import threading
import time
import webbrowser
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from rich.console import Console
from rich.panel import Panel

# Cargar .env
def load_env_file(filepath: str = ".env") -> None:
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k not in os.environ:
                        os.environ[k] = v

load_env_file()

API_BASE_URL = os.environ.get("FREELLMAPI_HOST", "https://ai.miksoftwarecol.com").rstrip("/")
API_KEY = os.environ.get("FREELLMAPI_API_KEY", "").strip()
MODEL = os.environ.get("OPENJARVIS_MODEL", "auto")

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "").strip()
ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "SHkfxEDcLXK31yPii5xM").strip()

PORT = int(os.environ.get("JARVIS_HUD_PORT", "5000"))
HUD_DIR = Path(__file__).resolve().parent / "ironman_hud"

console = Console()
app = FastAPI(title="MIK-JARVIS Iron Man Interface Server")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    prompt: str
    history: list[dict[str, str]] = []


class TTSRequest(BaseModel):
    text: str
    api_key: str = ""
    voice_id: str = ""


SYSTEM_PROMPT = (
    "Eres MIK-JARVIS, la avanzada inteligencia artificial conversacional de MIK Software (https://ai.miksoftwarecol.com), "
    "diseñada como copiloto personal al estilo de J.A.R.V.I.S. de Iron Man. "
    "Tu personalidad es sumamente inteligente, cercana, carismática, elocuente y proactiva. "
    "Hablas en un español neutral y fluido. "
    "DIRECTRICES CONVERSACIONALES OBLIGATORIAS: "
    "1. Mantén siempre viva y activa la conversación. NUNCA respondas con una sola frase seca como 'Es siempre un honor servirle'. "
    "2. Si el usuario te saluda, salúdalo con empatía y calidez, y pregúntale en qué pueden colaborar hoy (ej: programar, resolver dudas técnicas, revisar código o charlar). "
    "3. Si te hace preguntas o consultas, responde de forma clara, amena y precisa (unas 2 a 4 oraciones bien hiladas, optimizadas para ser escuchadas). "
    "4. Al final de tu respuesta, cuando sea natural, remata con una pregunta breve o una sugerencia para seguir la charla."
)


# Modelos ordenados por velocidad y estabilidad comprobada en FreeLLMAPI
FALLBACK_MODELS = [
    "gemini-3.5-flash-lite",  # Ultra-rápido: ~0.8s - 1.2s
    "gemini-flash-lite",      # Rápido: ~1.3s
    "gemma-4-31b-it",         # Rápido: ~4.0s
    "auto"                    # Fallback general
]


@app.get("/", response_class=HTMLResponse)
async def serve_hud():
    index_path = HUD_DIR / "index.html"
    if not index_path.exists():
        raise HTTPException(status_code=404, detail="Interfaz Iron Man HUD no encontrada")
    return FileResponse(index_path)


@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    if not API_KEY:
        return {
            "reply": "Señor, no se ha configurado la variable FREELLMAPI_API_KEY en el archivo .env. Por favor agregue su clave en .env para activar mis sistemas neuronales."
        }

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    # Evitar duplicar el prompt si ya viene en history
    history_clean = [
        msg for msg in req.history[-8:]
        if not (msg.get("role") == "user" and msg.get("content") == req.prompt)
    ]
    messages.extend(history_clean)
    messages.append({"role": "user", "content": req.prompt})

    url = f"{API_BASE_URL}/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}"}

    # Probar con los modelos ultra-rápidos con fallback automático
    last_err = ""
    for model_name in FALLBACK_MODELS:
        payload = {
            "model": model_name,
            "messages": messages,
            "max_tokens": 1200,
            "temperature": 0.7,
        }
        try:
            async with httpx.AsyncClient(timeout=6.5) as client:
                resp = await client.post(url, headers=headers, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    choices = data.get("choices", [])
                    if choices:
                        content = choices[0].get("message", {}).get("content", "").strip()
                        if content:
                            return {"reply": content, "model": model_name}
                last_err = f"HTTP {resp.status_code}"
        except Exception as exc:
            last_err = f"{type(exc).__name__}"
            continue

    return {
        "reply": "A la orden, señor. Los sistemas neuronales de MIK Software están recalculando rutas. Por favor, formule su pregunta nuevamente."
    }


class SaveKeyRequest(BaseModel):
    api_key: str
    voice_id: str = "SHkfxEDcLXK31yPii5xM"


@app.post("/api/save-elevenlabs-key")
async def save_key_endpoint(req: SaveKeyRequest):
    global ELEVENLABS_API_KEY, ELEVENLABS_VOICE_ID
    ELEVENLABS_API_KEY = req.api_key.strip()
    ELEVENLABS_VOICE_ID = req.voice_id.strip() or "SHkfxEDcLXK31yPii5xM"

    # Actualizar archivo .env
    env_file = Path(__file__).resolve().parent / ".env"
    if env_file.exists():
        content = env_file.read_text(encoding="utf-8")
        lines = []
        has_k = False
        has_v = False
        for l in content.splitlines():
            if l.startswith("ELEVENLABS_API_KEY="):
                lines.append(f"ELEVENLABS_API_KEY={ELEVENLABS_API_KEY}")
                has_k = True
            elif l.startswith("ELEVENLABS_VOICE_ID="):
                lines.append(f"ELEVENLABS_VOICE_ID={ELEVENLABS_VOICE_ID}")
                has_v = True
            else:
                lines.append(l)
        if not has_k:
            lines.append(f"ELEVENLABS_API_KEY={ELEVENLABS_API_KEY}")
        if not has_v:
            lines.append(f"ELEVENLABS_VOICE_ID={ELEVENLABS_VOICE_ID}")
        env_file.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return {"status": "saved", "voice_id": ELEVENLABS_VOICE_ID}


@app.post("/api/tts")
async def tts_endpoint(req: TTSRequest):
    key = req.api_key.strip() or ELEVENLABS_API_KEY
    voice = req.voice_id.strip() or ELEVENLABS_VOICE_ID or "SHkfxEDcLXK31yPii5xM"

    if not key:
        raise HTTPException(status_code=400, detail="ELEVENLABS_API_KEY no configurada")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"
    headers = {
        "xi-api-key": key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": req.text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True,
        },
    }

    try:
        async with httpx.AsyncClient(timeout=25.0) as client:
            resp = await client.post(
                url,
                headers=headers,
                json=payload,
                params={"output_format": "mp3_44100_128"},
            )
            if resp.status_code == 200:
                return Response(content=resp.content, media_type="audio/mpeg")
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/api/health")
async def health_endpoint():
    return {
        "status": "online",
        "ai_host": API_BASE_URL,
        "model": MODEL,
        "elevenlabs_configured": bool(ELEVENLABS_API_KEY),
        "voice_id": ELEVENLABS_VOICE_ID,
    }


def open_browser():
    time.sleep(1.2)
    webbrowser.open(f"http://localhost:{PORT}")


def main():
    os.system("cls" if os.name == "nt" else "clear")

    console.print(
        Panel.fit(
            "[bold cyan]  __  __ ___ _  __      _   _    ______     _____ ____  \n"
            " |  \\/  |_ _| |/ /     | | / \\  |  _ \\ \\   / /_ _/ ___| \n"
            " | |\\/| || || ' /   _  | |/ _ \\ | |_) \\ \\ / / | |\\___ \\ \n"
            " | |  | || || . \\  | |_| / ___ \\|  _ < \\ V /  | | ___) |\n"
            " |_|  |_|___|_|\\_\\  \\___/_/   \\_\\_| \\_\\ \\_/  |___|____/ \n[/bold cyan]"
            "[bold white]       INTERFAZ HOLOGRÁFICA IRON MAN — ARC REACTOR HUD[/bold white]\n"
            f"[dim cyan]       Conectado a: {API_BASE_URL} | Servidor: http://localhost:{PORT}[/dim cyan]",
            border_style="cyan",
        )
    )

    console.print(f"[bold green]✔ Servidor iniciado exitosamente en http://localhost:{PORT}[/bold green]")
    console.print("[dim cyan]Abriendo la interfaz futurista en tu navegador predeterminado...[/dim cyan]\n")
    console.print("[dim](Presiona Ctrl+C en esta ventana cuando desees detener el servidor)[/dim]\n")

    threading.Thread(target=open_browser, daemon=True).start()

    uvicorn.run(app, host="127.0.0.1", port=PORT, log_level="warning")


if __name__ == "__main__":
    main()

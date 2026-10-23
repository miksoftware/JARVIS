"""
MIK-JARVIS — Modo Iron Man (Activación por Voz y Aplauso)
Desarrollado para MIK Software (https://ai.miksoftwarecol.com)

Escucha pasivamente en segundo plano hasta que detecta:
1. Palabra de activación: "Hola Jarvis", "Jarvis", "Oye Jarvis", "MIK-JARVIS", "MIK"
2. O un aplauso / sonido fuerte.
Responde de forma autónoma con voz humana e inteligencia artificial de FreeLLMAPI.
"""

from __future__ import annotations

import io
import math
import os
import struct
import sys
import time
import wave
import winsound

try:
    import httpx
    import pyttsx3
    import sounddevice as sd
    from faster_whisper import WhisperModel
    from rich.console import Console
    from rich.panel import Panel
except ImportError as e:
    print(f"Error de dependencia: {e}. Ejecuta 'uv sync --extra desktop' primero.")
    sys.exit(1)

# Configuración del Entorno
API_BASE_URL = os.environ.get("FREELLMAPI_HOST", "https://ai.miksoftwarecol.com").rstrip("/")
API_KEY = os.environ.get("FREELLMAPI_API_KEY", "freellmapi-dc80607e8bd12ef930407ecf03d0e9e7d3bed844be5b2b9e")
MODEL = os.environ.get("OPENJARVIS_MODEL", "auto")

# Configuración de Audio
SAMPLE_RATE = 16000
CHUNK = 1024
CLAP_THRESHOLD = 5000       # Umbral RMS para detectar aplauso
VOICE_ACTIVATION_KEYWORDS = [
    "jarvis", "hola jarvis", "oye jarvis", "mik", "mik jarvis", 
    "amigo", "asistente", "hola", "hey jarvis"
]

console = Console()

# Inicializar TTS (Voz)
tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 175)  # Velocidad natural
voices = tts_engine.getProperty("voices")
# Seleccionar voz en español si está disponible
for v in voices:
    if "spanish" in v.name.lower() or "helena" in v.name.lower() or "es" in getattr(v, "languages", [""])[0].lower():
        tts_engine.setProperty("voice", v.id)
        break


def play_chime():
    """Sonido futurista de activación estilo Iron Man HUD."""
    try:
        winsound.Beep(880, 100)
        winsound.Beep(1320, 150)
    except Exception:
        pass


def speak_text(text: str):
    """Sintetiza y reproduce el texto en audio."""
    try:
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception as e:
        console.print(f"[red]Error en síntesis de voz: {e}[/red]")


def calculate_rms(data: bytes) -> float:
    """Calcula la energía sonora (RMS) de un bloque de audio."""
    n = len(data) // 2
    if n == 0:
        return 0.0
    shorts = struct.unpack(f"{n}h", data[: n * 2])
    return math.sqrt(sum(s * s for s in shorts) / n)


def record_phrase(silence_seconds: float = 1.3, max_seconds: float = 20.0) -> bytes:
    """Graba la voz del usuario hasta que hace silencio."""
    chunks_per_sec = SAMPLE_RATE / CHUNK
    silence_limit = int(silence_seconds * chunks_per_sec)
    max_chunks = int(max_seconds * chunks_per_sec)

    frames: list[bytes] = []
    silence_count = 0
    has_spoken = False

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE, channels=1, dtype="int16", blocksize=CHUNK
    ) as stream:
        for _ in range(max_chunks):
            raw, _ = stream.read(CHUNK)
            data = bytes(raw)
            frames.append(data)

            rms = calculate_rms(data)
            if rms > 700:
                has_spoken = True
                silence_count = 0
            elif has_spoken:
                silence_count += 1
                if silence_count >= silence_limit:
                    break
            elif len(frames) > int(4 * chunks_per_sec):
                # No habló en los primeros 4 segundos
                break

    # Empaquetar como WAV en memoria
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b"".join(frames))
    return buf.getvalue()


def query_llm(user_prompt: str) -> str:
    """Envía la solicitud al endpoint de FreeLLMAPI en miksoftwarecol.com."""
    system_prompt = (
        "Eres MIK-JARVIS, la inteligencia artificial avanzada inspirada en J.A.R.V.I.S. de Iron Man, "
        "desarrollada por MIK Software. Responde siempre con tono refinado, sumamente inteligente, "
        "elegante, respetuoso y conciso (1 a 3 oraciones por lo general, optimizado para ser escuchado). "
        "Tu interlocutor es tu creador/usuario, trátalo con cortesía ejecutiva (por ejemplo: 'A la orden', 'Por supuesto, señor')."
    )

    url = f"{API_BASE_URL}/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": 250,
        "temperature": 0.6,
    }

    try:
        with httpx.Client(timeout=30) as client:
            resp = client.post(url, headers=headers, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                choices = data.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content", "").strip()
            return f"Lo lamento, hubo un error en la conexión con el servidor (código {resp.status_code})."
    except Exception as exc:
        return f"Error al procesar la respuesta con el servidor de IA: {exc}"


def main():
    os.system("cls" if os.name == "nt" else "clear")

    console.print(
        Panel.fit(
            "[bold cyan]  __  __ ___ _  __      _   _    ______     _____ ____  \n"
            " |  \\/  |_ _| |/ /     | | / \\  |  _ \\ \\   / /_ _/ ___| \n"
            " | |\\/| || || ' /   _  | |/ _ \\ | |_) \\ \\ / / | |\\___ \\ \n"
            " | |  | || || . \\  | |_| / ___ \\|  _ < \\ V /  | | ___) |\n"
            " |_|  |_|___|_|\\_\\  \\___/_/   \\_\\_| \\_\\ \\_/  |___|____/ \n[/bold cyan]"
            "[bold white]    MODO IRON-MAN — ACTIVACIÓN POR VOZ Y APLAUSO[/bold white]\n"
            f"[dim cyan]    Conectado a: {API_BASE_URL} | Modelo: {MODEL}[/dim cyan]",
            border_style="cyan",
        )
    )

    console.print("[yellow]Cargando motor de reconocimiento Whisper (base)...[/yellow]")
    whisper_model = WhisperModel("base", device="auto", compute_type="int8")
    console.print("[green]✔ Reconocimiento auditivo calibrado y listo.[/green]\n")

    console.print("[bold green]● SISTEMA EN LÍNEA Y EN ESPERA[/bold green]")
    console.print("[dim]Di [cyan]'Hola Jarvis'[/cyan], [cyan]'Jarvis'[/cyan], [cyan]'MIK'[/cyan] o [cyan]da un aplauso[/cyan] para activarme.[/dim]")
    console.print("[dim](Presiona Ctrl+C en cualquier momento para salir)[/dim]\n")

    # Buffer circular para detección continua de palabras clave
    listen_buffer = []
    buffer_seconds = 2.0
    buffer_max_chunks = int(buffer_seconds * (SAMPLE_RATE / CHUNK))

    with sd.RawInputStream(
        samplerate=SAMPLE_RATE, channels=1, dtype="int16", blocksize=CHUNK
    ) as mic:
        while True:
            try:
                raw, _ = mic.read(CHUNK)
                data = bytes(raw)
                listen_buffer.append(data)
                if len(listen_buffer) > buffer_max_chunks:
                    listen_buffer.pop(0)

                rms = calculate_rms(data)

                # Detección de aplauso (pico alto repentino)
                activated_by_clap = rms > CLAP_THRESHOLD
                activated_by_wake_word = False

                # Detección de palabra clave cada 1.5 segundos si hay suficiente energía de voz
                if not activated_by_clap and rms > 1200 and len(listen_buffer) >= buffer_max_chunks:
                    buf = io.BytesIO()
                    with wave.open(buf, "wb") as wf:
                        wf.setnchannels(1)
                        wf.setsampwidth(2)
                        wf.setframerate(SAMPLE_RATE)
                        wf.writeframes(b"".join(listen_buffer))

                    buf.seek(0)
                    segments, _ = whisper_model.transcribe(buf, language="es", beam_size=1)
                    heard_text = " ".join([s.text for s in segments]).strip().lower()

                    if any(kw in heard_text for kw in VOICE_ACTIVATION_KEYWORDS):
                        activated_by_wake_word = True

                if activated_by_clap or activated_by_wake_word:
                    play_chime()
                    tipo = "Aplauso" if activated_by_clap else "Palabra de activación"
                    console.print(f"\n[bold yellow]⚡ ¡ACTIVACIÓN DETECTADA! ({tipo})[/bold yellow]")
                    console.print("[bold cyan]🤖 MIK-JARVIS:[/bold cyan] 'A la orden, señor.'")
                    speak_text("A la orden, señor.")

                    console.print("[cyan]🎙 Escuchando tu instrucción...[/cyan]")
                    audio_cmd = record_phrase(silence_seconds=1.2)

                    if len(audio_cmd) > 2000:
                        cmd_buf = io.BytesIO(audio_cmd)
                        segments, _ = whisper_model.transcribe(cmd_buf, language="es")
                        user_query = " ".join([s.text for s in segments]).strip()

                        if user_query:
                            console.print(f"\n[bold white]Tú dijiste:[/bold white] \"{user_query}\"")
                            console.print("[dim cyan]Procesando respuesta en MIK Software FreeLLMAPI...[/dim cyan]")

                            reply = query_llm(user_query)
                            console.print(f"\n[bold cyan]🤖 MIK-JARVIS:[/bold cyan] {reply}\n")
                            speak_text(reply)
                        else:
                            console.print("[dim]No se detectó ninguna instrucción clara.[/dim]")
                    else:
                        console.print("[dim]No se detectó audio de comando.[/dim]")

                    # Limpiar buffer y volver a espera
                    listen_buffer.clear()
                    console.print("[bold green]● Listo. Volviendo a modo de guardia en segundo plano...[/bold green]\n")

            except KeyboardInterrupt:
                console.print("\n[yellow]Desactivando MIK-JARVIS Modo Iron Man. ¡Hasta luego, señor![/yellow]")
                break
            except Exception as e:
                time.sleep(0.1)


if __name__ == "__main__":
    main()

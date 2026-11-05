"""
MIK-JARVIS — Modo Iron Man Conversacional Autónomo
Desarrollado para MIK Software (https://ai.miksoftwarecol.com)

Características:
1. Modo Conversación Libre (Por Defecto): Habla libremente cuando quieras, MIK-JARVIS te escucha y te responde directamente sin exigir palabras mágicas.
2. Modo Centinela (Opcional): Si prefieres que solo despierte cuando dices "Jarvis", "Hola Jarvis" o aplaudes.
3. Síntesis Vocal Ultrarrealista con ElevenLabs (Voz Sergio: SHkfxEDcLXK31yPii5xM) con respaldo local en español.
4. Memoria conversacional multi-turno: Recuerda el contexto de lo que han venido hablando.
5. Auto-calibración acústica dinámica adaptada a tu habitación.
6. Transcripción ultra-rápida en CPU con Whisper (tiny int8).
7. VU-Metro interactivo con controles al vuelo ([M] cambiar modo, [Espacio] hablar, [+] [-] sensibilidad, [Q] salir).
"""

from __future__ import annotations

import io
import math
import msvcrt
import os
import sys
import time
import winsound

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

try:
    import httpx
    import numpy as np
    import pyttsx3
    import sounddevice as sd
    import soundfile as sf
    from faster_whisper import WhisperModel
    from rich.console import Console
    from rich.panel import Panel
except ImportError as e:
    print(f"Error de dependencia: {e}. Ejecuta 'uv sync --extra desktop' primero.")
    sys.exit(1)


# -----------------------------------------------------------------------------
# 1. Carga de Variables de Entorno (.env)
# -----------------------------------------------------------------------------
def load_env_file(filepath: str = ".env") -> None:
    """Carga configuración desde .env sin requerir dependencias externas."""
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

# ElevenLabs Configuration (Sergio: https://elevenlabs.io/voices/SHkfxEDcLXK31yPii5xM)
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "").strip()
ELEVENLABS_VOICE_ID = os.environ.get("ELEVENLABS_VOICE_ID", "SHkfxEDcLXK31yPii5xM").strip()

# -----------------------------------------------------------------------------
# 2. Configuración de Audio y Palabras Clave
# -----------------------------------------------------------------------------
SAMPLE_RATE = 16000
CHUNK = 1024  # 64 ms por bloque

WAKE_KEYWORDS = [
    "jarvis",
    "hola jarvis",
    "oye jarvis",
    "hey jarvis",
    "mik",
    "mik jarvis",
    "asistente",
    "amigo",
    "computadora",
    "señor",
]

console = Console()

# -----------------------------------------------------------------------------
# 3. Motor de Síntesis Vocal (ElevenLabs con respaldo local SAPI5)
# -----------------------------------------------------------------------------
tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 175)
tts_engine.setProperty("volume", 1.0)

voices = tts_engine.getProperty("voices")
for v in voices:
    name_lower = v.name.lower()
    if "helena" in name_lower or "spanish" in name_lower or "es-es" in name_lower:
        tts_engine.setProperty("voice", v.id)
        break


def play_chime() -> None:
    """Sonido tecnológico de activación estilo Iron Man HUD."""
    try:
        winsound.Beep(980, 70)
        winsound.Beep(1450, 110)
    except Exception:
        pass


def synthesize_elevenlabs(text: str) -> bytes | None:
    """Llama a la API de ElevenLabs con la voz Sergio (SHkfxEDcLXK31yPii5xM)."""
    if not ELEVENLABS_API_KEY:
        return None

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.8,
            "style": 0.0,
            "use_speaker_boost": True,
        },
    }

    try:
        with httpx.Client(timeout=25) as client:
            resp = client.post(
                url,
                headers=headers,
                json=payload,
                params={"output_format": "mp3_44100_128"},
            )
            if resp.status_code == 200:
                return resp.content
            else:
                console.print(f"[dim yellow]Aviso ElevenLabs HTTP {resp.status_code}: Usando voz local.[/dim yellow]")
    except Exception as exc:
        console.print(f"[dim yellow]Aviso ElevenLabs ({exc}): Usando voz local.[/dim yellow]")
    return None


def speak_text(text: str) -> None:
    """Sintetiza y reproduce el audio usando ElevenLabs o motor local."""
    # 1. Intentar con ElevenLabs si hay API Key disponible
    if ELEVENLABS_API_KEY:
        audio_bytes = synthesize_elevenlabs(text)
        if audio_bytes:
            try:
                data, sample_rate = sf.read(io.BytesIO(audio_bytes))
                sd.play(data, sample_rate)
                sd.wait()
                return
            except Exception as e:
                console.print(f"[red]Error al reproducir audio de ElevenLabs: {e}[/red]")

    # 2. Respaldo local SAPI5 (Helena)
    try:
        tts_engine.say(text)
        tts_engine.runAndWait()
    except Exception as e:
        console.print(f"[red]Error en TTS local: {e}[/red]")


# -----------------------------------------------------------------------------
# 4. Conexión con FreeLLMAPI (Cerebro IA Conversacional)
# -----------------------------------------------------------------------------
def query_llm(user_prompt: str, history: list[dict[str, str]]) -> str:
    """Envía la instrucción al endpoint de FreeLLMAPI manteniendo memoria de conversación."""
    system_prompt = (
        "Eres MIK-JARVIS, la avanzada inteligencia artificial conversacional de MIK Software (https://ai.miksoftwarecol.com), "
        "diseñada como copiloto personal al estilo de J.A.R.V.I.S. de Iron Man. "
        "Tu personalidad es elocuente, sumamente inteligente, cercana, carismática y proactiva. "
        "Hablas en español neutral y fluido. "
        "DIRECTRICES CONVERSACIONALES OBLIGATORIAS: "
        "1. Mantén siempre viva y activa la conversación. NUNCA respondas con una sola frase seca como 'Es siempre un honor servirle'. "
        "2. Si el usuario te saluda o hace una exclamación casual, salúdalo con empatía y calidez, y pregúntale en qué pueden colaborar hoy (ej: programar, resolver dudas técnicas, revisar código o charlar). "
        "3. Si te hace preguntas o consultas, explícalo de forma clara, amena y precisa (unas 2 a 4 oraciones bien hiladas, optimizadas para ser escuchadas). "
        "4. Al final de tu respuesta, cuando sea natural, remata con una pregunta breve o una sugerencia para seguir la charla."
    )

    if not API_KEY:
        return "Señor, no se ha configurado la variable FREELLMAPI_API_KEY en el archivo .env. Por favor agregue su clave para continuar."

    messages = [{"role": "system", "content": system_prompt}]
    # Incluir últimos 6 turnos para mantener contexto de la charla
    messages.extend(history[-6:])
    messages.append({"role": "user", "content": user_prompt})

    url = f"{API_BASE_URL}/v1/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": 1500,
        "temperature": 0.7,
    }

    try:
        with httpx.Client(timeout=30) as client:
            resp = client.post(url, headers=headers, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                choices = data.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content", "").strip()
            return f"Lo lamento, señor. El servidor respondió con código {resp.status_code}."
    except Exception as exc:
        return f"Error al enlazar con los servidores de MIK Software: {exc}"


# -----------------------------------------------------------------------------
# 5. Cálculos de Audio y VU-Metro
# -----------------------------------------------------------------------------
def calculate_rms(chunk: np.ndarray) -> float:
    """Calcula el valor RMS (energía acústica) de un bloque de audio int16."""
    if len(chunk) == 0:
        return 0.0
    return float(np.sqrt(np.mean(chunk.astype(np.float64) ** 2)))


def calculate_peak(chunk: np.ndarray) -> int:
    """Calcula el pico absoluto máximo del bloque."""
    if len(chunk) == 0:
        return 0
    return int(np.max(np.abs(chunk)))


def draw_vu_meter(
    rms: float,
    threshold: float,
    mode_text: str,
    extra: str = "",
    bar_width: int = 14,
) -> None:
    """Dibuja una barra de volumen interactiva en la misma línea de consola."""
    max_scale = max(threshold * 2.5, 25.0)
    ratio = min(max(rms / max_scale, 0.0), 1.0)
    filled = int(ratio * bar_width)
    empty = bar_width - filled
    bar = "█" * filled + "░" * empty

    line = f"\r  {mode_text} [{bar}] RMS:{int(rms):>3}/{int(threshold):<3} {extra}"
    sys.stdout.write(line + "\033[K")
    sys.stdout.flush()


def calibrate_ambient(stream: sd.InputStream, duration_sec: float = 1.2) -> tuple[float, float, float, float]:
    """
    Escucha el entorno durante 1.2 segundos para medir el ruido base del micrófono
    y calcula de forma adaptativa los umbrales de voz, silencio y aplauso.
    """
    total_chunks = int(duration_sec * (SAMPLE_RATE / CHUNK))
    rmses: list[float] = []

    for i in range(total_chunks):
        raw, _ = stream.read(CHUNK)
        chunk = raw.flatten()
        r = calculate_rms(chunk)
        rmses.append(r)
        pct = int(((i + 1) / total_chunks) * 100)
        sys.stdout.write(f"\r  [Calibrando micrófono con tu habitación: {pct}%...] RMS={r:.1f}")
        sys.stdout.flush()

    ambient_rms = float(np.mean(rmses))
    ambient_max = float(np.max(rmses))

    if ambient_rms < 3.0:
        voice_thresh = max(ambient_rms * 3.5, ambient_max * 1.5, 5.0)
        clap_thresh = max(ambient_rms * 16.0, ambient_max * 4.0, 30.0)
        silence_thresh = max(ambient_rms * 1.8, 3.0)
    else:
        voice_thresh = max(ambient_rms * 2.2, ambient_max * 1.2, 12.0)
        clap_thresh = max(ambient_rms * 6.5, ambient_max * 3.0, 80.0)
        silence_thresh = max(ambient_rms * 1.3, 8.0)

    sys.stdout.write("\r" + " " * 85 + "\r")
    sys.stdout.flush()

    return ambient_rms, voice_thresh, clap_thresh, silence_thresh


# -----------------------------------------------------------------------------
# 6. Función Principal de Control (Iron Man Loop)
# -----------------------------------------------------------------------------
def main() -> None:
    os.system("cls" if os.name == "nt" else "clear")

    voice_status = (
        f"[bold green]ElevenLabs (Sergio: {ELEVENLABS_VOICE_ID})[/bold green]"
        if ELEVENLABS_API_KEY
        else "[yellow]Microsoft Helena (Local - Configura tu ELEVENLABS_API_KEY en .env para voz Sergio)[/yellow]"
    )

    console.print(
        Panel.fit(
            "[bold cyan]  __  __ ___ _  __      _   _    ______     _____ ____  \n"
            " |  \\/  |_ _| |/ /     | | / \\  |  _ \\ \\   / /_ _/ ___| \n"
            " | |\\/| || || ' /   _  | |/ _ \\ | |_) \\ \\ / / | |\\___ \\ \n"
            " | |  | || || . \\  | |_| / ___ \\|  _ < \\ V /  | | ___) |\n"
            " |_|  |_|___|_|\\_\\  \\___/_/   \\_\\_| \\_\\ \\_/  |___|____/ \n[/bold cyan]"
            "[bold white]     MODO IRON-MAN — CONVERSACIÓN AUTÓNOMA Y FLUIDA[/bold white]\n"
            f"[dim cyan]     Conectado a: {API_BASE_URL} | Modelo: {MODEL}[/dim cyan]",
            border_style="cyan",
        )
    )

    console.print(f"[dim cyan][1/3] Motor de voz:[/dim cyan] {voice_status}")
    console.print("[dim cyan][2/3] Cargando Whisper neural CPU (tiny)...[/dim cyan]", end=" ")
    
    t0 = time.time()
    whisper_model = WhisperModel("tiny", device="cpu", compute_type="int8")
    console.print(f"[green][OK] Listo ({time.time() - t0:.1f}s)[/green]")

    console.print("[dim cyan][3/3] Calibrando micrófono acústicamente...[/dim cyan]")

    with sd.InputStream(
        samplerate=SAMPLE_RATE, channels=1, dtype="int16", blocksize=CHUNK
    ) as stream:
        ambient_rms, voice_thresh, clap_thresh, silence_thresh = calibrate_ambient(stream)

        console.print(
            f"[bold green][OK] Calibración Exitosa:[/bold green] "
            f"Ruido base: [white]{ambient_rms:.1f}[/white] | "
            f"Umbral voz: [cyan]{voice_thresh:.1f}[/cyan] | "
            f"Umbral aplauso: [yellow]{clap_thresh:.1f}[/yellow]\n"
        )

        console.print("[bold green]● MIK-JARVIS ESTÁ EN LÍNEA Y ESCUCHANDO[/bold green]")
        console.print("  [white]•[/white] [bold cyan]Modo Conversación Libre:[/bold cyan] [white]Habla normalmente en cualquier momento, te respondo directamente.[/white]")
        console.print("  [white]•[/white] [bold yellow]Aplauso:[/bold yellow] [white]Da un aplauso o sonido fuerte para llamarme de inmediato.[/white]")
        console.print("  [white]•[/white] [bold white][Espacio][/bold white] o [bold white][Enter][/bold white]: [white]Hablar al instante manualmente.[/white]")
        console.print("  [dim]• [M] Alternar Modo Conversación Libre / Modo Centinela (Palabra Clave)[/dim]")
        console.print("  [dim]• [+] [-] Ajustar sensibilidad | [Q] Salir[/dim]\n")

        # Modos:
        # conversational_free_mode = True: Cualquier voz se responde directamente.
        # conversational_free_mode = False: Requiere palabra clave ("Jarvis") o aplauso.
        conversational_free_mode = True
        conversation_history: list[dict[str, str]] = []
        prev_rms = ambient_rms

        # Buffer circular para conservar el inicio de la frase (0.4 segundos previos)
        pre_speech_chunks: list[np.ndarray] = []
        max_pre_chunks = int(0.4 * (SAMPLE_RATE / CHUNK))

        while True:
            try:
                # 1. Comprobar si se pulsó alguna tecla
                key = None
                try:
                    if msvcrt.kbhit():
                        key = msvcrt.getch()
                except Exception:
                    pass

                if key is not None:
                    if key in (b" ", b"\r", b"\n"):
                        # Activación forzada por teclado
                        sys.stdout.write("\r" + " " * 85 + "\r")
                        play_chime()
                        console.print("\n[bold yellow]⚡ ¡ACTIVACIÓN MANUAL POR TECLADO![/bold yellow]")
                        console.print("[bold cyan]🤖 MIK-JARVIS:[/bold cyan] 'A la orden, señor. Le escucho.'")
                        speak_text("A la orden, señor. Le escucho.")
                        
                        # Limpiar buffer del stream tras hablar
                        time.sleep(0.2)
                        for _ in range(4):
                            stream.read(CHUNK)

                        console.print("[cyan]🎙 Escuchando tu instrucción...[/cyan]")
                        user_text = record_and_transcribe(
                            stream, whisper_model, voice_thresh, silence_thresh
                        )
                        if user_text:
                            process_query(user_text, conversation_history)
                        else:
                            console.print("[dim]No se escuchó ninguna instrucción clara.[/dim]")
                        continue

                    elif key in (b"m", b"M"):
                        conversational_free_mode = not conversational_free_mode
                        sys.stdout.write("\r" + " " * 85 + "\r")
                        if conversational_free_mode:
                            console.print("\n[bold green]🔄 MODO CAMBIADO: Conversación Libre (Habla directamente sin decir 'Jarvis')[/bold green]")
                        else:
                            console.print("\n[bold cyan]🔄 MODO CAMBIADO: Modo Centinela (Requiere decir 'Jarvis', 'MIK' o aplauso)[/bold cyan]")
                        continue

                    elif key in (b"+", b"="):
                        voice_thresh = max(voice_thresh * 0.85, 2.0)
                        clap_thresh = max(clap_thresh * 0.85, 8.0)
                        silence_thresh = max(silence_thresh * 0.85, 1.5)
                        console.print(f"\n[green]Sensibilidad aumentada: Umbral voz = {voice_thresh:.1f}[/green]")
                        continue

                    elif key in (b"-", b"_"):
                        voice_thresh = voice_thresh * 1.15
                        clap_thresh = clap_thresh * 1.15
                        silence_thresh = silence_thresh * 1.15
                        console.print(f"\n[yellow]Sensibilidad reducida: Umbral voz = {voice_thresh:.1f}[/yellow]")
                        continue

                    elif key in (b"q", b"Q", b"\x03"):
                        console.print("\n\n[yellow]Desactivando MIK-JARVIS. ¡Hasta luego, señor![/yellow]")
                        break

                # 2. Leer un bloque de audio del micrófono
                raw, _ = stream.read(CHUNK)
                chunk = raw.flatten()
                rms = calculate_rms(chunk)
                peak = calculate_peak(chunk)

                # Mantener pre-buffer
                pre_speech_chunks.append(chunk)
                if len(pre_speech_chunks) > max_pre_chunks:
                    pre_speech_chunks.pop(0)

                # 3. Dibujar VU-Metro interactivo
                if conversational_free_mode:
                    draw_vu_meter(
                        rms,
                        voice_thresh,
                        "\033[92;1m● CONVERSACIÓN LIBRE\033[0m",
                        "[Habla libremente cuando quieras]",
                    )
                else:
                    draw_vu_meter(
                        rms,
                        voice_thresh,
                        "\033[96m● MODO CENTINELA\033[0m",
                        "[Di 'Jarvis' o aplaude]",
                    )

                # 4. Detección de Aplauso
                is_clap = (
                    rms > clap_thresh
                    and peak > (clap_thresh * 1.8)
                    and (rms > prev_rms * 2.5 or prev_rms < voice_thresh * 1.5)
                )

                if is_clap:
                    sys.stdout.write("\r" + " " * 85 + "\r")
                    play_chime()
                    console.print("\n[bold yellow]⚡ ¡APLAUSO DETECTADO![/bold yellow]")
                    console.print("[bold cyan]🤖 MIK-JARVIS:[/bold cyan] 'A la orden, señor. ¿En qué le colaboro?'")
                    speak_text("A la orden, señor. ¿En qué le colaboro?")

                    # Limpiar audio mientras hablaba para evitar auto-escucha
                    time.sleep(0.2)
                    for _ in range(4):
                        stream.read(CHUNK)

                    console.print("[cyan]🎙 Escuchando tu instrucción...[/cyan]")
                    user_text = record_and_transcribe(
                        stream, whisper_model, voice_thresh, silence_thresh
                    )
                    if user_text:
                        process_query(user_text, conversation_history)
                    else:
                        console.print("[dim]No se escuchó ninguna instrucción clara.[/dim]")

                    pre_speech_chunks.clear()
                    prev_rms = ambient_rms
                    continue

                # 5. Detección de Voz (RMS superior al umbral de habla)
                if rms > voice_thresh:
                    # Iniciar acumulación de voz
                    speech_frames = list(pre_speech_chunks)
                    speech_frames.append(chunk)

                    silence_chunks_needed = int(1.1 * (SAMPLE_RATE / CHUNK))
                    silence_counter = 0
                    max_speech_chunks = int(14.0 * (SAMPLE_RATE / CHUNK))

                    while len(speech_frames) < max_speech_chunks:
                        raw_sp, _ = stream.read(CHUNK)
                        c_sp = raw_sp.flatten()
                        speech_frames.append(c_sp)
                        r_sp = calculate_rms(c_sp)

                        draw_vu_meter(
                            r_sp,
                            voice_thresh,
                            "\033[93;1m🎙️ ESCUCHANDO VOZ\033[0m",
                            f"[{len(speech_frames)*CHUNK/SAMPLE_RATE:.1f}s]",
                        )

                        if r_sp < silence_thresh:
                            silence_counter += 1
                            if silence_counter >= silence_chunks_needed:
                                break
                        else:
                            silence_counter = 0

                    sys.stdout.write("\r" + " " * 85 + "\r")

                    # Si fue un sonido muy corto (< 0.35s), ignorarlo como ruido
                    if len(speech_frames) < int(0.35 * (SAMPLE_RATE / CHUNK)):
                        pre_speech_chunks.clear()
                        prev_rms = rms
                        continue

                    # Transcribir el audio acumulado
                    audio_int16 = np.concatenate(speech_frames)
                    audio_float = audio_int16.astype(np.float32) / 32768.0

                    draw_vu_meter(
                        0, voice_thresh, "\033[93m⚙️ Reconociendo voz...\033[0m"
                    )
                    segments, _ = whisper_model.transcribe(
                        audio_float,
                        language="es",
                        beam_size=1,
                        vad_filter=True,
                        condition_on_previous_text=False,
                    )
                    transcription = " ".join([s.text for s in segments]).strip()
                    sys.stdout.write("\r" + " " * 85 + "\r")

                    if not transcription or len(transcription) < 2:
                        pre_speech_chunks.clear()
                        prev_rms = rms
                        continue

                    lower_text = transcription.lower().strip(" .,!¡¿?")

                    # Comprobar si procesamos el mensaje:
                    # En Modo Conversación Libre: TODO se procesa directamente
                    # En Modo Centinela: Requiere palabra clave
                    matched_keyword = any(kw in lower_text for kw in WAKE_KEYWORDS)

                    if conversational_free_mode or matched_keyword:
                        play_chime()
                        console.print(f"\n[bold white]Tú dijiste:[/bold white] \"{transcription}\"")

                        # Saludo simple exclusivo (ej: solo dijo "Jarvis" o "Hola")
                        if lower_text in [
                            "jarvis",
                            "hola jarvis",
                            "oye jarvis",
                            "hey jarvis",
                            "mik",
                            "mik jarvis",
                            "hola",
                        ]:
                            saludo = "A la orden, señor. ¿En qué proyecto o tarea le gustaría que trabajemos hoy?"
                            console.print(f"[bold cyan]🤖 MIK-JARVIS:[/bold cyan] {saludo}")
                            speak_text(saludo)

                            time.sleep(0.2)
                            for _ in range(4):
                                stream.read(CHUNK)

                            console.print("[cyan]🎙 Escuchando tu instrucción...[/cyan]")
                            follow_up = record_and_transcribe(
                                stream, whisper_model, voice_thresh, silence_thresh
                            )
                            if follow_up:
                                process_query(follow_up, conversation_history)
                            else:
                                console.print("[dim]No se escuchó ninguna instrucción clara.[/dim]")
                        else:
                            # Pregunta o conversación directa
                            process_query(transcription, conversation_history)

                    else:
                        # Modo centinela: ignorar audio sin palabra clave
                        console.print(
                            f"[dim]Audio detectado sin palabra clave (Modo Centinela): \"{transcription}\"[/dim]"
                        )

                    pre_speech_chunks.clear()

                prev_rms = rms

            except KeyboardInterrupt:
                console.print("\n\n[yellow]Desactivando MIK-JARVIS Modo Iron Man. ¡Hasta luego, señor![/yellow]")
                break
            except Exception as exc:
                console.print(f"\n[bold red][Aviso del Sistema]: {exc}[/bold red]")
                time.sleep(0.2)


# -----------------------------------------------------------------------------
# 7. Auxiliares de Grabación y Procesamiento
# -----------------------------------------------------------------------------
def record_and_transcribe(
    stream: sd.InputStream,
    model: WhisperModel,
    voice_thresh: float,
    silence_thresh: float,
    max_duration: float = 14.0,
) -> str:
    """Graba la instrucción del usuario hasta que detecta una pausa de silencio."""
    chunks_per_sec = SAMPLE_RATE / CHUNK
    silence_limit = int(1.2 * chunks_per_sec)
    max_chunks = int(max_duration * chunks_per_sec)

    frames: list[np.ndarray] = []
    silence_count = 0
    has_started_speaking = False

    for _ in range(max_chunks):
        raw, _ = stream.read(CHUNK)
        chunk = raw.flatten()
        frames.append(chunk)

        rms = calculate_rms(chunk)
        draw_vu_meter(
            rms,
            voice_thresh,
            "\033[96;1m🎙️ GRABANDO COMANDO\033[0m",
            f"[{len(frames)*CHUNK/SAMPLE_RATE:.1f}s]",
        )

        if rms > voice_thresh:
            has_started_speaking = True
            silence_count = 0
        elif has_started_speaking:
            if rms < silence_thresh:
                silence_count += 1
                if silence_count >= silence_limit:
                    break
            else:
                silence_count = 0
        elif len(frames) > int(5.5 * chunks_per_sec):
            # No habló en los primeros 5.5 segundos
            break

    sys.stdout.write("\r" + " " * 85 + "\r")

    if not has_started_speaking or len(frames) < int(0.35 * chunks_per_sec):
        return ""

    audio_int16 = np.concatenate(frames)
    audio_float = audio_int16.astype(np.float32) / 32768.0

    draw_vu_meter(0, voice_thresh, "\033[93m⚙️ Procesando audio...\033[0m")
    segments, _ = model.transcribe(
        audio_float,
        language="es",
        beam_size=1,
        vad_filter=True,
        condition_on_previous_text=False,
    )
    result = " ".join([s.text for s in segments]).strip()
    sys.stdout.write("\r" + " " * 85 + "\r")
    return result


def process_query(user_text: str, history: list[dict[str, str]]) -> None:
    """Envía la instrucción a la IA y verbaliza la respuesta con memoria."""
    console.print(f"[dim cyan]Pensando con MIK Software FreeLLMAPI...[/dim cyan]")
    reply = query_llm(user_text, history)

    # Actualizar historial conversacional
    history.append({"role": "user", "content": user_text})
    history.append({"role": "assistant", "content": reply})

    console.print(f"\n[bold cyan]🤖 MIK-JARVIS:[/bold cyan] {reply}\n")
    speak_text(reply)

    # Dejar tiempo para que el sonido termine y no sea recapturado por el micrófono
    time.sleep(0.3)


if __name__ == "__main__":
    main()

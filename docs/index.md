---
title: MIK-JARVIS
description: Asistente Inteligente de IA y Copiloto Holográfico — MIK Software
search:
  boost: 2
hide:
  - navigation
---

# Personal AI, On Personal Devices

<p class="hero-tagline">
MIK-JARVIS es un ecosistema integral y modular de Inteligencia Artificial desarrollado para MIK Software.
Construye y ejecuta IA personal en tu propio hardware y conectado a FreeLLMAPI.
</p>

<div class="grid cards" markdown>

-   :material-image-multiple:{ .lg .middle } **Mira lo que puedes hacer**

    ---

    Asistente con modos holográficos Iron Man HUD, resúmenes diarios, integración con voz ultrarrealista ElevenLabs, ejecución de código y conexión a modelos de alto rendimiento.

    [:octicons-arrow-right-24: Ver Demostraciones](showcase/index.md)

</div>

---

## ¿Por qué MIK-JARVIS?

MIK-JARVIS es la plataforma de IA de **MIK Software** pensada para dar autonomía, privacidad y velocidad. Integra interfaces futuristas estilo Iron Man con un backend de alto rendimiento conectado a modelos de vanguardia y síntesis de voz en español.

---

## Get Started

=== "Browser App"

    Run the full chat UI locally with one script:

    ```bash
    git clone https://github.com/miksoftware/JARVIS.git
    cd JARVIS
    ./scripts/quickstart.sh
    ```

    This installs dependencies, starts Ollama + a local model, launches the backend
    and frontend, and opens `http://localhost:5173` in your browser.

=== "Desktop App"

    The desktop app is a native window for the MIK-JARVIS UI.
    The backend runs on your machine — start it first, then open the app.

    **Step 1.** Start the backend:

    ```bash
    git clone https://github.com/miksoftware/JARVIS.git
    cd JARVIS
    ./scripts/quickstart.sh
    ```

    **Step 2.** Download and open the desktop app:

    [Download for Windows](https://github.com/miksoftware/JARVIS/releases){ .md-button .md-button--primary }

    Also available for macOS and Linux. See the [Downloads](downloads.md) page for details.

    The app connects to `http://localhost:8000` automatically.

=== "Python SDK"

    ```python
    from openjarvis import Jarvis

    j = Jarvis()                              # auto-detect engine
    response = j.ask("Explain quicksort.")
    print(response)
    ```

    For more control, use `ask_full()` to get usage stats, model info, and tool results:

    ```python
    result = j.ask_full(
        "What is 2 + 2?",
        agent="orchestrator",
        tools=["calculator"],
    )
    print(result["content"])       # "4"
    print(result["tool_results"])  # [{tool_name: "calculator", ...}]
    ```

=== "CLI"

    ```bash
    jarvis ask "What is the capital of France?"

    jarvis ask --agent orchestrator --tools calculator "What is 137 * 42?"

    jarvis serve --port 8000

    jarvis memory index ./docs/
    jarvis memory search "configuration options"
    ```

---

## Five Primitives for Personal AI

OpenJarvis is built around five composable layers. Each has a clean interface and can be swapped independently.

1. **Intelligence** — Pick a model, or let OpenJarvis pick one for your hardware. Manages the full catalog of local models across providers.
2. **Engine** — The inference runtime: [Ollama](https://ollama.com), [vLLM](https://github.com/vllm-project/vllm), [SGLang](https://github.com/sgl-project/sglang), [llama.cpp](https://github.com/ggerganov/llama.cpp), cloud APIs, and more. Auto-detects your hardware and recommends the best fit.
3. **Agents** — Multi-step reasoning with tool use. Eight built-in agent types from simple chat to orchestrated workflows.
4. **Tools & Memory** — Web search, calculator, file I/O, code interpreter, retrieval, persistent local state, and any external MCP server.
5. **Learning** — Your AI gets better over time. Every interaction generates traces that drive automatic improvements to model weights, prompts, and agent behavior.

---

## Key Features

<div class="grid cards" markdown>

-   **10+ Engine Backends**

    ---

    [Ollama](https://ollama.com), [vLLM](https://github.com/vllm-project/vllm), [SGLang](https://github.com/sgl-project/sglang), [llama.cpp](https://github.com/ggerganov/llama.cpp), [MLX](https://github.com/ml-explore/mlx), [Exo](https://github.com/exo-explore/exo), [LiteLLM](https://github.com/BerriAI/litellm), cloud (OpenAI/Anthropic/Google), and more. Same `InferenceEngine` interface, swap freely.

-   **Automated Workflows**

    ---

    Cron-based agents that monitor, summarize, and act. Code review, email triage, research digests — running 24/7 on your hardware.

-   **Hardware-Aware**

    ---

    Auto-detects GPU vendor, model, and VRAM. Recommends the optimal engine for your hardware.

-   **Offline-First**

    ---

    All core functionality works without a network connection. Cloud APIs are optional extras.

-   **OpenAI-Compatible API**

    ---

    `jarvis serve` starts a FastAPI server with SSE streaming. Drop-in replacement for OpenAI clients.

-   **Energy & Cost Tracking**

    ---

    Built-in telemetry for GPU power draw, token costs, and latency. See exactly what each query costs in watts and dollars.

</div>

---

## Documentation

<div class="grid cards" markdown>

-   **[Getting Started](getting-started/installation.md)**

    ---

    Install OpenJarvis, configure your first engine, and run your first query.

-   **[User Guide](user-guide/cli.md)**

    ---

    CLI, Python SDK, and guides for [Morning Digest](user-guide/morning-digest.md), [Deep Research](user-guide/deep-research.md), [Code Assistant](user-guide/code-assistant.md), [Scheduled Monitor](user-guide/scheduled-monitor.md), [Simple Chat](user-guide/chat-simple.md), [Evaluations](user-guide/evaluations.md), agents, memory, tools, and telemetry.

-   **[Architecture](architecture/overview.md)**

    ---

    Five-primitive design, registry pattern, query flow, and cross-cutting learning.

-   **[API Reference](api-reference/openjarvis/index.md)**

    ---

    Auto-generated reference for every module.

-   **[Deployment](deployment/docker.md)**

    ---

    Docker, systemd, launchd. GPU-accelerated container images.

-   **[Development](development/contributing.md)**

    ---

    Contributing guide, extension patterns, roadmap, and changelog.

</div>

## Research

OpenJarvis is part of [Intelligence Per Watt](https://www.intelligence-per-watt.ai/), a research initiative studying the efficiency of on-device AI systems. Developed at [Hazy Research](https://hazyresearch.stanford.edu/) and the [Scaling Intelligence Lab](https://scalingintelligence.stanford.edu/) at [Stanford SAIL](https://ai.stanford.edu/).

Read the [blog post](https://openjarvis.stanford.edu/) for the full research motivation, architecture details, and experimental results.

## Citation

```bibtex
@misc{saadfalcon2026openjarvispersonalaipersonal,
      title={OpenJarvis: Personal AI, On Personal Devices}, 
      author={Jon Saad-Falcon and Avanika Narayan and Robby Manihani and Tanvir Bhathal and Herumb Shandilya and Hakki Orhun Akengin and Gabriel Bo and Andrew Park and Matthew Hart and Caia Costello and Chuan Li and Christopher Ré and Azalia Mirhoseini},
      year={2026},
      eprint={2605.17172},
      archivePrefix={arXiv},
      primaryClass={cs.LG},
      url={https://arxiv.org/abs/2605.17172}, 
}
```

## Sponsors

<p>
  <a href="https://www.laude.org/">Laude Institute</a> &bull;
  <a href="https://datascience.stanford.edu/marlowe">Stanford Marlowe</a> &bull;
  <a href="https://cloud.google.com/">Google Cloud Platform</a> &bull;
  <a href="https://lambda.ai/">Lambda Labs</a> &bull;
  <a href="https://ollama.com/">Ollama</a> &bull;
  <a href="https://research.ibm.com/">IBM Research</a> &bull;
  <a href="https://hai.stanford.edu/">Stanford HAI</a>
</p>

Follow [@OpenJarvisAI](https://x.com/OpenJarvisAI) on X for updates.

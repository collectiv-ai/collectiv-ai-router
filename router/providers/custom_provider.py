import asyncio
from typing import Optional


async def complete(prompt: str, model_id: Optional[str]) -> tuple[str, str]:
    """Placeholder for a custom backend provider.

    In the public CollectiVAI Router demo, this is intentionally disabled.
    In your private deployment you can replace this with:
    - a local RAG / vector search backend
    - a self-hosted LLM (Ollama, vLLM, etc.)
    - a civic data pipeline
    """
    await asyncio.sleep(0.01)
    # Wir geben hier bewusst einen Fehler zurück, damit klar ist:
    # Custom-Backend ist in dieser Demo NICHT konfiguriert.
    raise ValueError(
        "Custom provider is not configured in this public demo. "
        "Please use one of: openai, gemini, mistral, meta, deepseek, auto."
    )

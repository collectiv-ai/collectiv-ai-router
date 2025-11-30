import asyncio
from typing import Optional


async def complete(prompt: str, model_id: Optional[str]) -> tuple[str, str]:
    await asyncio.sleep(0.05)
    model = model_id or "gemini-2.0-flash"
    return f"[Gemini / {model}] Demo reply for: {prompt[:80]}...", model

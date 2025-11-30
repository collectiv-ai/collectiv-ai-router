from typing import Tuple
import asyncio


async def complete(prompt: str, model_id: str | None) -> Tuple[str, str]:
    await asyncio.sleep(0.05)
    model = model_id or "deepseek-chat"
    return f"[DeepSeek / {model}] Demo reply for: {prompt[:80]}...", model

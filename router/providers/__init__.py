from typing import Awaitable, Callable, Optional, Dict, Tuple

from . import (
    openai_provider,
    gemini_provider,
    mistral_provider,
    meta_provider,
    deepseek_provider,
    custom_provider,
)

ProviderFn = Callable[[str, Optional[str]], Awaitable[tuple[str, str]]]

# Zentrale Registry aller Provider-Implementierungen
PROVIDER_REGISTRY: Dict[str, ProviderFn] = {
    "openai": openai_provider.complete,
    "gemini": gemini_provider.complete,
    "mistral": mistral_provider.complete,
    "meta": meta_provider.complete,
    "deepseek": deepseek_provider.complete,
    "custom": custom_provider.complete,
}


async def call_provider(provider: str, prompt: str, model_id: Optional[str]) -> tuple[str, str]:
    """Dispatch to a concrete provider.

    Returns:
        (reply_text, model_name)
    """
    key = (provider or "").strip().lower()

    try:
        fn = PROVIDER_REGISTRY[key]
    except KeyError:
        raise ValueError(f"Unknown provider: {provider!r}")

    return await fn(prompt, model_id)

"""Provider registry for the CollectiVAI Router.

Each provider module exposes an async `complete(prompt: str, model_id: str | None)`
function that returns a plain string reply.
"""

from . import openai_provider, gemini_provider, mistral_provider, meta_provider, deepseek_provider, custom_provider  # noqa: F401


async def call_provider(provider: str, prompt: str, model_id: str | None) -> tuple[str, str]:
    """Dispatch to a concrete provider.

    Returns:
        (reply_text, model_name)
    """
    p = provider.lower()
    if p == "openai":
        return await openai_provider.complete(prompt, model_id)
    if p == "gemini":
        return await gemini_provider.complete(prompt, model_id)
    if p == "mistral":
        return await mistral_provider.complete(prompt, model_id)
    if p == "meta":
        return await meta_provider.complete(prompt, model_id)
    if p == "deepseek":
        return await deepseek_provider.complete(prompt, model_id)
    if p == "custom":
        return await custom_provider.complete(prompt, model_id)

    raise ValueError(f"Unknown provider: {provider}")

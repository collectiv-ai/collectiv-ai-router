from .models import ChatRequest


def choose_provider(request: ChatRequest) -> str:
    """Very small example of routing logic.

    For now this is intentionally simple and deterministic. You can extend this
    with more advanced rules, scores, costs, etc.
    """

    if request.provider != "auto":
        return request.provider

    # Auto‑routing example – feel free to tune:
    topic = request.topic.lower()
    mode = request.mode.lower()

    if mode == "technical":
        # favour code / security‑strong providers
        return "mistral"
    if topic in {"democracy", "economy"}:
        return "openai"
    if topic in {"climate", "research"}:
        return "gemini"

    # fallback
    return "openai"

from time import perf_counter

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .models import ChatRequest, ChatResponse, RoutingInfo
from .routing import choose_provider
from .providers import call_provider


settings = get_settings()

app = FastAPI(title="CollectiVAI Router", version="0.2.0")

# CORS
if settings.allowed_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/health")
async def health() -> dict:
    """Simple health‑check endpoint used by monitoring and the app."""
    return {"status": "ok", "version": app.version}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    """Main chat endpoint used by the CollectiVAI app."""

    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Empty prompt")

    # Decide which provider to use (auto or fixed)
    provider = choose_provider(request)

    # Simple latency measurement
    start = perf_counter()
    try:
        reply_text, model_name = await call_provider(provider, request.prompt, request.modelId)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:  # pragma: no cover - generic safeguard
        # In a real deployment you would log this in a secure way.
        raise HTTPException(status_code=502, detail="Upstream error") from e
    latency_ms = int((perf_counter() - start) * 1000)

    routing_info = RoutingInfo(
        reason=f"Routed to {provider} based on mode={request.mode}, topic={request.topic}.",
        filters=[request.mode, request.topic],
        latencyMs=latency_ms,
    )

    return ChatResponse(
        reply=reply_text,
        providerUsed=provider,
        model=model_name,
        routingInfo=routing_info,
    )

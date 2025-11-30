from typing import List, Optional
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="User prompt text")
    mode: str = Field(..., description="Routing mode (ethical, research, technical)")
    provider: str = Field(..., description="Requested provider (auto, openai, gemini, mistral, meta, deepseek, custom)")
    topic: str = Field(..., description="High‑level topic (democracy, climate, economy, security, research, health)")
    modelId: Optional[str] = Field(None, description="Optional explicit model ID")
    serviceProfile: Optional[str] = Field(None, description="Civic service profile (city_service, ngo_lab, etc.)")


class RoutingInfo(BaseModel):
    reason: str | None = None
    filters: List[str] | None = None
    latencyMs: int | None = None


class ChatResponse(BaseModel):
    reply: str
    providerUsed: str
    model: str
    routingInfo: RoutingInfo | None = None

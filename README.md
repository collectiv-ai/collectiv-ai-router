<p align="center">
  <img src="logo.png" alt="CollectiVAI Logo" width="400" />
</p>

<h1 align="center">CollectiVAI Router</h1>
<h3 align="center">Mini backend for democratic AI routing</h3>

<p align="center">
  <a href="https://collectivai.org">
    <img src="https://img.shields.io/badge/Website-collectivai.org-003399?style=flat" alt="Website" />
  </a>
  <a href="https://github.com/collectiv-ai/collectiv-ai-app">
    <img src="https://img.shields.io/badge/App-iOS%20%7C%20iPadOS%20%7C%20macOS-ffcc00?style=flat" alt="App" />
  </a>
  <img src="https://img.shields.io/badge/Made%20in-Europe-003399?style=flat" alt="Made in Europe" />
</p>

---

# CollectiVAI Router (Backend)

This repository contains the **CollectiVAI Router** – a small backend that
receives chat requests from the CollectiVAI App, applies routing logic
(provider, model, mode, topic) and forwards them to 3rd-party AI APIs
such as **OpenAI, Gemini, Mistral, Meta and DeepSeek**.

> **Security first:**  
> – No provider API keys are stored in the iOS/macOS app.  
> – All provider keys live only as **environment variables** (e.g. in `.env` or Cloudflare secrets).  
> – The router is protected by a **router token** header.  
> – Custom / external backends are **not** freely configurable by the client – only allowlisted on the server side.

The code is written in **Python** using **FastAPI**, and can be run locally
with `uvicorn` and deployed behind **Cloudflare** or another reverse proxy.

---

## 1. Features

- Single `/api/chat` endpoint for the CollectiVAI App
- Routing fields compatible with your current Xcode app:
  - `mode` (ethical / research / technical)
  - `provider` (auto / openai / gemini / mistral / meta / deepseek)
  - `topic` (democracy, climate, economy, security, research, health)
  - optional `modelId` and `serviceProfile`
- Simple routing logic in `router/routing.py` that you can extend later
- **Router auth token** via `X-CollectivAI-Token` HTTP header
- CORS configuration via env variable `ALLOWED_ORIGINS`
- Clean separation of:
  - `router/models.py` (Pydantic models for request/response)
  - provider-specific logic in `router/providers/*`
  - configuration in `router/config.py`

By default, the providers return **placeholder responses** to keep the
router safe for first deployment. You can gradually enable real calls to
each provider once you have tested everything.

---

## 2. Project structure

```text
collectiv-ai-router/
├── README.md
├── SECURITY_NOTES.md
├── requirements.txt
├── example.env
├── .gitignore
└── router/
    ├── __init__.py
    ├── config.py
    ├── main.py
    ├── models.py
    ├── routing.py
    └── providers/
        ├── __init__.py
        ├── base.py
        ├── openai_provider.py
        ├── gemini_provider.py
        ├── mistral_provider.py
        ├── meta_provider.py
        └── deepseek_provider.py
```

- `router/main.py` – FastAPI application, `/api/chat` and `/health` endpoints, router token check, CORS.
- `router/config.py` – Reads environment variables, never hard-codes keys.
- `router/models.py` – Request/response models compatible with your app.
- `router/routing.py` – Decides which provider/model to call.
- `router/providers/*` – Provider-specific stubs (OpenAI, Gemini, etc.).
- `SECURITY_NOTES.md` – Short overview of security assumptions and checklist.

---

## 3. Local development

### 3.1. Clone and install

```bash
git clone https://github.com/collectiv-ai/collectiv-ai-router.git
cd collectiv-ai-router

# create virtualenv (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate    # macOS / Linux

pip install -r requirements.txt
```

### 3.2. Configure environment

Copy the example environment file and fill in your own secrets:

```bash
cp example.env .env
```

Then edit `.env` and set:

- `COLLECTIVAI_ROUTER_TOKEN` – a long random string, also used in the app.
- `ALLOWED_ORIGINS` – for example `https://collectivai.org` or leave empty in dev.
- `OPENAI_API_KEY`, `GEMINI_API_KEY`, `MISTRAL_API_KEY`, `META_API_KEY`, `DEEPSEEK_API_KEY`.

> **Important:** Never commit the real `.env` file to Git.  
> `.gitignore` is already configured to ignore `.env`.

### 3.3. Run locally (uvicorn)

```bash
uvicorn router.main:app --reload --host 0.0.0.0 --port 8000
```

Now the router is available at:

- `http://localhost:8000/health`
- `http://localhost:8000/api/chat`

You can test it with a simple `curl`:

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -H "X-CollectivAI-Token: change-this-to-a-long-random-string" \
  -d '{
    "prompt": "Hello CollectiVAI Router",
    "mode": "ethical",
    "provider": "auto",
    "topic": "democracy"
  }'
```

The response will be a JSON object with a placeholder reply until you enable real providers.

---

## 4. Security model (short)

- The router expects a **router token** in the header:

  ```http
  X-CollectivAI-Token: <COLLECTIVAI_ROUTER_TOKEN>
  ```

  If `COLLECTIVAI_ROUTER_TOKEN` is set in the environment, all requests
  without a matching token will receive `401 Unauthorized`.

- All 3rd-party API keys (OpenAI, Gemini, Mistral, Meta, DeepSeek) are
  read only from environment variables. They are **never logged** and **never
  sent back** in responses.

- The current version exposes **no dynamic custom URL provider**.  
  That means the client cannot send arbitrary URLs – this avoids SSRF-style
  abuse. If you later want to connect your own models, you can do that
  by hard-coding a small allowlist of backends on the server side.

- Cloudflare can be used in front of this router for:
  - WAF rules (only allow `POST /api/chat`, block others),
  - rate limiting,
  - IP filtering if desired.

See `SECURITY_NOTES.md` for a more detailed checklist.

---

## 5. How it connects to the CollectiVAI App

Your iOS/macOS app currently sends requests like:

```jsonc
{
  "prompt": "...",
  "mode": "ethical",        // maps to CollectivMode
  "provider": "auto",       // auto, openai, gemini, mistral, meta, deepseek
  "topic": "democracy",     // democracy, climate, ...
  "modelId": "gpt-4.1",     // optional
  "serviceProfile": "citizen_advisor" // optional
}
```

The router:

1. Verifies the `X-CollectivAI-Token` header.
2. Applies routing rules based on `mode`, `topic`, `provider`, `modelId`.
3. Calls one of the provider backends (OpenAI, Gemini, etc.).
4. Returns a standardised JSON response:

```jsonc
{
  "reply": "text answer",
  "providerUsed": "openai",
  "model": "gpt-4.1",
  "routingInfo": {
    "reason": "auto: picked OpenAI gpt-4.1 for ethical/democracy.",
    "filters": ["safe-mode"],
    "latencyMs": 1234
  }
}
```

This schema is implemented in `router/models.py` and `router/routing.py`.

---

## 6. Deployment behind Cloudflare (high-level)

You can deploy the router on any Python backend (VM, container, serverless)
and then put Cloudflare in front of it:

1. Deploy the FastAPI app (e.g. on a small VPS or platform-as-a-service).
2. Configure a Cloudflare DNS entry, e.g. `collectivai-server.collectivai.workers.dev`
   or a custom subdomain.
3. Enable:
   - HTTPS,
   - WAF rules for `/api/chat`,
   - rate limiting per IP or per path.
4. Set environment variables / secrets on the backend (not in Cloudflare pages).

The CollectiVAI App then points to:

```swift
static let endpoint = URL(string: "https://your-router-domain/api/chat")!
```

plus the router token header.

---

## 7. Next steps

- [ ] Wire real calls inside `router/providers/*.py` step by step.
- [ ] Add per-user or per-device tokens if you later have multiple users.
- [ ] Add logging/metrics (without sensitive data) for monitoring.
- [ ] Optionally add a **Custom provider** with a strict server-side allowlist.

For now, this repository gives you a **safe, minimal and security-aware**
starting point that matches your current CollectiVAI App interface.

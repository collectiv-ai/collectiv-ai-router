# CollectiVAI Router – Security Notes

This document summarises the main security assumptions and provides a
checklist for running the CollectiVAI Router in a safe way.

## 1. Secrets & API keys

- All provider API keys **must** be stored as environment variables:
  - `OPENAI_API_KEY`
  - `GEMINI_API_KEY`
  - `MISTRAL_API_KEY`
  - `META_API_KEY`
  - `DEEPSEEK_API_KEY`
- The `.env` file is only for local development and should **never** be committed.
- Do not log keys, full HTTP requests or full error messages from providers.

## 2. Router token

- The router is protected by `COLLECTIVAI_ROUTER_TOKEN`:
  - The app must send: `X-CollectivAI-Token: <token>`.
  - If the env var is set, all requests without a matching token receive `401`.
  - For development you can leave the env var empty to deactivate the check.

## 3. No dynamic custom URLs

- The router does **not** accept arbitrary URLs or hosts from the client.
- This prevents SSRF-style abuse (using the router to reach internal services).
- If you later want to connect your own models, do it via a **server-side allowlist**.

## 4. Cloudflare / Reverse Proxy

When running behind Cloudflare or another reverse proxy, you should:

- Restrict allowed HTTP methods and paths, for example:
  - `POST /api/chat`
  - `GET /health`
- Enable WAF / rules to block obvious attacks.
- Add basic rate limiting for `/api/chat` (e.g. X requests per minute per IP).

## 5. Logging

- Log only:
  - timestamps,
  - provider/model used,
  - high-level routing reasons,
  - latency and status codes.
- Avoid logging:
  - full prompts,
  - secrets,
  - full provider error payloads from external APIs.

## 6. Privacy

- The CollectiVAI App itself does not store API keys and does not send them.
- All routing happens via this backend.
- You can later add:
  - prompt anonymisation,
  - partial redaction,
  - or per-user privacy settings in the backend.

This repository is intentionally conservative: it prefers safety and clarity
over advanced features. Extend it carefully and review new features through
a security lens every time.

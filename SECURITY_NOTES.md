# CollectiVAI Router – Security Notes

This document explains security assumptions and recommendations for the
`collectiv-ai-router` project.

## 1. Secrets & API keys

- **Never** commit a real `.env` file to GitHub.
- Store **all provider API keys** (OpenAI, Gemini, Mistral, Meta, DeepSeek, …)
  in your deployment platform's secret storage (e.g. Cloudflare environment
  variables, GitHub Actions secrets, etc.).
- The file `.env.example` is only a template and MUST NOT contain real secrets.

If you accidentally pushed a real `.env` file to a public repo:

1. **Immediately rotate** all affected API keys (OpenAI, Gemini, Mistral, …).
2. Remove the file from the repo and commit history if possible.
3. Add `.env` to `.gitignore` (already present in this template).

## 2. Logging & data protection

- Be careful not to log full prompts, answers or personal data.
- Prefer structured, **minimal** logging:
  - timestamp
  - provider / model
  - latency and status
- If logs contain user data, treat them as confidential and store them securely.

## 3. CORS & origins

- Restrict `ROUTER_ALLOWED_ORIGINS` to your real frontends  
  (e.g. the CollectiVAI iOS/macOS app, website, or staging domains).
- Do **not** use `*` in production.

## 4. Rate limiting & abuse protection

In production you should add:

- basic rate limiting (per IP / per API key),
- request size limits,
- simple anomaly detection (too many errors, too many tokens, etc.).

These are not included in this minimal reference implementation.

## 5. Custom providers

The `Custom` provider is a **placeholder**.  
Only enable/implement it if you:

- control the target backend, and
- understand the security, logging and privacy implications.

By default, the example implementation simply returns an error if selected.

---
© 2025 CollectiVAI – This file is non-confidential documentation.

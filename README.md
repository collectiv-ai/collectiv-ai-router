<p align="center">
  <img src="logo.png" alt="CollectiVAI Logo" width="400" />
</p>

<h1 align="center">CollectiVAI Router</h1>
<h3 align="center">Multi-Provider AI Routing · Prototype v0.1</h3>

<p align="center">
  <a href="https://collectivai.org">
    <img src="https://img.shields.io/badge/Website-collectivai.org-003399?style=flat" alt="Website" />
  </a>
  <a href="https://github.com/collectiv-ai/collectiv-ai-app">
    <img src="https://img.shields.io/badge/App-Alpha-ffcc00?style=flat" alt="App Alpha" />
  </a>
  <a href="https://github.com/collectiv-ai/collectiv-ai-app-chain">
    <img src="https://img.shields.io/badge/Chain-Pre--Alpha-999999?style=flat" alt="Chain Pre-Alpha" />
  </a>
  <img src="https://img.shields.io/badge/Made%20in-Europe-003399?style=flat" alt="Made in Europe" />
</p>

---

> ⚠️ **Status:** Early experimental prototype – not production-ready.  
> This router is part of the technical heart of CollectiVAI and will evolve over time.

---

## What is the CollectiVAI Router?

The **CollectiVAI Router** is a small, experimental backend that:

- accepts a chat request via a simple HTTP API (`/v1/chat`),
- routes it to one of several AI backends (e.g. OpenAI, local Ollama),
- applies basic routing rules & metadata,
- and returns a unified response format.

It is meant as the **technical core** behind the CollectiVAI App and future
infrastructure – a place where:

- multi-provider routing,  
- privacy modes and  
- ethical / safety layers  

can gradually be implemented and tested.

---

## Current Scope (v0.1 – Prototype)

This first public version focuses on:

- a very small, understandable **Python / FastAPI** codebase  
- a simple `/v1/chat` endpoint  
- two provider backends (example idea):
  - `openai` (cloud)
  - `ollama` (local, running on the same machine)
- a basic routing parameter: `provider` (`auto`, `openai`, `ollama`)

No advanced safety, governance or logging yet – those will be added later,
in line with the overall CollectiVAI philosophy.

---

## Quickstart

> **Note:** Commands are written for macOS / Linux.  
> On Windows, you would use the equivalent PowerShell commands.

### 1. Clone the repository

```bash
git clone https://github.com/collectiv-ai/collectiv-ai-router.git
cd collectiv-ai-router

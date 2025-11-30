<p align="center">
  <img src="logo.png" alt="CollectiVAI Logo" width="320" />
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

## 1. What is the CollectiVAI Router?

The **CollectiVAI Router** is a small backend that powers the  
**CollectiVAI App** (iOS / iPadOS / macOS, SwiftUI).

It receives a structured request from the app (mode, provider, topic, service profile, modelId),  
decides **which AI backend to call**, and returns:

- the final **reply text**
- which **provider** and **model** were used
- optional **routing metadata** (latency, filters, reasoning)

In simple terms:

```text
CollectiVAI App  →  CollectiVAI Router  →  AI Providers (OpenAI, Gemini, Mistral, Meta, DeepSeek, local…)
           ↑                                 ↓
        Modes, topics, profiles          Reply + routingInfo

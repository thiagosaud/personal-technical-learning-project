# 🤖 Weather & Daily Dish AI Agents Case (From Scratch)

[![Python](https://img.shields.io/badge/python-%3E%3D3.12-3776AB?logo=python&logoColor=white)](pyproject.toml)
[![requests](https://img.shields.io/badge/requests-API-009688?logo=python&logoColor=white)](https://requests.readthedocs.io/)
[![scikit--learn](https://img.shields.io/badge/scikit--learn-NLP-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../../LICENSE)

Educational AI agents project implementing core agent components (perception, reasoning, memory, and action) **from scratch** using pure Python.

A practical laboratory demonstrating how autonomous agents work internally without relying on heavyweight agent frameworks 🧠

The execution pipeline routes user requests through specialized agents:

1. **Weather Agent**: Fetches real-time weather via OpenWeather API, manages local context memory, and formats natural language responses.
2. **Daily Dish Agent**: Parses restaurant PDF menus, applies TF-IDF vectorization and cosine similarity to match customer food inquiries.
3. **Router Agent**: Analyzes incoming queries and dynamically dispatches them to the appropriate specialized agent.

## ⚠️ Scope

This project is a technical and educational demonstration designed to expose the internal lifecycle of AI agents.

- The weather data relies on live responses from the OpenWeather API (requires a valid API key).
- The daily dish data relies on local restaurant documents and statistical text matching rather than conversational LLM black boxes.

## ⚙️ Requirements

See in the [PYPROJECT](pyproject.toml).

## ▶️ Usage

```bash
pnpm build
```

## 🧱 Architecture

## 📁 Structure

## 📋 Variables

## 🧪 Experiments

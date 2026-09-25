# 🤖 Weather & Daily Dish AI Agents Case (From Scratch)

[![Python](https://img.shields.io/badge/python-%3E%3D3.12-3776AB?logo=python&logoColor=white)](pyproject.toml)
[![nltk](https://img.shields.io/badge/nltk-%3E%3D3.10.3-154F3C?logo=python&logoColor=white)](https://www.nltk.org/)
[![numpy](https://img.shields.io/badge/numpy-%3E%3D2.5.2-013243?logo=numpy&logoColor=white)](https://numpy.org/)
[![pypdf](https://img.shields.io/badge/pypdf-%3E%3D6.19.0-FF5722?logo=python&logoColor=white)](https://pypdf.readthedocs.io/)
[![requests](https://img.shields.io/badge/requests-%3E%3D2.34.2-009688?logo=requests&logoColor=white)](https://requests.readthedocs.io/)
[![scikit--learn](https://img.shields.io/badge/scikit--learn-%3E%3D1.9.0-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![sentence--transformers](https://img.shields.io/badge/sentence--transformers-%3E%3D6.1.0-4B0082?logo=python&logoColor=white)](https://www.sbert.net/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](../../../../../LICENSE)

Educational AI agents project implementing core agent components (perception, reasoning, memory, and action) **from scratch** using pure Python.

A practical laboratory demonstrating how autonomous agents work internally without relying on heavyweight agent frameworks 🧠

The execution pipeline routes user requests through specialized agents:

1. **Weather Agent**: Fetches real-time weather via OpenWeather API, manages local context memory, and formats natural language responses.
2. **Daily Dish Agent**: Parses restaurant PDF menus, applies TF-IDF vectorization and cosine similarity to match customer food inquiries.
3. **Router Agent**: Analyzes incoming queries and dynamically dispatches them to the appropriate specialized agent.

---

## 🧭 Overview for Recruiters

This project is a software engineering laboratory applied to artificial intelligence, demonstrating the creation of modular **Autonomous Agents From Scratch**, using pure Python and low-level libraries, without heavy abstraction frameworks (like LangChain or LlamaIndex).

### What makes this project stand out

- **Understanding Primitives**: Instead of hiding logic behind abstractions, it explicitly implements the fundamental agent lifecycle: **Perception** (query preprocessing and normalization), **Reasoning** (dynamic intent routing and semantic matching via TF-IDF), **Memory** (conversational history + stateful key-value persistence), and **Action** (external API integrations and document parsers).
- **Production-Ready Standards**:
  - **`src`-layout architecture** with clean separation of concerns (Domain, Data, Memory, Processor, Orchestrator).
  - **Dependency Injection** for isolated testability.
  - **Strict Type-Hinting** validated by type checkers.
  - **100% Test Coverage** using `pytest` and robust mocks.
  - **Modern Dependency Management** with `uv`.

---

## ⚠️ Scope

This project is a technical and educational demonstration designed to expose the internal lifecycle of AI agents.

- The weather data relies on live responses from the OpenWeather API (requires a valid API key).
- The daily dish data relies on local restaurant documents and statistical text matching rather than conversational LLM black boxes.

---

## ⚙️ Requirements

See in the [PYPROJECT](pyproject.toml).

## ▶️ Usage

```bash
pnpm build
```

## 🧱 Architecture

The system adopts a domain-driven layered architecture, decoupling infrastructure from agent business rules:

```text
[ User Request ]
       │
       ▼
[ QueryProcessor ] ──> (Sanitization & Synonym Expansion)
       │
       ▼
[ RouterAgent ] ────> (Intent Classification)
       ├─────────────────────────────────┐
       ▼                                 ▼
[ WeatherAgent ]                 [ DailyDishAgent ]
 (OpenWeather API + Memory)       (PDF Menu Parser + TF-IDF/Cosine Similarity)
```

- Core Domain (src/core/domain/): Contains specialized agents (WeatherAgent, DailyDishAgent, RouterAgent) and the central orchestrator (ChatbotOrchestrator).
- Core Layers (src/core/layer/): Isolated infrastructure modules including the PDF loader (PdfFaqLoader), memory manager (MemoryAgent), language processor (QueryProcessor), and centralized logger (AppLogger).
- Configuration (src/app/configs/): Environment configuration and static path management.

## 📁 Structure

```text
case-weather-and-daily-dish-agents/
├── README.md                                      # Project overview, architecture, scope, usage, and technical documentation
├── pyproject.toml                                 # Python project metadata, dependencies, tooling, and configuration
├── uv.lock                                        # Deterministic lockfile for resolved Python dependencies
│
├── data/                                          # Raw dataset and static documents directory
│   └── raw/                                       # Unprocessed documents used by agents
│       └── The_Daily_Dish_FAQ.pdf                 # Restaurant menu and FAQ PDF document
│
├── tests/                                         # Automated test suite for validating application behavior
│   ├── test_app_logger.py                         # Unit tests for structured logging functionality
│   ├── test_chatbot_orchestrator.py               # Unit tests for end-to-end multi-agent orchestration
│   ├── test_daily_dish_agent.py                   # Unit tests for semantic dish matching and search
│   ├── test_memory_agent.py                       # Unit tests for conversational history and key-value state
│   ├── test_pdf_loader.py                         # Unit tests for PDF parsing, text extraction, and branch coverage
│   ├── test_query_processor.py                    # Unit tests for query sanitization and synonym expansion
│   ├── test_router_agent.py                       # Unit tests for intent classification and query dispatch
│   └── test_weather_agent.py                      # Unit tests for live weather API integration and mocks
│
└── src/                                           # Application source code and runtime components
    ├── app/                                       # Application configuration and settings
    │   └── configs/                               # Global configuration management
    │       └── settings.py                        # Environment variables and static path definitions
    │
    └── core/                                      # Core domain logic and infrastructure layers
        ├── domain/                                # Business domain agents and orchestration logic
        │   ├── agents/                            # Specialized autonomous agent implementations
        │   │   ├── router_agent.py                # Classifies incoming user intents
        │   │   ├── weather_agent.py               # Fetches real-time weather and manages context
        │   │   └── daily_dish_agent.py            # Matches food inquiries via TF-IDF and cosine similarity
        │   │
        │   └── orchestrator/                      # Central workflow orchestration
        │       └── chatbot_orchestrator.py        # Routes requests through specialized agents
        │
        └── layer/                                 # Low-level infrastructure and processing layers
            ├── data/                              # Data ingestion and parsing layer
            │   └── pdf_loader.py                  # Parses and extracts text sections from PDF documents
            ├── logging/                           # Logging and monitoring layer
            │   └── app_logger.py                  # Structured console/file logging utility
            ├── memory/                            # Persistence and memory layer
            │   └── memory_agent.py                # Dual history and stateful key-value storage
            └── processor/                         # Natural language processing layer
                └── query_processor.py             # Sanitizes queries and expands domain synonyms
```

## 📋 Variables

Supported environment variables for runtime configuration (via `.env` or direct export):

| Variable              | Description                               | Default / Example                                 |
| :-------------------- | :---------------------------------------- | :------------------------------------------------ |
| `OPENWEATHER_API_KEY` | OpenWeather API authentication key        | `your_api_key_here`                               |
| `WEATHER_API_URL`     | Weather API HTTP endpoint                 | `https://api.openweathermap.org/data/2.5/weather` |
| `FAQ_PDF_PATH`        | Local file path for menu/FAQ PDF document | `data/raw/menu_faq.pdf`                           |

## 🧪 Experiments

- **Semantic Retrieval vs. Exact Match**: Experiment comparing the robustness of cosine similarity via `scikit-learn` (TF-IDF) on restaurant menus versus traditional substring search, demonstrating higher resilience against user typos and vocabulary variations.
- **API Resilience**: Simulation of network failures and HTTP error codes in the OpenWeather API using `unittest.mock`, ensuring graceful degradation and user-friendly fallback responses without breaking the agent orchestrator pipeline.

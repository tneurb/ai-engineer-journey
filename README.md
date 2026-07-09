# AI Engineer Learning Journey

Building my way to an AI Engineer role through hands-on challenges.
Every file here is code I wrote myself, debugged, and shipped.

## Phase 1 — Python for AI + LLM APIs ✅

Five working projects built with the Anthropic Claude API:

- **API Data Merger** — calls 3 public APIs, merges results with error handling
- **Sentiment Classifier** — structured JSON output with confidence scoring
- **Invoice Extractor** — multi-language extraction including Thai Buddhist calendar
- **Multi-turn Chatbot** — conversation memory across unlimited turns
- **Customer Support Bot** — FAQ grounding, unknown question handling, JSON logging

## Stack

Python · Anthropic Claude API · FastAPI · Streamlit

## In progress

Phase 2 — RAG Pipelines + AI Agents

## Phase 2 — RAG Pipelines + AI Agents (in progress)

### RAG Chatbot over Technical Documentation

A full retrieval-augmented generation pipeline that answers questions about
a 35-page Spring Boot course document, with source transparency and
grounded refusal (says "I don't know" instead of hallucinating).

**Architecture:**

PDF → chunking → Voyage embeddings → ChromaDB → FastAPI → Gradio chat UI

**Stack:** Python · FastAPI · ChromaDB · Voyage AI embeddings · Anthropic Claude API · Gradio

**Key engineering decisions:**

- Fixed-size chunking (500 chars, 50 overlap) balances context completeness vs. specificity
- Retrieval tuned from n_results=3 to 5 after testing — more context without noticeable noise
- Explicit "answer only from context" prompting prevents hallucination — verified with an out-of-scope test question that correctly returns "I don't know"

**Run it:**

```bash
uvicorn phase2.rag_api:app --reload    # terminal 1
python phase2/gradio_app.py             # terminal 2
```

### Multi-Step Tool-Using Agent

A ReAct-pattern agent that reasons about which tools it needs, calls them,
and synthesizes results into a final answer — rather than guessing at
computations an LLM is known to get wrong.

**Tools:** calculator (real Python `eval()`), word counter

**Key engineering decisions:**

- Handles multiple simultaneous tool calls in a single turn (not just one at a time)
- Hard step limit (5 iterations) prevents infinite retry loops on tool failures
- Real tool execution instead of trusting Claude's internal math — verified
  by testing a multi-part question requiring both tools

**Run it:**

```bash
python phase2/agent.py
```

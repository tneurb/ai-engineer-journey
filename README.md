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

### Fine-Tuned Insurance Ticket Formatter (LoRA)

A LoRA fine-tuned adapter for Mistral-7B-Instruct-v0.2 that converts informal,
messy stakeholder requests into structured engineering tickets, specialized
for insurance industry workflows (claims, underwriting, billing, compliance).

**Model:** [huggingface.co/tneurb/mistral-insurance-ticket-formatter](https://huggingface.co/tneurb/mistral-insurance-ticket-formatter)

**Stack:** Mistral 7B · PEFT (LoRA) · bitsandbytes (4-bit quantization) · Google Colab T4 GPU

**Key engineering decisions:**

- LoRA (r=16, alpha=32) trains only 13.6M of 7.26B parameters (0.19%) —
  fits fine-tuning on a free GPU instead of requiring enterprise hardware
- 4-bit NF4 quantization shrinks the base model from ~14GB to ~4GB memory footprint
- Verified training actually worked with a real before/after comparison against
  the untrained base model — not just a claim, a measured result

**What the before/after comparison showed:**
Fine-tuning changed _behavior_, not _knowledge_ — the base model produced
rambling, inconsistent responses with conversational filler ("Thank you for
your attention to this matter"). The fine-tuned model consistently produced
a terse, professional Title + Description structure across every unseen test
request, directly demonstrating the difference between fine-tuning (style/behavior)
and RAG (knowledge) covered elsewhere in this repo.

**Known limitation:** trained on only 15 examples / 6 optimizer steps as a
learning exercise. The model reliably learned 2 of the intended 3 ticket
sections (Title, Description) — Acceptance Criteria did not consistently
appear, likely needing more training data or steps to fully lock in.
**Observability:** Agent instrumented with LangSmith tracing (`wrap_anthropic()`)
for full visibility into tool-use decisions, execution timing, and reasoning steps.

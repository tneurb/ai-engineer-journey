import streamlit as st
import json
import os

# ── Page setup ──────────────────────────────────────────────
st.set_page_config(page_title="AI Engineer Learning Path", layout="wide")

PROGRESS_FILE = "progress.json"

# ── Load / save progress ────────────────────────────────────
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)

progress = load_progress()

# ── Roadmap data ─────────────────────────────────────────────
roadmap = [
    {
        "id": "phase1",
        "title": "Phase 1 — Python for AI + LLM APIs",
        "months": "Months 1–2",
        "color": "#1D9E75",
        "challenges": [
            "API Data Merger — call 3 APIs, merge results",
            "Sentiment classifier — structured JSON output",
            "Invoice extractor — multi-language, multi-currency",
            "Multi-turn chatbot — conversation history",
            "Customer support bot — FAQ + logging",
        ],
    },
    {
        "id": "phase2",
        "title": "Phase 2 — RAG Pipelines + AI Agents",
        "months": "Months 2–5",
        "color": "#534AB7",
        "challenges": [
            "Embeddings from scratch — cosine similarity",
            "RAG pipeline — chatbot over any PDF",
            "Deploy RAG as FastAPI endpoint",
            "Multi-step agent — search + code execution",
        ],
    },
    {
        "id": "phase3",
        "title": "Phase 3 — Production + Evals + Fine-tuning",
        "months": "Months 5–7",
        "color": "#D85A30",
        "challenges": [
            "Add ragas eval suite to RAG chatbot",
            "Add LangSmith tracing to agent",
            "Fine-tune Mistral 7B with LoRA",
            "Dockerise and deploy one project",
        ],
    },
    {
        "id": "phase4",
        "title": "Phase 4 — ML Depth + MLOps",
        "months": "Months 7–12",
        "color": "#E5930A",
        "challenges": [
            "Text classifier in PyTorch from scratch",
            "Add MLflow experiment tracking",
            "Add DVC + GitHub Actions CI/CD",
            "Deploy model as Docker container",
        ],
    },
    {
        "id": "phase5",
        "title": "Phase 5 — Interview Prep + Job Search",
        "months": "Months 12–18",
        "color": "#0C447C",
        "challenges": [
            "NeetCode 75 — 3 problems per week",
            "Weekly ML concept explanations",
            "Polish GitHub portfolio + READMEs",
            "Apply to 5 companies per week",
        ],
    },
]

# ── Sidebar — overall progress ──────────────────────────────
total_challenges = sum(len(p["challenges"]) for p in roadmap)
completed = sum(1 for v in progress.values() if v)

with st.sidebar:
    st.title("Your progress")
    pct = completed / total_challenges if total_challenges else 0
    st.progress(pct)
    st.write(f"{completed} / {total_challenges} challenges complete")
    st.divider()
    st.caption("Progress saves automatically to progress.json")

# ── Main content ─────────────────────────────────────────────
st.title("AI Engineer & LLM Engineer Learning Path")
st.caption("Software developer track · 5–10 hrs/week · Both roles")

for phase in roadmap:
    phase_challenges = phase["challenges"]
    phase_done = sum(
        1 for i in range(len(phase_challenges))
        if progress.get(f"{phase['id']}_{i}", False)
    )

    with st.expander(
        f"**{phase['title']}**  ·  {phase['months']}  ·  {phase_done}/{len(phase_challenges)} done",
        expanded=(phase_done < len(phase_challenges) and phase["id"] == "phase1"),
    ):
        for i, challenge in enumerate(phase_challenges):
            key = f"{phase['id']}_{i}"
            checked = st.checkbox(
                challenge,
                value=progress.get(key, False),
                key=key,
            )
            if checked != progress.get(key, False):
                progress[key] = checked
                save_progress(progress)
                st.rerun()
from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
import os
import voyageai
import anthropic
from dotenv import load_dotenv

load_dotenv()
vo = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# connect to your EXISTING ChromaDB — no PDF reading, no chunking, no embedding
chroma_client = chromadb.PersistentClient(path="phase2/chroma_db")
collection = chroma_client.get_or_create_collection(name="spring_boot_notes")

app = FastAPI(title="Spring Boot RAG API")

class Question(BaseModel):
    text: str

@app.post("/ask")
def ask(q: Question):
    # YOUR JOB: move the logic from answer_question() here
    # 1. embed q.text
    # 2. query collection, n_results=5
    # 3. build the grounded prompt
    # 4. call Claude
    # 5. return {"answer": ..., "sources": retrieved_chunks}
    # 1. embed the question
    question_result = vo.embed([q.text], model="voyage-3.5")
    question_embedding = question_result.embeddings[0]

    # 2. retrieve top 3 chunks from ChromaDB
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=5
    )
    retrieved_chunks = results["documents"][0]

    # 3. build a grounded prompt
    context = "\n\n---\n\n".join(retrieved_chunks)
    prompt = f"""Answer the question using ONLY the context below.
If the answer isn't in the context, say "I don't know based on the provided document."

Context:
{context}

Question: {q.text}"""

    # 4. call Claude
    message = claude.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    return {
    "answer": message.content[0].text,
    "sources": retrieved_chunks
}

    # print(f"Question: {q}\n")
    # print (f"Answer: {message.content[0].text}\n")
    # print("--- Sources used ---")
    # for i, chunk in enumerate(retrieved_chunks, 1):
    #     print(f"[{i}] {chunk[:100]}...")
    # print("=" * 50)
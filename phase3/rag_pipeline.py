from pypdf import PdfReader
import chromadb
import os
import voyageai
from dotenv import load_dotenv
import time
import anthropic
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from datasets import Dataset
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()
vo = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

test_questions = [
    {
        "question": "What is Spring Boot?",
        "ground_truth": "Spring Boot is an extension of the Spring framework that simplifies configuration and provides auto-configuration for building production-ready applications with minimal setup."
    },
    {
        "question": "What is the difference between ApplicationRunner and CommandLineRunner?",
        "ground_truth": "Both are functional interfaces that run code just after the Spring Boot application starts. CommandLineRunner's run method takes String... args, while ApplicationRunner's run method takes an ApplicationArguments object."
    },
    {
        "question": "What is a Spring Boot Starter?",
        "ground_truth": "Spring Boot starters are dependency descriptors that bundle compatible versions of related libraries, so developers don't need to manually manage individual dependency versions."
    },
    {
        "question": "What does the Spring Boot Actuator provide?",
        "ground_truth": "Actuator provides production-ready features like health checks, metrics, and monitoring endpoints such as /health and /info, without requiring custom implementation."
    },
    {
        "question": "How do you run a Spring Boot application as a standalone JAR?",
        "ground_truth": "You package it with 'mvn clean package spring-boot:repackage' and then run the generated JAR with 'java -jar <filename>'."
    },
]

reader = PdfReader("phase2/Unit-9.pdf")
print(f"Total pages: {len(reader.pages)}")

text = ""
for page in reader.pages:
    text += page.extract_text()

print(f"Extracted {len(text)} characters")

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap  # move forward, but overlap a bit
    return chunks


chunks = chunk_text(text)
print(f"Number of chunks: {len(chunks)}")
print("--- First chunk ---")
print(chunks[0])
print("--- Second chunk ---")
print(chunks[1])
    
# Create a database that lives in a local folder
chroma_client = chromadb.PersistentClient(path="phase2/chroma_db")

# A "collection" is like a table — one collection per document/topic
collection = chroma_client.get_or_create_collection(name="spring_boot_notes")

print(collection.count())

def answer_question(question):
    question_result = vo.embed([question], model="voyage-3.5")
    question_embedding = question_result.embeddings[0]

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=5
    )
    retrieved_chunks = results["documents"][0]

    context = "\n\n---\n\n".join(retrieved_chunks)
    prompt = f"""Answer the question using ONLY the context below.
If the answer isn't in the context, say "I don't know based on the provided document."

Context:
{context}

Question: {question}"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    return {
        "answer": message.content[0].text,
        "contexts": retrieved_chunks
    }
    



eval_data = {
    "question": [],
    "answer": [],
    "contexts": [],
    "ground_truth": [],
}

for item in test_questions:
    time.sleep(21)  # respect rate limits
    result = answer_question(item["question"])
    
    eval_data["question"].append(item["question"])
    eval_data["answer"].append(result["answer"])
    eval_data["contexts"].append(result["contexts"])
    eval_data["ground_truth"].append(item["ground_truth"])
    
    print(f"Done: {item['question']}")

print(eval_data)





eval_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o-mini"))
eval_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings(model="text-embedding-3-small"))

dataset = Dataset.from_dict(eval_data)

result = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy],
    llm=eval_llm,
    embeddings=eval_embeddings,
)
print(result)

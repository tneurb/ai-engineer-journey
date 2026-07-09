from pypdf import PdfReader
import chromadb
import os
import voyageai
from dotenv import load_dotenv
import time
import anthropic



load_dotenv()
vo = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

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

#result = vo.embed(chunks, model="voyage-3.5")
#chunk_embeddings = result.embeddings

# batch_size = 20
# chunk_embeddings = []

# for i in range(0, len(chunks), batch_size):
#     batch = chunks[i:i + batch_size]
#     result = vo.embed(batch, model="voyage-3.5")
#     chunk_embeddings.extend(result.embeddings)
#     print(f"Embedded {len(chunk_embeddings)} / {len(chunks)} chunks")
#     time.sleep(20)  # stay under 3 requests per minute
    
# Create a database that lives in a local folder
chroma_client = chromadb.PersistentClient(path="phase2/chroma_db")

# A "collection" is like a table — one collection per document/topic
collection = chroma_client.get_or_create_collection(name="spring_boot_notes")

# Add chunks — ChromaDB embeds them for you automatically by default,
# OR you can pass your own Voyage embeddings (recommended, since you already have them)
# collection.add(
#     documents=chunks,                    # the text chunks
#     embeddings=chunk_embeddings,      # the Voyage vectors you already know how to create
#     ids=[f"chunk_{i}" for i in range(len(chunks))]  # unique ID per chunk
# )

print(collection.count())

def answer_question(question):
    # 1. embed the question
    question_result = vo.embed([question], model="voyage-3.5")
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

Question: {question}"""

    # 4. call Claude
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    print(f"Question: {question}\n")
    print(f"Answer: {message.content[0].text}\n")
    print("--- Sources used ---")
    for i, chunk in enumerate(retrieved_chunks, 1):
        print(f"[{i}] {chunk[:100]}...")
    print("=" * 50)
    
# answer_question("What is Spring Boot and why was it created?")
# answer_question("How do I configure Spring Security roles?")



time.sleep(5)  # small buffer to respect rate limits
answer_question("What is Spring Boot and why was it created?")

time.sleep(5)
answer_question("How do I configure Spring Security roles?")
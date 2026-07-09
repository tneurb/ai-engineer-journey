import numpy as np
import voyageai
import os
from dotenv import load_dotenv

load_dotenv()

sentences = [
    "How do I reset my password?",
    "I forgot my login credentials",
    "What is the price of the product?",
    "How much does it cost?",
    "The weather is sunny today",
    "It is a beautiful day outside",
    "Python is a great programming language",
    "I love coding in Python",
    "My order has not arrived yet",
    "Where is my delivery?",
]

query = "I need help with my account password"

def cosine_similarity(a, b):
    # fill this in using np.dot and np.linalg.norm
    return np.dot(a,b)/ (np.linalg.norm(a) * np.linalg.norm(b))

vo = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))

result = vo.embed(sentences, model="voyage-3.5")
#embedding = result.embeddings[0]  # this is your vector — a list of numbers
query_result = vo.embed([query], model="voyage-3.5")
query_embedding = query_result.embeddings[0]

scores = []
for i, sentence_embedding in enumerate(result.embeddings):
    score = cosine_similarity(sentence_embedding, query_embedding)
    scores.append((sentences[i], score))

# sort by score, highest first
scores.sort(key=lambda x: x[1], reverse=True)

print(f"Query: {query}\n")
print("Top 3 most similar:")
for sentence, score in scores[:3]:
    print(f"{sentence}   score: {score:.2f}")
    

   
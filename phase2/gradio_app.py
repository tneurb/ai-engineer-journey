import gradio as gr
import requests

def ask_api(question, history):
    response = requests.post(
        "http://localhost:8000/ask",
        json={"text": question}
    )
    data = response.json()
    return data["answer"]

gr.ChatInterface(
    ask_api,
    title="Spring Boot RAG Assistant",
    description="Ask questions about the Spring Boot course notes"
).launch()
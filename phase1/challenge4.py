import os
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

messages = []

while True:
    user_input = input("You: ")
    
    # 1. check quit here
    if user_input.lower() == "quit":
        print("Goodbye!")
        break
    
    # 2. append user message to history
    messages.append({"role": "user", "content": user_input})
    
    # 3. call Claude with full messages list
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=messages
    )
    
    # 4. get reply, print it, append to history
    reply = message.content[0].text
    print(f"Claude: {reply}")
    messages.append({"role": "assistant", "content": reply})
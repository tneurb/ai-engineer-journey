import os
import json
import datetime
import anthropic
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# 1. Read the FAQ file — fix the path to phase1/faq.txt
try:
    with open(os.path.join(os.getcwd(), 'phase1', 'faq.txt'), 'r') as file:
        faq_content = file.read()
       
except FileNotFoundError:
    print("Error: The specified file was not found.")
except json.JSONDecodeError:
    print("Error: The file contains invalid JSON syntax.")
except Exception as e:
        print(f"Unexpected error: {e}")

# 2. Build the system prompt using faq_content
system_prompt = f"""You are a support bot for TechCorp Thailand.
Answer ONLY using this FAQ. If the answer isn't here, say you don't know
and suggest contacting support@techcorp.th

FAQ:
{faq_content}"""

messages = []

while True:
    user_input = input("You: ")

    if user_input.lower() == "quit":
        print("Goodbye!")
        break

    # 3. append user message to history
    messages.append({"role": "user", "content": user_input})

    # 4. call Claude — pass system_prompt and messages
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        system=f"""You are a customer support bot for TechCorp Thailand.
                Answer questions using ONLY the information in this FAQ.
                If the question is not covered in the FAQ, say you don't know 
                and suggest contacting support@techcorp.th
                FAQ:
                {faq_content}""",
        messages=messages        
    )

    # 5. get reply, print it, append to history
    reply = message.content[0].text
    print(f"Claude: {reply}")
    messages.append({"role": "assistant", "content": reply})

    # 6. log this turn
    log_entry = {
        "role": "user",
        "content": user_input,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
        with open(os.path.join(os.getcwd(), 'phase1', 'conversation_log.json'), 'r') as f:
            log = json.load(f)
    except FileNotFoundError:
        log = []

    log.append(log_entry)
    with open(os.path.join(os.getcwd(), 'phase1', 'conversation_log.json'), 'w') as f:
        json.dump(log, f, indent=2)
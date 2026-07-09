import os
import json
import anthropic
from dotenv import load_dotenv
from pathlib import Path
import datetime


    
load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


try:
    with open(os.path.join(os.getcwd(), 'week2', 'faq.txt'), 'r') as file:
        faq_content = file.read()
       
except FileNotFoundError:
    print("Error: The specified file was not found.")
except json.JSONDecodeError:
    print("Error: The file contains invalid JSON syntax.")
except Exception as e:
        print(f"Unexpected error: {e}")
messages=[] 
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
        system=f"""You are a customer support bot for TechCorp Thailand.
                Answer questions using ONLY the information in this FAQ.
                If the question is not covered in the FAQ, say you don't know 
                and suggest contacting support@techcorp.th
                FAQ:
                {faq_content}""",
        messages=messages        
                )
    
    
    
    # 4. get reply, print it, append to history
    reply = message.content[0].text
    print(f"Claude: {reply}")
    messages.append({"role": "assistant", "content": reply})    
    # log user message
    log_entry = {
        "role": "user",
        "content": user_input,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    try:
     with open(os.path.join(os.getcwd(), 'week2', 'conversation_log.json'), 'r') as f:
        log = json.load(f)
    except FileNotFoundError:
        log = []
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit()  # ← add exit() here so script stops if faq fails to load
    if 'faq_content' not in dir():
        print("Cannot start — faq.txt not found.")
        exit()
    log.append(log_entry)
    with open(os.path.join(os.getcwd(), 'week2', 'conversation_log.json'), 'w') as f:
        json.dump(log, f, indent=2)




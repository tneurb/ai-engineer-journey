import os
import json
import anthropic
import sys


from dotenv import load_dotenv

load_dotenv()
filename = sys.argv[1] 
code=''
try:
    with open(os.path.join(os.getcwd(), filename), 'r') as file:
        code = file.read()
        
except FileNotFoundError:
    print("Error: The specified file was not found.")
except json.JSONDecodeError:
    print("Error: The file contains invalid JSON syntax.")

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": f"Review this Python code:\n\n{code}"}
    ]
)

print(message.content[0].text)
print("---")
print(f"Input tokens: {message.usage.input_tokens}")
print(f"Output tokens: {message.usage.output_tokens}")
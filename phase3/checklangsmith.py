import os
from dotenv import load_dotenv
import anthropic
from langsmith import wrappers

load_dotenv()

client = wrappers.wrap_anthropic(anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY")))

message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=100,
    messages=[{"role": "user", "content": "Say hello in one sentence."}]
)
print(message.content[0].text)
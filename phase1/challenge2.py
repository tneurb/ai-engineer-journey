import os
from dotenv import load_dotenv
import anthropic
import json

load_dotenv()  # reads the .env file

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def extract_json(text):
    text = text.strip()
    if text.startswith("```"):
        # Cut off the closing backticks
        text = text.removesuffix("```")
        # Cut off the opening backticks and the 'json' identifier line
        if text.startswith("```json"):
            text = text.removeprefix("```json")
        else:
            text = text.removeprefix("```")
            
    return text.strip()


feedbacks = [
    "This product changed my life, absolutely love it!",
    "It was okay, nothing special but got the job done.",
    "Terrible experience, never buying again. Complete waste of money."
]
for feedback in feedbacks:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": f"""
        Return ONLY a JSON object. No explanation. No markdown.
        Return with json exactly of these fields
        -sentiment: "positive" or "negative" or "neutral",
        -confidence: "high" or "medium" or "low",
        -reason: "one sentence explaining why
    {feedback}"""}]
        
    )
    text = message.content[0].text
    result = json.loads(extract_json(text))
    print(f"Sentiment: {result['sentiment']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Reason: {result['reason']}")
    print("---")




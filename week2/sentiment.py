import os
import anthropic
import json



from dotenv import load_dotenv

load_dotenv()

sentiment=''

    
feedbacks = [
    "This product changed my life, absolutely love it!",
    "It was okay, nothing special but got the job done.",
    "Terrible experience, never buying again. Complete waste of money."
]


client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def extract_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return text.strip()

for feedback in feedbacks:
    prompt = f"""You are a sentiment analyser.
Analyse the sentiment of this customer feedback:"{feedback}"
Return ONLY a JSON object with exactly these fields:
- sentiment: must be "positive", "negative", or "neutral"
- confidence: must be "high", "medium", or "low"  
- reason: one sentence explaining why
Return nothing else. No explanation. Just the JSON."""
    
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
  
    result = json.loads(extract_json(message.content[0].text))
    print(f"SENTIMENT: {result['sentiment'].upper()}")
    print("---")


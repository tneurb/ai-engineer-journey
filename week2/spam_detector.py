import os
import anthropic
import json
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

emails = [
    "Hi John, just following up on our meeting yesterday. Can we schedule a call this week?",
    "CONGRATULATIONS! You have been selected to receive a FREE iPhone 15! Click here NOW to claim your prize!!!",
    "Your Amazon order #12345 has been shipped. Expected delivery: Thursday."
]
def extract_json(txt):
    txt = txt.strip()
    if txt.startswith("```"):
        txt = txt.split("```")[1]
        if txt.startswith('json'):
            txt = txt[4:]
            
    return txt.strip()

for email in emails:
    prompt = f"""you are a spam detector Check this email {email}
    return only a json object with exactly these fields:
    -is_spam": true or false
    -confidence": "high" or "medium" or "low"
    -reason": "one sentence explaining why"
    Return nothing else. No explanation. Just the JSON.
    """
    message = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": prompt}
    ]
    )

    #print(message.content[0].text)
    result = json.loads(extract_json(message.content[0].text))
    print(email)
    print(f"is_spam: {result['is_spam']}")
    print(f"Confidence: {result['confidence']}")
    print(f"Reason: {result['reason']}")
    print("---")
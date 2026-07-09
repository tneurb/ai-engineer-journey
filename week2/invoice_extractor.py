import os
import json
import anthropic

from dotenv import load_dotenv

load_dotenv()

invoices = [
    "Invoice from Acme Corp dated March 15 2024. Total due: $1,250.00. Payment pending.",
    "ใบแจ้งหนี้จาก บริษัท ABC จำกัด วันที่ 1 เมษายน 2567 ยอดชำระ 45,000 บาท ชำระแล้ว",
    "Bill #445 - TechSupplies Ltd. Date: 22/01/2024. Amount: EUR 890.50. UNPAID.",
]

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def extract_json(text):
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    return text.strip()

for invoice in invoices:
    prompt= f"""You are an Financial analyst or Invoice Data Extractor.
    Extract these invoices:"{invoice}"
    Return ONLY a JSON object with exactly these fields:
        -vendor: "company or person name"
        -amount: 1234.56
        -currency: "USD" or "THB" or "EUR" etc
        -date: must be in "YYYY-MM-DD format using Gregorian calendar year"
        - The Thai Buddhist calendar year 2567 = Gregorian year 2024.
        วันที่ 1 เมษายน 2567 = 2024-04-01
        Always output Gregorian year in the date field.
        -status: "paid" or "unpaid" or "unknown"
    Return nothing else. No explanation. Just the JSON."""
    
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    result = json.loads(extract_json(message.content[0].text))
    print(result)
    #print(message.content[0].text)
    #print(extract_json(message.content[0].text))
    
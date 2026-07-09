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

invoices = [
    "Invoice from Acme Corp dated March 15 2024. Total due: $1,250.00. Payment pending.",
    "ใบแจ้งหนี้จาก บริษัท ABC จำกัด วันที่ 1 เมษายน 2567 ยอดชำระ 45,000 บาท ชำระแล้ว",
    "Bill #445 - TechSupplies Ltd. Date: 22/01/2024. Amount: EUR 890.50. UNPAID.",
]


for invoice in invoices:
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": f"""
        Return ONLY a JSON object. No explanation. No markdown.
        Return with json exactly of these fields
        "vendor": "company or person name",
        "amount": 1234.56,
        "currency": "USD" or "THB" or "EUR",
        "date": "YYYY-MM-DD",
        "status": "paid" or "unpaid" or "unknown"
    {invoice}"""}]
        
    )
    text = message.content[0].text
    result = json.loads(extract_json(text))
    print(result['vendor'])
    print(result['amount'])
    print(result['currency'])
    print(result['date'])
    print(result['status'])
    print("---")
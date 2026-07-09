import requests
r = requests.get("https://date.nager.at/api/v3/PublicHolidays/2025/US", timeout=5)
print(r.status_code)
print(r.text[:300])
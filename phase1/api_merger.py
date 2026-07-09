import requests

def get_person():
    # API 1
    try:
        r1 = requests.get("https://randomuser.me/api/", timeout=5)
        r1.raise_for_status()
        data1 = r1.json()
        return data1
    except requests.exceptions.ConnectionError:
        print("Could not connect — check your internet")
    except requests.exceptions.Timeout:
        print("Request took too long")
    except requests.exceptions.HTTPError as e:
        print(f"API returned an error: {e}")
    except Exception as e:
        print(f"Something went wrong: {e}")

def get_joke():
    try:
        r2 = requests.get("https://official-joke-api.appspot.com/random_joke", timeout=5)
        r2.raise_for_status()
        data2 = r2.json()
        return data2
    except requests.exceptions.ConnectionError:
        print("Could not connect — check your internet")
    except requests.exceptions.Timeout:
        print("Request took too long")
    except requests.exceptions.HTTPError as e:
        print(f"API returned an error: {e}")
    except Exception as e:
        print(f"Something went wrong: {e}")

def get_holiday():
    try:
        r3 = requests.get("https://date.nager.at/api/v3/PublicHolidays/2025/US", timeout=5)
        r3.raise_for_status()
        data3 = r3.json()
        return data3
    except requests.exceptions.ConnectionError:
        print("Could not connect — check your internet")
    except requests.exceptions.Timeout:
        print("Request took too long")
    except requests.exceptions.HTTPError as e:
        print(f"API returned an error: {e}")
    except Exception as e:
        print(f"Something went wrong: {e}")
    

# Call all three
person = get_person()
joke = get_joke()
holiday = get_holiday()

# Print combined summary
# Print combined summary
print("=== Daily Summary ===")

if person:
    first = person["results"][0]["name"]["first"]
    last = person["results"][0]["name"]["last"]
    email = person["results"][0]["email"]
    print(f"Person:   {first} {last} ({email})")
else:
    print("Person:   [unavailable]")

if joke:
    setup = joke["setup"]
    punchline = joke["punchline"]
    print(f"Joke:     {setup} {punchline}")
else:
    print("Joke:     [unavailable]")

if holiday:
    name = holiday[0]["name"]
    day = holiday[0]["date"]
    print(f"Holiday:  {name} on {day}")
else:
    print("Holiday:  [unavailable]")
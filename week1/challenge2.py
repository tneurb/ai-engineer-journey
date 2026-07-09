import json
import os
from pathlib import Path
try:
    with open(os.path.join(os.getcwd(), 'week1', 'employees.json'), 'r') as file:
        data = json.load(file)
       
        
        for employee in data:
            print(f"Name:  {employee.get('name','N/A')} | Department : {employee.get('department','N/A')} | Salary : {employee.get('salary','N/A')}")
except FileNotFoundError:
    print("Error: The specified file was not found.")
except json.JSONDecodeError:
    print("Error: The file contains invalid JSON syntax.")
except Exception as e:
        print(f"Unexpected error: {e}")


import requests
import csv
from itertools import islice

base_url = "http://localhost:8000/chat"
with open("/home/test/key.csv", "r") as f:
    reader = csv.reader(f)
    api_key = next(islice(reader, 0, 1), None)[1]

while True:
    user_input = input("请输入: ")
    if user_input.lower() == "exit":
        break
    user_message = {
        "model_name": "deepseek-flash",
        "api_key": api_key,
        "message": user_input
    }
    response = requests.post(base_url, json=user_message)
    if response.status_code == 200:
        assistant_message = response.json().get("message")
        print(assistant_message)
    else:
        print("Error:", response.status_code, response.text)
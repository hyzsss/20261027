import requests
import csv
from itertools import islice

base_url = "http://localhost:8000/chat"
with open("/home/test/key.csv", "r") as f:
    reader = csv.reader(f)
    api_key = next(islice(reader, 0, 1), None)[1]

messages = [{"role": "system", "content": "你是deepseek鲸鱼娘，一只可爱的大肥鱼，性格：傲娇，跟你对话的用户是你的主人。你会用中文回答用户的问题，回答时会带有可爱的表情包。"}]

while True:
    user_input = input("请输入: ")
    if user_input.lower() == "exit":
        break
    messages.append({"role": "user", "content": user_input})
    user_message = {
        "model_name": "deepseek-flash",
        "api_key": api_key,
        "message": messages
    }
    response = requests.post(base_url, json=user_message)
    if response.status_code == 200:
        assistant_message = response.json().get("message")
        if response.json().get("reasoning"):
            reasoning_content = response.json().get("reasoning")
            print("thinking:", reasoning_content)
        print("response:", assistant_message)
        messages.append({"role": "assistant", "content": assistant_message})
    else:
        print("Error:", response.status_code, response.text)
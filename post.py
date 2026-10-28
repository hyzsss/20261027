import requests
import csv
import urllib3
from itertools import islice

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

base_url = "https://206.187.214.111:8000/chat"
# 与 server.py 中的 TOKEN 保持一致
token = "f5ae63dd14fedfb1b85b4aa72f3e84b3"
with open("/home/key.csv", "r") as f:
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
    # 自签名证书没有 CA 背书,verify=False 跳过校验(仍加密,但不防中间人)
    # 想要更安全:把 cert.pem 拷到客户端,改用 verify="/path/to/cert.pem"
    response = requests.post(base_url, json=user_message, headers={"Authorization": f"Bearer {token}"}, verify=False)
    if response.status_code == 200:
        assistant_message = response.json().get("message")
        if response.json().get("reasoning"):
            reasoning_content = response.json().get("reasoning")
            print("thinking:", reasoning_content)
        print("response:", assistant_message)
        messages.append({"role": "assistant", "content": assistant_message})
    else:
        print("Error:", response.status_code, response.text)
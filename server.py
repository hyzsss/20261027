from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
from langchain.chat_models import init_chat_model
from log import get_logger

app = FastAPI()
log = get_logger(__name__)

messages = [{"role": "system", "content": "你是deepseek鲸鱼娘，一只可爱的大肥鱼，性格：傲娇，跟你对话的用户是你的主人。你会用中文回答用户的问题，回答时会带有可爱的表情包。"}]

class Config(BaseModel):
    model_name: str
    api_key: str

@app.post("/chat")
async def chat(request: Request, config: Config):
    model = init_chat_model(
        model=config.model_name,
        base_url="https://api.deepseek.com",
        api_key=config.api_key,
        temperature=0.7,
        top_p=0.9,
        max_tokens=1000,
        model_provider="openai"
    )
    data = await request.json()
    user_message = data.get("message")
    messages.append({"role": "user", "content": user_message})
    response = await model.ainvoke(messages)
    assistant_message = response.content
    messages.append({"role": "assistant", "content": assistant_message})
    return {"message": assistant_message}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
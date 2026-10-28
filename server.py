from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
from langchain.chat_models import init_chat_model
from log import get_logger

app = FastAPI()
log = get_logger(__name__)

class Config(BaseModel):
    model_name: str
    api_key: str

log.info("启动服务，监听端口 8000")

@app.post("/chat")
async def chat(request: Request, config: Config):
    model = init_chat_model(
        model=config.model_name,
        base_url="https://api.deepseek.com",
        api_key=config.api_key,
        # temperature=0.7,
        # top_p=0.9,
        max_tokens=1000,
        model_provider="deepseek",
        reasoning_effort="high",
        extra_body={"thinking": {"type": "enabled"}},
    )
    data = await request.json()
    log.info(f"接收到请求，调用模型 {data.get('model_name')} ")
    user_message = data.get("message")
    response = model.invoke(user_message)
    if response.content is not None:
        log.info(f"模型返回成功")
        return {"message": response.content, "reasoning": response.additional_kwargs.get("reasoning_content")}
    else:
        log.error(f"模型返回错误")
        return {"message": f"模型返回错误"}
    
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
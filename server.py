from fastapi import FastAPI, Request, Header, HTTPException
from pydantic import BaseModel
import os
import secrets
import uvicorn
from langchain.chat_models import init_chat_model
from log import get_logger

app = FastAPI()
log = get_logger(__name__)

# 访问 token:可通过环境变量 API_TOKEN 覆盖(修改后需重启服务)
TOKEN = os.getenv("API_TOKEN", "f5ae63dd14fedfb1b85b4aa72f3e84b3")


def check_token(authorization: str | None) -> bool:
    return bool(authorization) and secrets.compare_digest(authorization, f"Bearer {TOKEN}")

class Config(BaseModel):
    model_name: str
    api_key: str

log.info("启动服务，监听端口 8000")

@app.post("/chat")
async def chat(request: Request, config: Config, authorization: str | None = Header(default=None)):
    if not check_token(authorization):
        log.warning("未授权请求被拒绝")
        raise HTTPException(status_code=401, detail="无效或缺失的 token")
    try:
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
    except Exception as e:
        log.error(f"异常: {str(e)}")
        return {"message": f"发生错误，请联系管理员处理"}
    

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, ssl_certfile="cert.pem", ssl_keyfile="key.pem")
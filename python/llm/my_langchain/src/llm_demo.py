import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# 加载 .env 文件
load_dotenv()

llm = init_chat_model(
    model="claude-sonnet-4-5-20250929",
    model_provider="anthropic",
    base_url="https://globalai.vip",  # 自定义 base URL
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

if __name__ == '__main__':
    response = llm.invoke("1+1=?")
    print(response)

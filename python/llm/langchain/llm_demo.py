import os
from langchain.chat_models import init_chat_model

os.environ["ANTHROPIC_API_KEY"] = ""

llm = init_chat_model("anthropic:claude-sonnet-4-5-20250929")

if __name__ == '__main__':
    response = llm.invoke("1+1=?")
    print(response)
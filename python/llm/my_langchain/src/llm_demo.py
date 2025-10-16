from langchain.chat_models import init_chat_model

llm = init_chat_model(
    model="claude-sonnet-4-5-20250929",
    model_provider="anthropic",
    base_url="https://globalai.vip",  # 自定义 base URL
    api_key="sk-SWA3Td8L6b6nPHR5yU5zBc2lIUDGafWFbx57RJzkH4JZ77kr"
)

if __name__ == '__main__':
    response = llm.invoke("1+1=?")
    print(response)

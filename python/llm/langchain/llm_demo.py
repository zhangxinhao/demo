from langchain.chat_models import init_chat_model

llm = init_chat_model(
    model="openrouter/google/gemini-2.5-flash",
    model_provider="openai",
    base_url="http://127.0.0.1:9006",  # 自定义 base URL
    api_key="sk-IXwQuAKWK_w14UPfzv6JQQ"
)

if __name__ == '__main__':
    response = llm.invoke("1+1=?")
    print(response)

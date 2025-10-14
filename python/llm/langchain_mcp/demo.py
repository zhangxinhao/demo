import asyncio

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_mcp_adapters.client import MultiServerMCPClient

llm = init_chat_model(
    model="openrouter/google/gemini-2.5-flash",
    model_provider="openai",
    base_url="http://127.0.0.1:9006",  # 自定义 base URL
    api_key="sk-IXwQuAKWK_w14UPfzv6JQQ"
)
client = MultiServerMCPClient(
    {
        "demo": {
            "transport": "streamable_http",  # HTTP-based remote server
            # Ensure you start your weather server on port 8000
            "url": "http://127.0.0.1:9000/mcp",
        }
    }
)


async def main():
    tools = await client.get_tools()
    agent = create_agent(
        llm,
        tools
    )
    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's 777+333=?"}]}
    )

    print(math_response)
    print("==============")

    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "有几个工具?"}]}
    )

    print(weather_response)


if __name__ == '__main__':
    asyncio.run(main())

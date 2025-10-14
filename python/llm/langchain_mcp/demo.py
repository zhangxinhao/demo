from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent

client = MultiServerMCPClient(
    {
        "math": {
            "transport": "stdio",  # Local subprocess communication
            "command": "python",
            # Absolute path to your math_server.py file
            "args": ["/path/to/math_server.py"],
        },
        "weather": {
            "transport": "streamable_http",  # HTTP-based remote server
            # Ensure you start your weather server on port 8000
            "url": "http://localhost:8000/mcp",
        }
    }
)

tools = await client.get_tools()
agent = create_agent(
    "anthropic:claude-3-7-sonnet-latest",
    tools
)
math_response = await agent.ainvoke(
    {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
)
weather_response = await agent.ainvoke(
    {"messages": [{"role": "user", "content": "what is the weather in nyc?"}]}
)
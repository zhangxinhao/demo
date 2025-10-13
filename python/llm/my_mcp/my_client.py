import asyncio

from fastmcp import Client

client = Client("http://127.0.0.1:9000/mcp")


async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result)


if __name__ == '__main__':
    asyncio.run(call_tool("Ford"))

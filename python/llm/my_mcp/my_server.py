from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")


@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"


@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="0.0.0.0",  # Bind to all interfaces
        port=9000,  # Custom port
        log_level="DEBUG",  # Override global log level
    )

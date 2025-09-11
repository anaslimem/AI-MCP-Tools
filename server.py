from fastmcp import FastMCP

# Create an instance of FastMCP
mcp = FastMCP("GreetingMCP")

@mcp.tool
def greet(name: str) -> str:
    """Greet a person by name."""
    return f"Hello, {name}!"
    

if __name__ == "__main__":
    mcp.run(transport="http", host="localhost", port=8000)

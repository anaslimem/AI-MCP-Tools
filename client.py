import asyncio
from fastmcp import Client

client = Client("http://127.0.0.1:8000")

async def call_tool(query: str):
    async with client:
        result = await client.call_tool("web_search", {"query": query})
        print(result)

asyncio.run(call_tool("who is donald trump"))

import asyncio
from fastmcp import Client

client = Client("http://127.0.0.1:8000/mcp")

async def call_tool(query: str):
    async with client:
        result = await client.call_tool("web_search", {"query": query})
        if result is None:
            print("No result returned from web_search tool.")
            return
        print("=== Web Search Results ===")
        print(result)

        summary = await client.call_tool("summarize_text", {"text": result})
        if summary is None:
            print("No summary returned from summarize_text tool.")
            return
        print("\n=== Summary ===")
        print(summary)

if __name__ == "__main__":
    asyncio.run(call_tool("who is Donald Trump"))

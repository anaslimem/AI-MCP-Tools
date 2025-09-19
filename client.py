import asyncio
import re
from fastmcp import Client

client = Client("http://127.0.0.1:8000/mcp")

def extract_first_url(result):
    lines = str(result).splitlines()
    for line in lines:
        # Find the last ( ... ) in the line
        match = re.search(r'\((https?://[^\s)]+)\)', line)
        if match:
            return match.group(1)
    return None

async def call_tool(query: str):
    async with client:
        result = await client.call_tool("web_search", {"query": query})
        if result is None:
            print("No result returned from web_search tool.")
            return
        print("=== Web Search Results ===")
        print(result)

        first_url = extract_first_url(result)
        if not first_url:
            print("No URL found in web_search result.")
            return
        print(f"\nUsing first URL: {first_url}")

        output = await client.call_tool("fetch_page_content", {"url": first_url})
        if output is None:
            print("No content returned from fetch_page_content tool.")
            return
        if not isinstance(output, str):
            print("Fetched page content is not a string. Got:", type(output), "-- converting to string.")
            output = str(output)
        print("\n=== Fetched Page Content ===")
        print(output)

        summary = await client.call_tool("summarize_text", {"text": output})
        if summary is None:
            print("No summary returned from summarize_text tool.")
            return
        print("\n=== Summary ===")
        print(summary)

if __name__ == "__main__":
    asyncio.run(call_tool("What are the latest advancements in AI technology?"))

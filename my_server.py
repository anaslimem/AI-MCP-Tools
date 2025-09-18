from fastmcp import FastMCP
from dotenv import load_dotenv
from serpapi import GoogleSearch
import os
import requests

load_dotenv()  
mcp = FastMCP("MCP")

@mcp.tool
def web_search(query: str) -> str:
    """Perform a web search using Serper.dev API and return top results."""
    api_key = os.getenv("SERPER_API_KEY")  
    if not api_key:
        return "Error: SERPER_API_KEY not set."
    
    url = "https://google.serper.dev/search"
    payload = {"q": query}
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
    except Exception as e:
        return f"Error: {e}"
    
    # Extract organic results
    results = data.get("organic", [])
    if not results:
        return f"No results found. Full response: {data}"
    
    summaries = []
    for res in results[:3]:
        title = res.get("title", "No title")
        link = res.get("link", "No link")
        snippet = res.get("snippet", "")
        summaries.append(f"{title}: {snippet} ({link})")
    
    return "\n".join(summaries)


if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)

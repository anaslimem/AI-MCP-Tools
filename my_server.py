from fastmcp import FastMCP
from dotenv import load_dotenv
from serpapi import GoogleSearch
import os

load_dotenv()  # Load environment variables from .env file
# Create an instance of FastMCP
mcp = FastMCP("MCP")

@mcp.tool
def greet(name: str) -> str:
    """Greet a person by name."""
    return f"Hello, {name}!"

@mcp.tool
def web_search(query: str) -> str:
    """Perform a web search using SerpApi and return a summary of results."""
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        return "Error: SERPAPI_API_KEY environment variable not set."
    params = {
        "q": query,
        "api_key": api_key,
        "engine": "google",
        "num": 5
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    summaries = []
    for res in results.get("organic_results", [])[:3]:
        title = res.get("title", "No title")
        link = res.get("link", "No link")
        snippet = res.get("snippet", "")
        summaries.append(f"{title}: {snippet} ({link})")
    if not summaries:
        return "No results found."
    return "\n".join(summaries)
    

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)

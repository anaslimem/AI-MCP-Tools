from fastmcp import FastMCP
from dotenv import load_dotenv
import os
import requests
from langchain_google_genai import ChatGoogleGenerativeAI

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

@mcp.tool
def summarize_text(text: str) -> str:
    """Summarize the given text using Gemini."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Error: GOOGLE_API_KEY not set."
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0,
        google_api_key=api_key
    )
    prompt = f"Summarize the following text in a concise manner:\n\n{text}\n\nSummary:"
    response = llm.invoke(prompt)
    if isinstance(response.content, str):
        return response.content
    elif isinstance(response.content, list):
        return " ".join([c.get("text", "") for c in response.content if isinstance(c, dict)])
    else:
        return str(response.content)
if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8000)

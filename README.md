# AI MCP Tools

A simple implementation of an MCP (Model Context Protocol) server in Python, deployed with [FastMCP Cloud](https://anaslimem.fastmcp.app).

## What is MCP (Model Context Protocol)?

MCP is a protocol designed for connecting and serving tools, models, and functions in a unified and context-aware way. It enables the creation of smart, extensible servers that can expose custom tools (functions) for remote or local access.

## Project Overview

This project demonstrates a basic MCP server built using the [FastMCP](https://github.com/fastmcp/fastmcp) Python framework. The server is deployed and accessible publicly via FastMCP Cloud:

👉 **Live Demo:** [https://anaslimem.fastmcp.app](https://anaslimem.fastmcp.app)

### Features

- **MCP Server:** Runs with FastMCP and exposes custom tools.
- **Custom Tools:**
  - `web_search(query)`: Uses the Serper.dev API to perform Google searches and returns summarized results.
  - `fetch_page_content(url)`: Fetches and extracts the main content from a web page given its URL.
  - `summarize_text(text)`: Summarizes the given text using Gemini (Google Generative AI).
  - `save_results(topic, content)`: Saves the summarized results to a local file on the server.
- **Environment Variables:** Uses `.env` for sensitive keys such as the Serper API key.
- **Simple Client Example:** Includes a Python client script to call the server’s tools asynchronously.

### Example Usage

#### Web Search Tool

```python
result = await client.call_tool("web_search", {"query": "OpenAI"})
# Output: "Top 3 search results with titles, snippets, and links."
```

#### Fetch Page Content Tool

```python
content = await client.call_tool("fetch_page_content", {"url": "https://example.com"})
# Output: Main text content of the page as a string.
```

#### Summarize Text Tool

```python
summary = await client.call_tool("summarize_text", {"text": content})
# Output: Concise summary of the provided text.
```

## Running Locally

1. **Clone the repo:**

   ```bash
   git clone https://github.com/anaslimem/first_mcp_server.git
   cd first_mcp_server
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your `.env` file:**

   ```bash
   SERPER_API_KEY=your_serper_api_key
   GOOGLE_API_KEY=your_google_api_key
   ```

4. **Start the server:**

   ```bash
   python my_server.py
   ```

5. **Test with the included client:**

   ```bash
   python client.py
   ```

## Deployment

This server is deployed using [FastMCP Cloud](https://fastmcp.app), making it accessible online at [https://anaslimem.fastmcp.app](https://anaslimem.fastmcp.app).

---

Feel free to fork, experiment, and extend this project!

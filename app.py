import streamlit as st
import asyncio
from fastmcp import Client

st.set_page_config(page_title="AI MCP Tools", page_icon="📝", layout="wide")
st.title("AI MCP Tools ")

for key in ['web_result', 'page_content', 'summary', 'loading']:
    if key not in st.session_state:
        st.session_state[key] = None if key != 'loading' else False

def extract_text(result):
    if hasattr(result, "data"):
        return result.data
    elif isinstance(result, list):
        return " ".join(str(r) for r in result)
    else:
        return str(result)

def run_tool(tool_name, input_value, state_key):
    async def call_tool():
        st.session_state['loading'] = True
        client = Client("http://127.0.0.1:8000/mcp")
        async with client:
            try:
                result = await client.call_tool(tool_name, input_value)
                st.session_state[state_key] = extract_text(result)
            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                st.session_state['loading'] = False
    asyncio.run(call_tool())

with st.container():
    query = st.text_input("Enter your search query:", "What are the latest advancements in AI technology?")
    url = st.text_input("Enter a URL to fetch page content:", "https://example.com")
    text_to_summarize = st.text_area("Enter text to summarize:")

col_btn1, col_btn2, col_btn3 = st.columns(3)

with col_btn1:
    if st.button("Run Web Search"):
        if query.strip():
            run_tool("web_search", {"query": query}, "web_result")
        else:
            st.warning("Please enter a search query.")

with col_btn2:
    if st.button("Fetch Page Content"):
        if url.strip():
            run_tool("fetch_page_content", {"url": url}, "page_content")
        else:
            st.warning("Please enter a URL.")

with col_btn3:
    if st.button("Summarize Text"):
        if text_to_summarize.strip():
            run_tool("summarize_text", {"text": text_to_summarize}, "summary")
        else:
            st.warning("Please enter some text to summarize.")

if st.session_state['loading']:
    st.info("🕒 Running tool, please wait...")

if st.session_state['web_result']:
    with st.expander("🔍 Web Search Results", expanded=True):
        st.markdown(st.session_state['web_result'].replace("\n", "\n\n"))

if st.session_state['page_content']:
    with st.expander("🌐 Page Content", expanded=True):
        st.markdown(st.session_state['page_content'].replace("\n", "\n\n"))

if st.session_state['summary']:
    with st.expander("📝 Summary", expanded=True):
        st.markdown(st.session_state['summary'].replace("\n", "\n\n"))
        # Compose file content with topic and summary
        topic = query if 'query' in locals() else "Summary"
        file_content = f"Topic: {topic}\n\n{st.session_state['summary']}"
        st.download_button(
            label="Download Summary as .txt",
            data=file_content,
            file_name="summary.txt",
            mime="text/plain"
        )



import streamlit as st
import asyncio
from fastmcp import Client

st.set_page_config(page_title="AI Web Search & Summarizer", page_icon="📝", layout="wide")
st.title("🔎 AI Web Search & Summarizer")

for key in ['result', 'summary', 'loading']:
    if key not in st.session_state:
        st.session_state[key] = None if key != 'loading' else False

def extract_text(result):
    if hasattr(result, "data"):
        return result.data
    elif isinstance(result, list):
        return " ".join(str(r) for r in result)
    else:
        return str(result)

def run_tools(query):
    async def call_tools():
        st.session_state['loading'] = True
        client = Client("http://127.0.0.1:8000/mcp")
        async with client:
            try:
                # Web search
                web_result = await client.call_tool("web_search", {"query": query})
                st.session_state['result'] = extract_text(web_result)

                # Summarize
                summary_input = extract_text(web_result)
                summary_result = await client.call_tool("summarize_text", {"text": summary_input})

                # Ensure only the text content is returned
                st.session_state['summary'] = extract_text(summary_result)

            except Exception as e:
                st.error(f"Error: {e}")
            finally:
                st.session_state['loading'] = False

    asyncio.run(call_tools())

with st.container():
    query = st.text_input(
        "Enter your search query:",
        "What are the latest advancements in AI technology?"
    )
    if st.button("Run Search & Summarize"):
        if query.strip():
            with st.spinner("Running search and summarization, please wait..."):
                run_tools(query)
        else:
            st.warning("Please enter a query.")

if st.session_state['loading']:
    st.info("🕒 Running search and summarization, please wait...")

col1, col2 = st.columns(2)

with col1:
    if st.session_state['result']:
        with st.expander("🔍 Web Search Results", expanded=True):
            # Break lines for readability
            st.markdown(st.session_state['result'].replace("\n", "\n\n"))

with col2:
    if st.session_state['summary']:
        with st.expander("📝 Summary", expanded=True):
            # Display summary text clearly
            st.markdown(st.session_state['summary'].replace("\n", "\n\n"))

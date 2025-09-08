from fastmcp import FastMCP
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware

load_dotenv()

mcp = FastMCP(name="Notes App")

@mcp.tool()
def get_notes() -> str:
    """Get a list of notes."""
    return "No notes yet."

@mcp.tool()
def add_note(note: str) -> str:
    """Add a new note."""
    return f"Note added: {note}"

if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1",
        port=8000,
        middleware=[
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        ]
    )
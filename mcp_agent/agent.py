import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from .consts import AGENT_MODEL

load_dotenv()

GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
MCP_BASE_FOLDER = os.environ.get("MCP_BASE_FOLDER")
MCP_SERVER_SCRIPT = os.environ.get("MCP_SERVER_SCRIPT")

if not GOOGLE_MAPS_API_KEY:
    raise ValueError("GOOGLE_MAPS_API_KEY is not set in the environment")

if not MCP_BASE_FOLDER:
    raise ValueError("MCP_BASE_FOLDER is not set in the environment")

if MCP_SERVER_SCRIPT == "/path/to/your/my_adk_mcp_server.py":
    raise ValueError("MCP_SERVER_SCRIPT is not set in the environment")

filesystem_tools = MCPToolset(
    connection_params=StdioServerParameters(
        command='npx',
        args=[
            "-y",  # Argument for npx to auto-confirm install
            "@modelcontextprotocol/server-filesystem",
            os.path.abspath(MCP_BASE_FOLDER),
        ],
    ),
    # Optional: Filter which tools from the MCP server are exposed
    # tool_filter=['list_directory', 'read_file']
)

map_tools = MCPToolset(
    connection_params=StdioServerParameters(
        command='npx',
        args=[
            "-y",
            "@modelcontextprotocol/server-google-maps",
        ],
        env={
            "GOOGLE_MAPS_API_KEY": GOOGLE_MAPS_API_KEY
        }
    ),
    # You can filter for specific Maps tools if needed:
    # tool_filter=['get_directions', 'find_place_by_id']
)

mcp_server = MCPToolset(
    connection_params=StdioServerParameters(
        command='python3',  # Command to run your MCP server script
        args=[MCP_SERVER_SCRIPT],  # Argument is the path to the script
    )
    # tool_filter=['load_web_page'] # Optional: ensure only specific tools are loaded
)

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='filesystem_assistant_agent',
    instruction='You can use the filesystem tools to list files, read files, etc. Always look in the allowed directory.'
                'You can use google maps tools to find places and get directions.'
                'You can use the load_web_page tool to fetch content from a URL',
    tools=[filesystem_tools, map_tools, mcp_server],
)

#
# if __name__ == "__main__":
#     print("Running agent...")
#     root_agent = asyncio.run(create_agent())

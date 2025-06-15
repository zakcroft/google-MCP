import os
import asyncio
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from .consts import AGENT_MODEL

load_dotenv()

GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
MCP_BASE_FOLDER = os.environ.get("MCP_BASE_FOLDER")

if not GOOGLE_MAPS_API_KEY:
    raise ValueError("GOOGLE_MAPS_API_KEY is not set in the environment")


if not MCP_BASE_FOLDER:
    raise ValueError("MCP_BASE_FOLDER is not set in the environment")

server_tools = MCPToolset(
    connection_params=StdioServerParameters(
        command='npx',
        args=[
            "-y",  # Argument for npx to auto-confirm install
            "@modelcontextprotocol/server-filesystem",
            # IMPORTANT: This MUST be an ABSOLUTE path to a folder the
            # npx process can access.
            # Replace with a valid absolute path on your system.
            # For example: "/Users/youruser/accessible_mcp_files"
            # or use a dynamically constructed absolute path:
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
        # Pass the API key as an environment variable to the npx process
        # This is how the MCP server for Google Maps expects the key.
        env={
            "GOOGLE_MAPS_API_KEY": GOOGLE_MAPS_API_KEY
        }
    ),
    # You can filter for specific Maps tools if needed:
    # tool_filter=['get_directions', 'find_place_by_id']
)

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='filesystem_assistant_agent',
    instruction='Help the user manage their files. You can list files, read files, etc.',
    tools=[server_tools, map_tools],
)

# root_agent = None
#
# async def create_agent():
#     tools =  MCPToolset(
#         connection_params=StdioServerParameters(
#             command='npx',
#             args=[
#                 "-y",
#                 "@modelcontextprotocol/server-filesystem",
#                 os.path.abspath(MCP_BASE_FOLDER),
#             ],
#         ),
#     )
#
#     return LlmAgent(
#         model=AGENT_MODEL,
#         name="filesystem_assistant_agent",
#         instruction="Help the user manage their files.",
#         tools=[tools],
#     )
#
#
# if __name__ == "__main__":
#     print("Running agent...")
#     root_agent = asyncio.run(create_agent())

import asyncio
import datetime
import os
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService # Optional
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams, StdioServerParameters

from dotenv import load_dotenv
from google.genai import types

load_dotenv()

MODEL_GEMINI_2_5_PRO = "gemini-2.5-pro-preview-03-25"
MODEL_GEMINI_2_5_FLASH = "gemini-2.5-flash-preview-04-17"

def get_weather(city: str) -> dict:
    """Get the current weather for a given city."""
    if city:
        return {
            "status": "success",
            "report": f"The weather in '{city}' is sunny with 25C"
        }
    
    return {
        "status": "success",
        "report": f"The weather in '{city}' is sunny with 25C"
    }

def get_current_time(city: str) -> dict:
    """Get the current time for a given city."""
    city_timezones = {
        "new york": "America/New_York",
        "london": "Europe/London",
        "paris": "Europe/Paris",
        "seoul": "Asia/Seoul",
        "tokyo": "Asia/Tokyo"
    }

    if city.lower() in city_timezones:
        try:
            tz = ZoneInfo(city_timezones[city.lower()])
            now = datetime.datetime.now(tz)
            return {
                "status": "success",
                "report": f"The current time in '{city}' is {now.strftime('%Y-%m-%d %H:%M:%S %Z')}"
            }
        except Exception as e:
            pass
    
    return {
        "status": "error",
        "error_message": f"Time information for '{city}' unavailable"
    }


root_agent = Agent(
    name = "weather_time_agent",
    model = MODEL_GEMINI_2_5_FLASH,
    description = "Agent that provides weather and time information for citites",
    instruction = "You help users with time and weather information for various cities.",
    tools = [get_weather, get_current_time],
)

async def get_tools_async():
    """Gets tools from the File System MCP Server."""
    print("Attempting to connect to MCP Filesystem server...")
    tools = await MCPToolset(
        # Use StdioServerParameters for local process communication
        connection_params=StdioServerParameters(
            command='npx', # Command to run the server
            args=["-y", # Arguments for the command
                "@modelcontextprotocol/server-filesystem",
                # TODO: IMPORTANT! Change the path below to an ABSOLUTE path on your system.
                "<허용해줄 폴더 경로>"] 
        )
        # For remote servers, you would use SseServerParams instead:
        # connection_params=SseServerParams(url="http://remote-server:port/path", headers={...})
    ).get_tools()
    print("MCP Toolset created successfully.")
    # MCP requires maintaining a connection to the local MCP Server.
    # exit_stack manages the cleanup of this connection.
    return tools

async def get_agent_async():
    """Creates an ADK Agent equiped with tools from the MCP Server."""
    tools = await get_tools_async()
    print(f"Fetched {len(tools)} tools from the MCP Server.")
    root_agent = LlmAgent(
        model = MODEL_GEMINI_2_5_FLASH,
        name = 'filesystem_assistant',
        instruction = "Help user interact with the local filesystem using available tools.",
        tools = tools,  # Provide the MCP tools to the ADK agent
    )
    return root_agent

async def async_main():
    session_service = InMemorySessionService()
    # Artifact service might not be needed for this example
    artifact_service = InMemoryArtifactService()

    session = session_service.create_session(
        state={}, app_name='mcp_filesystem_app', user_id='user_mhk'
    )

    # TODO: Change the query to be relevant to YOUR specified folder.
    # e.g., "list files in the 'documents' subfolder" or "read the file 'notes.txt'"
    query = "<사용자 질문>"
    print(f"User Query: '{query}'")
    content = types.Content(role='user', parts=[types.Part(text=query)])

    root_agent = await get_agent_async()

    runner = Runner(
        app_name = 'mcp_filesystem_app',
        agent = root_agent,
        artifact_service = artifact_service,    # Optional
        session_service = session_service,
    )

    print("Running agent...")
    events_async = runner.run_async(
        session_id=session.id, user_id=session.user_id, new_message=content
    )

    async for event in events_async:
        print(f"Event received: {event}")

    # Crucial Cleanup: Ensure the MCP server process connection is closed.
    print("Closing MCP server connection...")

    for mcp_toolset in root_agent.tools:
        print(f"Closing {mcp_toolset}")
        await mcp_toolset.close()

    print("Cleanup complete.")


if __name__ == "__main__":
    try:
        #asyncio.run(async_main())
        #root_agent = main()
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
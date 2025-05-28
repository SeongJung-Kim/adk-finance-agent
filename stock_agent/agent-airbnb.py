# https://github.com/nikhilpurwant/google-adk-mcp/blob/main/agent-repairworld.py
# ./adk_agent_samples/mcp_agent/agent.py
import asyncio
from dotenv import load_dotenv
from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts.in_memory_artifact_service import InMemoryArtifactService # Optional
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams, StdioServerParameters
import os
import logging

logging.basicConfig(level=logging.INFO)

# Load environment variables from .env file in the parent directory
# Place this near the top, before using env vars like API keys
load_dotenv('./.env')

if os.environ.get("GOOGLE_API_KEY") == "NOT_SET":
    print("Please set a Google API Key using - https://aistudio.google.com/app/apikey")
    exit(1)

log_verbosity = os.environ.get("LOG_VERBOSITY")


# --- Step 1: Import Tools from MCP Server ---
async def get_tools_async():
    """Gets tools from the MCP Server."""
    print("Attempting to connect to the MCP server...")
    tools = await MCPToolset(
        # Use StdioServerParameters for local process communication
        connection_params=StdioServerParameters(
            command='npx', # Command to run the server
            args=["-y", # Arguments for the command
                "@openbnb/mcp-server-airbnb",
                "--ignore-robots-txt"] 
        )
        # For remote servers, you would use SseServerParams instead:
        # connection_params=SseServerParams(url="http://remote-server:port/path", headers={...})
    ).get_tools()
    print("MCP Toolset created successfully.")
    # MCP requires maintaining a connection to the local MCP Server.
    # exit_stack manages the cleanup of this connection.
    return tools

# --- Step 2: Agent Definition ---
async def get_agent_async():
    """Creates an ADK Agent equipped with tools from repairworld MCP Server."""
    # tools = await get_tools_async()
    # print(f"Fetched {len(tools)} tools from MCP server.")
    root_agent = LlmAgent(
        model = "gemini-2.5-flash-preview-04-17", # Adjust model name if needed based on availability
        name='booking_assistant',
        instruction = "You are a booking assistant for Airbnb. Help the user find the listing of the place to stay.",
        tools=[MCPToolset(
        # Use StdioServerParameters for local process communication
        connection_params=StdioServerParameters(
            command = "npx", # Command to run the server
            args=["-y", # Arguments for the command
                "@openbnb/mcp-server-airbnb",
                "--ignore-robots-txt"] 
        )
        )], # Provide the MCP tools to the ADK agent
    )
    return root_agent


def print_event(event):
    if log_verbosity == 0:
        print(f"Event received: {event}")
    elif log_verbosity == 1:
        print(f"Event from: {event.author}")
        if event.content and event.content.parts:
            if event.get_function_calls():
                print("  Type: Tool Call Request")
            elif event.get_function_responses():
                print("  Type: Tool Result")
            elif event.content.parts[0].text:
                if event.partial:
                    print("  Type: Streaming Text Chunk")
                else:
                    print("  Type: Complete Text Message")
                print(event.content.parts[0].text)                  
            else:
                print("  Type: Other Content (e.g., code result)")
        elif event.actions and (event.actions.state_delta or event.actions.artifact_delta):
            print("  Type: State/Artifact Update")
        else:
            print("  Type: Control Signal or Other")  
    else:
        if event.content.parts[0].text:
            print(event.content.parts[0].text)
             

# --- Step 3: Main Execution Logic ---
async def async_main():
    session_service = InMemorySessionService()
    # Artifact service might not be needed for this example
    artifacts_service = InMemoryArtifactService()

    session = await session_service.create_session(
        state={}, app_name='mcp_booking_app', user_id='user_booking'
    )


    root_agent = await get_agent_async()

    runner = Runner(
        app_name='mcp_booking_app',
        agent=root_agent,
        artifact_service=artifacts_service, # Optional
        session_service=session_service,
    )

    # accept and run user's query
    # e.g., "list files in the 'documents' subfolder" or "read the file 'notes.txt'"
    query = "What listings are available in Paris for 2 people on August 1st to 4th 2025?"
    #print(f"User Query: '{query}'")
    content = types.Content(role='user', parts=[types.Part(text=query)])

    print("Running agent...")
    events_async = runner.run_async(
        session_id=session.id, user_id=session.user_id, new_message=content
    )

    async for event in events_async:
        print_event(event)

    # Crucial Cleanup: Ensure the MCP server process connection is closed.
    print("Closing MCP server connection...")
    # await exit_stack.aclose()

    for mcp_toolset in root_agent.tools:
        print(f"Closing {mcp_toolset}")
        await mcp_toolset.close()

    print("Cleanup complete.")

if __name__ == '__main__':
    try:
        asyncio.run(async_main())
    except Exception as e:
        print(f"An error occurred: {e}")
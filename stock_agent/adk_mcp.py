# pip install python-dotenv google-adk

import asyncio
import os
from dotenv import load_dotenv

from google.genai import types
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.adk.agents.llm_agent import LlmAgent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner

load_dotenv()

os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

async def get_agent():
    tools = MCPToolset(
        connection_params = StdioServerParameters(
            command = "npx",
            args = [
                "-y",
                "@openbnb/mcp-server-airbnb",
                "--ignore-robots-txt"
            ]
        )
    ).get_tools()
    """
    tools, exit_stack = await MCPToolset.from_server(
        connection_params = StdioServerParameters(
            command = "npx",
            args = [
                "-y",
                "@openbnb/mcp-server-airbnb",
                "--ignore-robots-txt"
            ]
        )
    )
    """

    agent = LlmAgent(
        name = "booking_assistant",
        model = "gemini-2.5-flash-preview-04-17",
        #tools = tools,
        #tools = [tool],
        tools = [
            MCPToolset(
                connection_params = StdioServerParameters(
                    command = "npx",
                    args = [
                        "-y",
                        "@openbnb/mcp-server-airbnb",
                        "--ignore-robots-txt"
                    ]
                )
            )
        ],
        instruction = "You are a booking assistant for Airbnb. Help the user find the listing of the place to stay.",
    )

    #return agent, exit_stack
    return get_agent

async def main():
    #agent, exit_stack = await get_agent()
    agent = await get_agent()

    session_service = InMemorySessionService()

    session = await session_service.create_session(
        state = {},
        app_name = "mcp_booking_app",
        user_id = "user_booking"
    )

    query = "What listings are available in Paris for 2 people on August 1st to 4th 2025?"
    content = types.Content(role="user",
                            parts = [types.Part(text=query)])

    runner = Runner(
        app_name = "mcp_booking_app",
        agent = agent,
        session_service = session_service
    )
    response = runner.run_async(
        session_id = session.id,
        user_id = session.user_id,
        new_message = content,
    )

    print(response)
    async for message in response:
        print(message)

    #await exit_stack.aclose()
    #print("Exit stack closed")

if __name__ == "__main__":
    asyncio.run(main())
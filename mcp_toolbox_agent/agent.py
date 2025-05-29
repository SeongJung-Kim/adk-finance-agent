from google.adk.agents import Agent
from toolbox_core import ToolboxSyncClient

import os
from dotenv import load_dotenv

load_dotenv()

MODEL_GEMINI_2_5_PRO = "gemini-2.5-pro-preview-03-25"
MODEL_GEMINI_2_5_FLASH = "gemini-2.5-flash-preview-04-17"

# --- Load Tools from Toolbox ---
# TODO(developer): Ensure the Toolbox server is running at http://127.0.0.1:7000
toolbox_client = ToolboxSyncClient("http://127.0.0.1:9000")

# TODO(developer): Replace "my-toolset" with the actual ID of your toolset as configured in your MCP Toolbox server.
agent_toolset = toolbox_client.load_toolset("mhkim_bq_toolset")

# --- Define the Agent's Prompt ---
prompt = """
  You are a helpful Data Analytics Assistant and need to extract meaningful data from user questions about accommodations and call the appropriate tool.
  Answer must be generated in Korean.
"""

# --- Configure the Agent ---

#root_agent = 
root_agent = Agent(
    model = MODEL_GEMINI_2_5_FLASH,
    name = 'bq_agent',
    description = 'Answers user questions about the accommodation information.',
    instruction = prompt,
    tools = [agent_toolset],  # Pass the loaded toolset
)
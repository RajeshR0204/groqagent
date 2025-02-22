import Utilities as ut

import os
from autogen import AssistantAgent, UserProxyAgent
from pathlib import Path
from autogen.coding import LocalCommandLineCodeExecutor
import os
from autogen import AssistantAgent, UserProxyAgent

import os
import json
from pathlib import Path
from typing import Annotated
from autogen import AssistantAgent, UserProxyAgent
from autogen.coding import LocalCommandLineCodeExecutor

initdict={}
initdict = ut.get_tokens()
groq_api_key = initdict["groq_api"]



# Configure
config_list = [{
    "model": "llama-3.3-70b-versatile",
    "api_key": groq_api_key,
    "api_type": "groq"
}]


# Create a directory to store code files from code executor
work_dir = Path("coding")
work_dir.mkdir(exist_ok=True)
code_executor = LocalCommandLineCodeExecutor(work_dir=work_dir)

# Define weather tool
def get_current_weather(location, unit="fahrenheit"):
    """Get the weather for some location"""
    weather_data = {
        "berlin": {"temperature": "13"},
        "istanbul": {"temperature": "40"},
        "san francisco": {"temperature": "55"}
    }
    
    location_lower = location.lower()
    if location_lower in weather_data:
        return json.dumps({
            "location": location.title(),
            "temperature": weather_data[location_lower]["temperature"],
            "unit": unit
        })
    return json.dumps({"location": location, "temperature": "unknown"})

# Create an AI assistant that uses the weather tool
assistant = AssistantAgent(
    name="groq_assistant",
    system_message="""You are a helpful AI assistant who can:
    - Use weather information tools
    - Write Python code for data visualization
    - Analyze and explain results""",
    llm_config={"config_list": config_list}
)

# Register weather tool with the assistant
@assistant.register_for_llm(description="Weather forecast for cities.")
def weather_forecast(
    location: Annotated[str, "City name"],
    unit: Annotated[str, "Temperature unit (fahrenheit/celsius)"] = "fahrenheit"
) -> str:
    weather_details = get_current_weather(location=location, unit=unit)
    weather = json.loads(weather_details)
    return f"{weather['location']} will be {weather['temperature']} degrees {weather['unit']}"

# Create a user proxy agent that only handles code execution
user_proxy = UserProxyAgent(
    name="user_proxy",
    code_execution_config={"executor": code_executor}
)

# Start the conversation
user_proxy.initiate_chat(
    assistant,
    message="""Let's do two things:
    1. Get the weather for Berlin, Istanbul, and San Francisco
    2. Write a Python script to create a bar chart comparing their temperatures and create a file called appgraph.py to store the code in working directory"""
)

import Utilities as ut

import os
from autogen import AssistantAgent, UserProxyAgent
from pathlib import Path
from autogen.coding import LocalCommandLineCodeExecutor

initdict={}
initdict = ut.get_tokens()
groq_api_key = initdict["groq_api"]

import os
from autogen import AssistantAgent, UserProxyAgent

# Configure
config_list = [{
    "model": "llama-3.3-70b-versatile",
    "api_key": groq_api_key,
    "api_type": "groq"
}]

# Create an AI assistant
assistant = AssistantAgent(
    name="groq_assistant",
    system_message="You are a helpful AI assistant.",
    llm_config={"config_list": config_list}
)

# Create a directory to store code files
work_dir = Path("coding")
work_dir.mkdir(exist_ok=True)
code_executor = LocalCommandLineCodeExecutor(work_dir=work_dir)

# Configure the UserProxyAgent with code execution
user_proxy = UserProxyAgent(
    name="user_proxy",
    code_execution_config={"executor": code_executor}
)

# Start a conversation between the agents
user_proxy.initiate_chat(
    assistant,
    message="write a python code for Fibonacci Numbers from 1 to 100 and save the code in the working directory in a file called test.py"
)
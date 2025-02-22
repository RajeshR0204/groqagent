import Utilities as ut

import os
from autogen import AssistantAgent, UserProxyAgent

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

# Create a user proxy agent (no code execution in this example)
user_proxy = UserProxyAgent(
    name="user_proxy",
    code_execution_config=False
)

# Start a conversation between the agents
user_proxy.initiate_chat(
    assistant,
    message="What are the key benefits of using Groq for AI apps?"
)

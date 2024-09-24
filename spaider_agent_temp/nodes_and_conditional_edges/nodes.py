import json
import logging
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage, AnyMessage
from dotenv import load_dotenv

'''LOCAL IMPORTS'''
from spaider_agent_temp.schemas import State
from spaider_agent_temp.prompts.prompts import *
from spaider_agent_temp.models.chatgroq import BuildChatGroq

'''IMPORT ALL TOOLS HERE AND CREATE LIST OF TOOLS TO BE PASSED TO THE AGENT.'''
from spaider_agent_temp.tools.shell import run_batch_script
from spaider_agent_temp.tools.file_tree import get_file_tree

load_dotenv()

tools = [run_batch_script, get_file_tree]

'''LLM TO USE'''
MODEL = "llama-3.1-70b-versatile"
# MODEL = "llama-3.1-8b-instant"
# MODEL = "gemma2-9b-it"
# MODEL = "llama3-groq-70b-8192-tool-use-preview"
# MODEL = "mixtral-8x7b-32768"
llm = BuildChatGroq(model=MODEL, temperature=0)

llm_with_tools = llm.bind_tools(tools)

# WRITE FUNCTION DEFINING THE LOGIC OF EACH NODE. REFER BELOW SAMPLES FOR SYNTAX.

# Tool 1: a built-in tool node that has access to a list of nodes and can call them when asked to.
tool_node = ToolNode(tools)

# Tool 2: the FS manager AKA our tool-calling node.
def fs_manager_node(state: State):
    """
    This node creates batch-scripts and calls tools to execute them.
    """
    system_prompt = SystemMessage(FS_MANAGER_PROMPT)
    state["messages"].append(system_prompt)
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Tool 3: the reporter node, presents the information to the user. Refer to bottom of script for more on this node.
def reporter(state: State):
    """
    This function is used to talk to the user like a regular chatbot.
    """
    return {"messages": llm.invoke(state["messages"])}



# NOTE on reporter node: 
# I noticed while working on this that, when working with only a tool-calling node and tool node, the result of a query is generated and stored in the list just fine, but the message is not interpreted and read out to the user, since that would take a second llm call.

# I encountered this issue with the opensource llms a lot. You can see the result of your query if you print out the contents of the state at the end, but the message is not read out to the user.

# I fixed it back then by simply calling the llm OUTSIDE the graph a second time that looks at the final state and presents the answer to me. 

# For this project (and i suggest we continue this practice), I decided to make a dedicated reporter node that does nothing but reads the state right before the exit node is reached, and properly reads out the output to the user.


import json
import logging
from typing import Union, Literal, Any
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain.agents import initialize_agent, AgentType
from langchain_groq import ChatGroq
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, AnyMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


'''LOCAL IMPORTS'''
from spaider_agent_template.schemas import State
from spaider_agent_template.prompts import *

'''IMPORT ALL TOOLS HERE AND CREATE LIST OF TOOLS TO BE PASSED TO THE AGENT.'''
from spaider_agent_template.tools.shell import run_batch_script
from spaider_agent_template.tools.file_tree import get_file_tree

tools = [run_batch_script, get_file_tree]

'''LLM TO USE'''
MODEL = "llama-3.1-70b-versatile"
# MODEL = "llama-3.1-8b-instant"
llm = ChatGroq(model=MODEL, temperature=0)

# MODEL = "gpt-4o-mini"
# llm = ChatOpenAI(model=MODEL, temperature=0)
llm_with_tools = llm.bind_tools(tools)

# WRITE FUNCTION DEFINING THE LOGIC OF EACH NODE. REFER BELOW SAMPLES FOR SYNTAX.
tool_node = ToolNode(tools)

def fs_manager_node(state: State):
    """
    This node creates batch-scripts and calls tools to execute them.
    """
    system_prompt = SystemMessage(FS_MANAGER_PROMPT)
    state["messages"].append(system_prompt)
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

def reporter(state: State):
    """
    This function is used to talk to the user like a regular chatbot.
    """
    return {"messages": llm.invoke(state["messages"])}

def custom_tools_condition(
    state: Union[list[AnyMessage], dict[str, Any], BaseModel],
) -> Literal["tools", "reporter"]:
    """Use in the conditional_edge to route to the ToolNode if the last message

    has tool calls. Otherwise, route to the reporter node.

    Args:
        state (Union[list[AnyMessage], dict[str, Any], BaseModel]): The state to check for
            tool calls. Must have a list of messages (MessageGraph) or have the
            "messages" key (StateGraph).

    Returns:
        The next node to route to.
    """
    if isinstance(state, list):
        ai_message = state[-1]
    elif isinstance(state, dict) and (messages := state.get("messages", [])):
        ai_message = messages[-1]
    elif messages := getattr(state, "messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state to tool_edge: {state}")
    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        return "tools"
    return "reporter"


# Define the conditional edge that determines whether to continue or not
# def should_continue(state: State):
#     messages = state["messages"]
#     last_message = messages[-1]
#     # If there is no function call, then we finish
#     if not last_message.tool_calls:
#         return "end"
#     # Otherwise if there is, we continue
#     else:
#         return "continue"
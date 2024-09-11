# import the LLM you want to use.
from spaider_agent_template.models import build_oai_llm

import json
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import ToolMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain.agents import initialize_agent, AgentType

'''LOCAL IMPORTS'''
from spaider_agent_template.schemas import State
from spaider_agent_template.prompts import *

'''IMPORT ALL TOOLS HERE AND CREATE LIST OF TOOLS TO BE PASSED TO THE AGENT.'''
from spaider_agent_template.tools.shell import run_batch_script_tool
from spaider_agent_template.tools.file_tree import get_file_tree_tool

tools = [get_file_tree_tool, run_batch_script_tool]

'''LLM TO USE'''
llm = build_oai_llm()
llm_with_tools = llm.bind_tools(tools)

'''WRITE FUNCTION DEFINING THE LOGIC OF EACH NODE. REFER BELOW SAMPLES FOR SYNTAX.'''
# tool node: the node that does all the tool calling.
tools_by_name = {tool.name: tool for tool in tools}

def tool_node(state: State):
    outputs = []
    for tool_call in state['messages'][-1].tool_calls:
        tool_result = tools_by_name[tool_call["name"]].invoke(
            tool_call["args"]
        )
        outputs.append(
            ToolMessage(
                content=json.dumps(tool_result),
                name=tool_call["name"],
                tool_call_id=tool_call["id"],
            )
        )
    return {"messages": outputs}

# fs_manager_node: the node that calls the model for our task.
def fs_manager_node(state: State, config: RunnableConfig):
    system_prompt = SystemMessage(FS_MANAGER_PROMPT)
    response = llm_with_tools.invoke([system_prompt] + state['messages'], config)
    return {"messages": [response]}



# Define the conditional edge that determines whether to continue or not
def should_continue(state: State):
    messages = state["messages"]
    last_message = messages[-1]
    # If there is no function call, then we finish
    if not last_message.tool_calls:
        return "end"
    # Otherwise if there is, we continue
    else:
        return "continue"
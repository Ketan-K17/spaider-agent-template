from langgraph.graph import StateGraph, END, START
from langgraph.constants import END
from typing import TypedDict, Annotated, List, Dict, Any
from langchain_core.messages import HumanMessage, AIMessage
# from langgraph.prebuilt import tools_condition

import subprocess
from dotenv import load_dotenv

'''LOCAL IMPORTS'''
from spaider_agent_template.nodes_and_cond_edges import fs_manager_node, custom_tools_condition, tool_node, reporter
from spaider_agent_template.tools import *
from spaider_agent_template.schemas import State


load_dotenv()

def create_graph():
    # GRAPH INSTANCE
    builder = StateGraph(State)

    # LIST OF NODES TO THE GRAPH
    builder.add_node("fs_manager", fs_manager_node)
    builder.add_node("tools", tool_node)
    builder.add_node("reporter", reporter)

    # ADD EDGES/CONDITIONAL EDGES FOR THE GRAPH
    builder.add_edge(START, "fs_manager")
    builder.add_conditional_edges(
    "fs_manager",
    custom_tools_condition,
    )   
    builder.add_edge("tools", "fs_manager")
    builder.add_edge("reporter", END)

    return builder

def compile_graph(builder):
    '''COMPILE GRAPH'''
    graph = builder.compile()
    return graph

# Helper function for formatting the stream nicely
def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


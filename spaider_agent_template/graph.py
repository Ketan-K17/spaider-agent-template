from langgraph.graph import StateGraph, END
from langgraph.constants import END
from typing import TypedDict, Annotated, List, Dict, Any
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import ToolNode
import subprocess
from dotenv import load_dotenv

'''LOCAL IMPORTS'''
from spaider_agent_template.nodes_and_cond_edges import *
from spaider_agent_template.tools import *
from spaider_agent_template.schemas import State


load_dotenv()

'''GRAPH INSTANCE'''
builder = StateGraph(State)

'''LIST OF NODES TO THE GRAPH'''
builder.add_node("fs_manager", fs_manager_node)
builder.add_node("tools", tool_node)

'''SET AN ENTRY POINT FOR THE GRAPH'''
builder.set_entry_point("fs_manager")


'''ADD EDGES/CONDITIONAL EDGES FOR THE GRAPH'''
'''SYNTAX FOR CONDITIONAL EDGES, COPY THIS.'''
builder.add_conditional_edges("fs_manager", should_continue, {"continue": "tools", "end": END})

'''SYNTAX FOR REGULAR EDGES, COPY THIS.'''
builder.add_edge("tools", "fs_manager")

'''COMPILE GRAPH'''
graph = builder.compile()
    
# Helper function for formatting the stream nicely
def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

inputs = {"messages": [("user", "in the same file of the same folder, add the text 'India is my country.'")]}
print_stream(graph.stream(inputs, stream_mode="values"))
    
# # Create a thread configuration
# thread = {"configurable": {"thread_id": "1"}}
# task = input("User >>")
# for s in graph.stream(
#     {
#         'task': task,
#         'current_directory_path': (subprocess.run("pwd", shell=True, check=True, text=True, capture_output=True)).stdout
#     },
#     thread
# ):
#     for key, value in s.items():
#         print(f"{key}:")
#         if isinstance(value, dict):
#             for sub_key, sub_value in value.items():
#                 print(f"  {sub_key}:")
#                 print(f"    {sub_value}")
#                 print()
#         else:
#             print(value)
#         print()
        
   
    


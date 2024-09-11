from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List, Dict, Any
from spaider_agent_template.nodes_and_cond_edges import *
from spaider_agent_template.tools import *
from spaider_agent_template.schemas import AgentState
import sqlite3
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.prebuilt import ToolNode
import subprocess
from dotenv import load_dotenv

load_dotenv()

# Use a context manager for the SqliteSaver
with SqliteSaver.from_conn_string(":memory:") as memory:

    '''GRAPH INSTANCE'''
    builder = StateGraph(AgentState)

    '''LIST OF NODES TO THE GRAPH'''
    builder.add_node("fs_manager", fs_manager_node)
    builder.add_node("query", query_node)

    '''SET AN ENTRY POINT FOR THE GRAPH'''
    builder.set_entry_point("query")


    '''ADD EDGES/CONDITIONAL EDGES FOR THE GRAPH'''
    '''SYNTAX FOR CONDITIONAL EDGES, COPY THIS.'''
    # builder.add_conditional_edges(
    #     "generate", 
    #     should_continue, 
    #     {END: END, "reflect": "reflect"}
    # )

    '''SYNTAX FOR REGULAR EDGES, COPY THIS.'''
    builder.add_edge("query", "fs_manager")
    builder.add_edge("fs_manager", "query")
    # builder.add_edge("node1name", "node2name")
    # builder.add_edge("fs_manager", "fs_manager") # edge from fs_manager to itself, essentially looping its function.

    graph = builder.compile(checkpointer=memory)
        
        
    # Create a thread configuration
    thread = {"configurable": {"thread_id": "1"}}
    task = input("User >>")
    for s in graph.stream(
        {
            'task': task,
            'current_directory_path': (subprocess.run("pwd", shell=True, check=True, text=True, capture_output=True)).stdout
        },
        thread
    ):
        for key, value in s.items():
            print(f"{key}:")
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    print(f"  {sub_key}:")
                    print(f"    {sub_value}")
                    print()
            else:
                print(value)
            print()
        
    # # Main execution loop
    # while True:
    #     task = input("User >> ")
    #     state = {
    #         'task': task,
    #         'current_directory': '/',  # Set an initial directory
    #         'file_tree': '',
    #         'recent_actions': [],
    #         'error_messages': [],
    #     }

    #     for s in graph.stream(state):
    #         if s.get('changes'):
    #             print("Assistant:", s['changes'])
            
    #         if s == END:
    #             print("Goodbye!")
    #             exit(0)

    #     print()  # Add a blank line for readability between interactions
    


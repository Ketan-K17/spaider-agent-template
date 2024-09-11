from langchain_core.pydantic_v1 import BaseModel
from typing import TypedDict, List
from langgraph.graph import MessagesState


'''AGENTSTATE IS THE MODE OF TRANSFER OF DATA BETWEEN NODES. WE'LL CHANGE IT ACCORDING TO WHAT OUR GRAPH NEEDS.'''
class AgentState(MessagesState):
    task: str # file mgmt task given by user.
    changes: str # description of changes made to the file system.
    current_directory_path: str # current directory path.

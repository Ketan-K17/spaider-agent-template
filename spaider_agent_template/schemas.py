from langchain_core.pydantic_v1 import BaseModel
from typing import TypedDict, List
from langchain_core.pydantic_v1 import BaseModel


'''AGENTSTATE IS THE MODE OF TRANSFER OF DATA BETWEEN NODES. WE'LL CHANGE IT ACCORDING TO WHAT OUR GRAPH NEEDS.'''
class AgentState(TypedDict):
    task: str
    changes: str
    current_directory_path: str
    file_tree: str
    recent_actions: List[str]
    error_messages: List[str]

    def update_current_directory(self, new_directory: str):
        self['current_directory'] = new_directory
        self['recent_actions'].append(f"Changed directory to {new_directory}")

    def log_error(self, error_message: str):
        self['error_messages'].append(error_message)


class Queries(BaseModel):
    queries: List[str]
import os
from typing import Annotated
from typing_extensions import TypedDict
import langchain
from langchain_community.llms import HuggingFaceHub
from langchain_huggingface import HuggingFaceEndpoint
from langchain.schema import HumanMessage, SystemMessage
# from langchain_community.tools import YourChosenTool
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from dotenv import load_dotenv

from tools.shell import run_batch_script_tool
from tools.file_tree import get_file_tree_tool

load_dotenv()

llm = HuggingFaceHub(
    repo_id="llama3-groq-8b-8192-tool-use-preview",
    task="text-generation",
    model_kwargs={
        "max_new_tokens": 2000,
        "top_k": 30,
        "temperature": 0.1,
        "repetition_penalty": 1.03,
    },
)

messages = [
    SystemMessage(content="You're a helpful assistant equipped with necessary tools. Provide accurate technical answers."),
    HumanMessage(content="Answer my query using the available tools with accurate and factual response."),
]

chat_model = ChatHuggingFace(llm=llm)

tools = [run_batch_script_tool, get_file_tree_tool]

class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)
llm_with_tools = chat_model.bind_tools(tools)

def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)
tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")
graph_builder.set_entry_point("chatbot")
graph = graph_builder.compile()


while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            if isinstance(value["messages"][-1], BaseMessage):
                print("Assistant:", value["messages"][-1].content)

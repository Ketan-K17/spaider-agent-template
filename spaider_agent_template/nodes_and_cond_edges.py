# import the LLM you want to use.
from spaider_agent_template.models import build_oai_llm

from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage, ChatMessage
from spaider_agent_template.prompts import *
from spaider_agent_template.schemas import AgentState
from langchain.agents import initialize_agent, AgentType

'''IMPORT ALL TOOLS HERE'''
from spaider_agent_template.tools.shell import run_batch_script_tool
from spaider_agent_template.tools.file_tree import get_file_tree_tool

'''llm to use'''
llm = build_oai_llm()

'''WRITE FUNCTION DEFINING THE LOGIC OF EACH NODE. REFER BELOW SAMPLES FOR SYNTAX.'''
def fs_manager_node(state: AgentState):
    tools = [get_file_tree_tool, run_batch_script_tool]
    
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    messages = [
        SystemMessage(content=FS_MANAGER_PROMPT),
        HumanMessage(content=state['task'])
    ]
    
    response = agent.run(messages)
    return {
        "changes": response,
        "current_directory": state.get('current_directory', '/'),
        "file_tree": state.get('file_tree', ''),
        "recent_actions": state.get('recent_actions', []) + [state['task']],
        "error_messages": state.get('error_messages', [])
    }

def query_node(state: AgentState):
    if state['task'].lower() == 'exit':
        return END
    return "file_system_manager"

def should_continue(state):
    if state.get('task', '').lower() == 'exit':
        return END
    return "query"

# def plan_node(state: AgentState):
#     messages = [
#         SystemMessage(content=PLAN_PROMPT), 
#         HumanMessage(content=state['task'])
#     ]
#     response = llm.invoke(messages)
#     return {"plan": response.content}

# def research_plan_node(state: AgentState):
#     queries = llm.with_structured_output(Queries).invoke([
#         SystemMessage(content=RESEARCH_PLAN_PROMPT),
#         HumanMessage(content=state['task'])
#     ])
#     content = state['content'] or []
#     for q in queries.queries:
#         response = search_tool.search(query=q, max_results=2)
#         for r in response['results']:
#             content.append(r['content'])
#     return {"content": content}

# def generation_node(state: AgentState):
#     content = "\n\n".join(state['content'] or [])
#     user_message = HumanMessage(
#         content=f"{state['task']}\n\nHere is my plan:\n\n{state['plan']}")
#     messages = [
#         SystemMessage(
#             content=WRITER_PROMPT.format(content=content)
#         ),
#         user_message
#         ]
#     response = llm.invoke(messages)
#     return {
#         "draft": response.content, 
#         "revision_number": state.get("revision_number", 1) + 1
#     }

# def reflection_node(state: AgentState):
#     messages = [
#         SystemMessage(content=REFLECTION_PROMPT), 
#         HumanMessage(content=state['draft'])
#     ]
#     response = llm.invoke(messages)
#     return {"critique": response.content}


# def research_critique_node(state: AgentState):
#     queries = llm.with_structured_output(Queries).invoke([
#         SystemMessage(content=RESEARCH_CRITIQUE_PROMPT),
#         HumanMessage(content=state['critique'])
#     ])
#     content = state['content'] or []
#     for q in queries.queries:
#         response = search_tool.search(query=q, max_results=2)
#         for r in response['results']:
#             content.append(r['content'])
#     return {"content": content}


# '''INPUT APPROPRIATE LOGIC TO TERMINATE THE GRAPH'''
# def should_continue(state):
#     if state["revision_number"] > state["max_revisions"]:
#         return END
#     return "reflect"
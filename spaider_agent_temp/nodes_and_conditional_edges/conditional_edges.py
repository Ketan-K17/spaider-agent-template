from typing import Union, Literal, Any
from langchain_core.messages import SystemMessage, AnyMessage
from pydantic import BaseModel
# from langgraph.prebuilt import tools_condition


# Tools_condition that sets the logic of the conditional edge from FS_manager to reporter or the tools node.
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

# NOTE on custom_tools_condition:
# there's a built-in function called 'tools_condition' (import stmt: from langgraph.prebuilt import tools_condition) that routes between the END node and the TOOLS-NODE. I modified that defn to route between reporter and tools.


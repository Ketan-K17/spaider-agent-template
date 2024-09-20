from spaider_agent_template.graph import create_graph, compile_graph, print_stream
from langchain_core.messages import SystemMessage, HumanMessage
from spaider_agent_template.prompts import FS_MANAGER_PROMPT
from langchain_core.runnables.config import RunnableConfig



config = RunnableConfig(recursion_limit=10)
print(config)

# Define a new graph
# workflow = StateGraph(AgentState)
# app = workflow.compile()
# app.invoke(inputs, config)


if __name__ == "__main__":
    verbose = True
    builder = create_graph()
    graph = compile_graph(builder)
        
    while True:
        user_input = input("############# User: ")
        print_stream(graph.stream({"messages": [("system", FS_MANAGER_PROMPT), ("user", user_input)]}, stream_mode="values", config=config))
        # messages = [SystemMessage(FS_MANAGER_PROMPT), HumanMessage(user_input)]

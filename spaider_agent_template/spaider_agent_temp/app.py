from langchain_core.runnables.config import RunnableConfig


# LOCAL IMPORTS.
from spaider_agent_temp.graph import create_graph, compile_graph, print_stream
from spaider_agent_temp.prompts.prompts import FS_MANAGER_PROMPT



config = RunnableConfig(recursion_limit=10)
print(config)

if __name__ == "__main__":
    # creating graph workflow instance and then compiling it.
    verbose = True
    builder = create_graph()
    graph = compile_graph(builder)
    # FS_MANAGER_PROMPT = FS_MANAGER_PROMPT.format(root_folder="C:\\Users\\ketan\\Desktop\\SPAIDER-SPACE\\spaider_agent_template\\testfolder")

    # print the mermaid diagram of the graph.
    # print(graph.get_graph().draw_mermaid())
    
    # infinite loop to take user input and print the output stream.
    while True:
        if 'root_folder' not in locals():
            root_folder = input("Enter the root folder path: ")
            FS_MANAGER_PROMPT = FS_MANAGER_PROMPT.format(root_folder=root_folder)
        user_input = input("############# User: ")
        print_stream(graph.stream({"messages": [("system", FS_MANAGER_PROMPT), ("user", user_input)]}, stream_mode="values", config=config))

from IPython.display import Image, display
from spaider_agent_template.graph import graph

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass
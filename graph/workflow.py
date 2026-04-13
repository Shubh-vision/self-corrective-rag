from langgraph.graph import StateGraph, START, END
from core.state import GraphState
from core.decision import eval_decision
from core.node import *

workflow = StateGraph(GraphState)

# ✅ Define nodes
workflow.add_node("retrieve", retrieve)
workflow.add_node("web_search", web_search)
workflow.add_node("generate", generate)
workflow.add_node("evaluate", evaluate)
workflow.add_node("rewrite", rewrite)


# ✅ Start Routing
workflow.add_conditional_edges(
    START,
    route,
    {
        "vectorstore": "retrieve",
        "web_search": "web_search"
    }
)

# ✅ Main Flow
workflow.add_edge("retrieve", "generate")
workflow.add_edge("web_search", "generate")
workflow.add_edge("generate", "evaluate")

# ✅ Evaluation Decision (FINAL STEP)
workflow.add_conditional_edges(
    "evaluate",
    eval_decision,
    {
        "rewrite": "rewrite",
        "generate": "generate",
        "human": END   # 🔥 IMPORTANT FIX
    }
)

# ✅ Rewrite Loop
# workflow.add_edge("rewrite", "retrieve")

# ✅ Compile
app = workflow.compile()
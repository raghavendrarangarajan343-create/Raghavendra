from langgraph.graph import StateGraph, END
from agents.state import CompanyIntelligenceState
from agents.nodes import research_node, consolidation_node, validation_node, save_node

def should_save(state: CompanyIntelligenceState):
    """Conditional edge logic after validation."""
    errors = state.get("validation_errors", [])
    retries = state.get("retry_count", 0)
    
    if not errors:
        return "save"
    elif retries < 3:
        print(f"--- REGENERATION LOOP Triggered (Retry {retries}/3) ---")
        return "consolidate"
    else:
        print("--- MAX RETRIES REACHED. ABORTING. ---")
        return "end"

def build_graph():
    """Builds and compiles the LangGraph."""
    workflow = StateGraph(CompanyIntelligenceState)
    
    # Add nodes
    workflow.add_node("research", research_node)
    workflow.add_node("consolidate", consolidation_node)
    workflow.add_node("validate", validation_node)
    workflow.add_node("save", save_node)
    
    # Add edges
    workflow.set_entry_point("research")
    workflow.add_edge("research", "consolidate")
    workflow.add_edge("consolidate", "validate")
    
    # Conditional edge from validate
    workflow.add_conditional_edges(
        "validate",
        should_save,
        {
            "save": "save",
            "consolidate": "consolidate",
            "end": END
        }
    )
    
    workflow.add_edge("save", END)
    
    return workflow.compile()

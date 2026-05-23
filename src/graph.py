from langgraph.graph import StateGraph, END

from src.state import AgentState
from src.agents import researcher_node, verifier_node

RESEARCHER = "researcher"
VERIFIER = "verifier"


def should_continue(state: AgentState) -> str:
    """Route back to researcher if score is below threshold, otherwise end."""
    if state.get("verification_score", 0.0) < 0.8:
        return RESEARCHER
    return END


def build_graph() -> StateGraph:
    workflow = StateGraph(AgentState)

    workflow.add_node(RESEARCHER, researcher_node)
    workflow.add_node(VERIFIER, verifier_node)

    workflow.set_entry_point(RESEARCHER)

    # Researcher always hands off to verifier
    workflow.add_edge(RESEARCHER, VERIFIER)

    # Verifier either loops back or ends
    workflow.add_conditional_edges(
        VERIFIER,
        should_continue,
        {
            RESEARCHER: RESEARCHER,
            END: END,
        },
    )

    return workflow


# Compiled graph exported as `app`
app = build_graph().compile()

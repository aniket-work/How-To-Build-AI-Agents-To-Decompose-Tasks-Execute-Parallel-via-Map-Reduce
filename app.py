from dotenv import load_dotenv
import os
from langgraph.graph import StateGraph, START, END
from langgraph.constants import Send
from state import OverallState
from constants import NodeTypes
from graph_nodes import GraphNodes


def build_graph():
    nodes = GraphNodes()
    graph = StateGraph(OverallState)

    # Add nodes
    graph.add_node(NodeTypes.GENERATE, nodes.generate_solutions)
    graph.add_node(NodeTypes.EVALUATE, nodes.evaluate_solution)
    graph.add_node(NodeTypes.DEEPEN, nodes.deepen_thought)
    graph.add_node(NodeTypes.RANK, nodes.rank_solutions)

    # Add edges
    def continue_to_evaluation(state: OverallState):
        return [Send(NodeTypes.EVALUATE, {"solution": s}) for s in state.get("solutions", [])]

    def continue_to_deep_thought(state: OverallState):
        return [Send(NodeTypes.DEEPEN, {"solution": r}) for r in state.get("reviews", [])]

    graph.add_edge(START, NodeTypes.GENERATE)
    graph.add_conditional_edges(NodeTypes.GENERATE, continue_to_evaluation, [NodeTypes.EVALUATE])
    graph.add_conditional_edges(NodeTypes.EVALUATE, continue_to_deep_thought, [NodeTypes.DEEPEN])
    graph.add_edge(NodeTypes.DEEPEN, NodeTypes.RANK)
    graph.add_edge(NodeTypes.RANK, END)

    return graph.compile()


if __name__ == "__main__":
    # Set your Groq API key

    # Load environment variables at the start of your app
    load_dotenv()

    # Now you can access the API key from anywhere using:
    api_key = os.getenv('GROQ_API_KEY')

    # Verify the API key is loaded
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")


    app = build_graph()

    test_input = {
        "input": "xxxxx",
        "considerations": "xxxx"
    }

    try:
        for s in app.stream(test_input):
            print("\nOutput:", s)
    except Exception as e:
        print(f"Error during execution: {str(e)}")
        import traceback

        print(traceback.format_exc())
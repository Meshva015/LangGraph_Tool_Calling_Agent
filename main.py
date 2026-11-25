
from typing import Literal

from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from llm import llm_with_tools
from tools import tools

MAX_TOOL_CALLS = 5

# DEFINE AGENT STATE

class AgentState(MessagesState):
    total_tool_calls: int


# DEFINE LLM NODE

def llm_node(state: AgentState):

    print("\n[LLM NODE] Thinking...")

    response = llm_with_tools.invoke(state["messages"])

    requested_calls = response.tool_calls

    previous_calls = state.get("total_tool_calls", 0)

    remaining_calls = MAX_TOOL_CALLS - previous_calls

    if len(requested_calls) > remaining_calls:
        allowed_calls = requested_calls[:remaining_calls]

        response = response.model_copy(
            update={"tool_calls": allowed_calls}
        )

    actual_calls = len(response.tool_calls)

    print("[LLM NODE] Tool calls requested:", actual_calls)

    return {
        "messages": [response],
        "total_tool_calls": previous_calls + actual_calls
    }

# DEFINE CUSTOM ROUTER

def custom_router(
    state: AgentState
) -> Literal["tools", "limit_reached", "__end__"]:

    last_message = state["messages"][-1]

    total_calls = state.get("total_tool_calls", 0)

    if last_message.tool_calls:

        if total_calls >= MAX_TOOL_CALLS:
            return "limit_reached"

        return "tools"

    return END

# DEFINE TOOL NODE

tool_node = ToolNode(tools)

# DEFINE LIMIT NODE

def limit_reached(state: AgentState):

    print("\n[AGENT] Maximum tool-call limit reached.")

    return {
        "messages": [
            AIMessage(
                content=(
                    "I reached the maximum limit of "
                    "5 tool calls. I cannot execute "
                    "additional tools for this request."
                )
            )
        ]
    }

# BUILD GRAPH

def build_graph(router=custom_router):

    workflow = StateGraph(AgentState)

    workflow.add_node("llm", llm_node)
    workflow.add_node("tools", tool_node)
    workflow.add_node("limit_reached", limit_reached)

    workflow.add_edge(START, "llm")

    workflow.add_conditional_edges(
        "llm",
        router,
        {
            "tools": "tools",
            "limit_reached": "limit_reached",
            END: END
        }
    )

    workflow.add_edge("tools", "llm")

    workflow.add_edge("limit_reached", END)

    return workflow.compile()

# CREATE AGENT

agent = build_graph(router=tools_condition)

# GRAPH VISUALIZATION

print("\n--- GRAPH STRUCTURE ---")

print(agent.get_graph().draw_mermaid())


# RUN AGENT WITH STREAMING

def run_agent(question: str):

    print("\n--- USER QUESTION ---")
    print(question)

    initial_state = {
        "messages": [HumanMessage(content=question)],
        "total_tool_calls": 0
    }

    config = {
        "recursion_limit": 20
    }

    print("\n--- AGENT EXECUTION ---")

    final_state = None

    for state in agent.stream(
        initial_state,
        config=config,
        stream_mode="values"
    ):

        final_state = state

        last_message = state["messages"][-1]

        print("\nLatest message:")
        print("Type:", type(last_message).__name__)

        if last_message.content:
            print("Content:", last_message.content)

        if getattr(last_message, "tool_calls", None):
            print("Tool calls:", last_message.tool_calls)

    print("\n--- FINAL CONVERSATION ---")

    for message in final_state["messages"]:

        print("\nMessage type:", type(message).__name__)
        print("Content:", message.content)

        if getattr(message, "tool_calls", None):
            print("Tool calls:", message.tool_calls)

        if getattr(message, "tool_call_id", None):
            print("Tool call ID:", message.tool_call_id)

    print("\nTotal tool calls:",
          final_state.get("total_tool_calls", 0))

# TEST SCENARIOS

if __name__ == "__main__":

    # Multi-tool execution
    question = """
    Find the capital of India.
    Calculate 150 multiplied by 20.
    Then increase the calculated result by 10%.
    """

    # Failed-tool recovery
    # question = "Find the capital of Mars."

    run_agent(question)


    
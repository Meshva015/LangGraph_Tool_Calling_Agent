# LangGraph Tool-Calling Agent

## 1. Project Overview

I developed a custom ReAct-style tool-calling agent using LangGraph without using `create_react_agent`.

The agent uses a Groq LLM to decide when tools are required, executes the tools, and returns the results to the LLM until a final answer is generated.

## 2. Technologies Used

- Python
- LangGraph
- LangChain
- Groq LLM

## 3. Tools Implemented

1. Calculator – Performs basic mathematical operations.
2. Percentage Calculator – Calculates percentage increase and decrease.
3. Information Lookup – Retrieves information from a local knowledge base.

## 4. Graph Architecture

The graph contains:

- START
- LLM Node
- Conditional Router
- ToolNode
- END

The LLM requests a tool when required. ToolNode executes it and sends the result back to the LLM. This cycle continues until the LLM generates a final response.

## 5. Design Choices

| Component | Purpose |
|---|---|
| MessagesState | Stores conversation history |
| add_messages | Appends messages without overwriting |
| bind_tools() | Provides tool definitions to the LLM |
| ToolNode | Executes requested tools |
| Custom Router | Controls graph routing |
| tools_condition | Provides built-in routing |
| recursion_limit | Controls graph execution steps |
| stream() | Displays intermediate execution steps |

## 6. Error Handling

Tools return readable error messages for invalid operations and unavailable information. This allows the LLM to receive the error and generate an appropriate response.

## 7. Loop Control

A custom counter limits tool calls to five. The recursion limit provides an additional safeguard against excessive graph execution.

## 8. Custom vs Prebuilt Agent

The custom implementation exposes the state, nodes, routing, and execution loop.

The prebuilt agent provides a convenient implementation of the standard ReAct workflow with less manual configuration.

## 9. Conclusion

This project helped me understand LangGraph state management, tool calling, conditional routing, reducers, graph cycles, error handling, and agent execution.


# TEST :1

## question = "Calculate 100 divided by 0."

->(.venv) PS D:\SS\Jupyter_ML\LangGraph_Tool_Calling_Agent> python main.py
Groq LLM connected successfully!
Available tools:
- calculator
- information_lookup
- percentage_calculator

--- GRAPH STRUCTURE ---
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        llm(llm)
        tools(tools<hr/><small><em>__tools = calculator, information_lookup, percentage_calculator</em></small>)
        limit_reached(limit_reached)
        __end__([<p>__end__</p>]):::last
        __start__ --> llm;
        llm -.-> __end__;
        llm -.-> limit_reached;
        llm -.-> tools;
        tools --> llm;
        limit_reached --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc


--- USER QUESTION ---
Calculate 100 divided by 0.

--- AGENT EXECUTION ---

Latest message:
Type: HumanMessage
Content: Calculate 100 divided by 0.

[LLM NODE] Thinking...
[LLM NODE] Tool calls requested: 0

Latest message:
Type: AIMessage
Content: Dividing any non‑zero number by 0 is undefined in ordinary arithmetic. In other words, \(100 ÷ 0\) does not have a finite, well‑defined result. If you need to work with limits or a different mathematical framework (e.g., extended real numbers), the expression would be considered to “tend toward infinity,” but in standard arithmetic it is simply undefined.

--- FINAL CONVERSATION ---

Message type: HumanMessage
Content: Calculate 100 divided by 0.

Message type: AIMessage
Content: Dividing any non‑zero number by 0 is undefined in ordinary arithmetic. In other words, \(100 ÷ 0\) does not have a finite, well‑defined result. If you need to work with limits or a different mathematical framework (e.g., extended real numbers), the expression would be considered to “tend toward infinity,” but in standard arithmetic it is simply undefined.

Total tool calls: 0

# TEST :2
## question = "Find the capital of Mars."

(.venv) PS Dpython main.pyL\LangGraph_Tool_Calling_Agent> 
Groq LLM connected successfully!
Available tools:
- calculator
- information_lookup
- percentage_calculator

--- GRAPH STRUCTURE ---
---
config:
  flowchart:
    curve: linear
---
graph TD;
        __start__([<p>__start__</p>]):::first
        llm(llm)
        tools(tools<hr/><small><em>__tools = calculator, information_lookup, percentage_calculator</em></small>)
        limit_reached(limit_reached)
        __end__([<p>__end__</p>]):::last
        __start__ --> llm;
        llm -.-> __end__;
        llm -.-> limit_reached;
        llm -.-> tools;
        tools --> llm;
        limit_reached --> __end__;
        classDef default fill:#f2f0ff,line-height:1.2
        classDef first fill-opacity:0
        classDef last fill:#bfb6fc


--- USER QUESTION ---
Find the capital of Mars.

--- AGENT EXECUTION ---

Latest message:
Type: HumanMessage
Content: Find the capital of Mars.

[LLM NODE] Thinking...
[LLM NODE] Tool calls requested: 0

Latest message:
Type: AIMessage
Content: Mars doesn’t have an official capital—after all, it’s a planet, not a nation. As of today there’s no sovereign government or recognized political structure on Mars, so there’s no capital city in the real‑world sense.

That said, the idea of a “capital of Mars” pops up in science‑fiction and speculative discussions about future colonies. Some writers and futurists have imagined places like:

- **New Olympus** – a fictional city often cited in stories set on the Martian Olympus Mons region.  
- **Mars City** – a generic name used in various proposals for the first permanent human settlement.  
- **Elysium** – sometimes referenced as a hub for a Martian colony in novels and games.

In the real world, space agencies are planning potential landing and habitat sites (e.g., near the equatorial region of **Elysium Planitia** or the **Gale Crater**), but none of these have been designated as a capital. If humanity eventually establishes a political entity on Mars, the “capital” will be decided by whatever governance structure emerges at that time.

--- FINAL CONVERSATION ---

Message type: HumanMessage
Content: Find the capital of Mars.

Message type: AIMessage
Content: Mars doesn’t have an official capital—after all, it’s a planet, not a nation. As of today there’s no sovereign government or recognized political structure on Mars, so there’s no capital city in the real‑world sense.

That said, the idea of a “capital of Mars” pops up in science‑fiction and speculative discussions about future colonies. Some writers and futurists have imagined places like:

- **New Olympus** – a fictional city often cited in stories set on the Martian Olympus Mons region.  
- **Mars City** – a generic name used in various proposals for the first permanent human settlement.  
- **Elysium** – sometimes referenced as a hub for a Martian colony in novels and games.

In the real world, space agencies are planning potential landing and habitat sites (e.g., near the equatorial region of **Elysium Planitia** or the **Gale Crater**), but none of these have been designated as a capital. If humanity eventually establishes a political entity on Mars, the “capital” will be decided by whatever governance structure emerges at that time.

Total tool calls: 0

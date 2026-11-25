
from langchain.tools import tool

@tool
def calculator(a: float, b: float, operation: str) -> str:
    """
    Perform basic mathematical operations.

    Args:
        a: First number.
        b: Second number.
        operation: add, subtract, multiply, or divide.
    """
    try:
        if operation == "add":
            result = a + b

        elif operation == "subtract":
            result = a - b

        elif operation == "multiply":
            result = a * b

        elif operation == "divide":
            if b == 0:
                return "ERROR: Division by zero is not allowed."
            result = a / b

        else:
            return f"ERROR: Unsupported operation: {operation}"

        return f"Calculation result: {result}"

    except Exception as e:
        return f"ERROR: Calculator failed: {str(e)}"

@tool
def percentage_calculator(
    value: float,
    percentage: float,
    operation: str
) -> str:
    """
    Calculate percentage increase or decrease.

    Args:
        value: Original number.
        percentage: Percentage to increase or decrease.
        operation: increase or decrease.
    """
    try:
        amount = value * percentage / 100

        if operation == "increase":
            result = value + amount

        elif operation == "decrease":
            result = value - amount

        else:
            return f"ERROR: Unsupported operation: {operation}"

        return f"Final result: {result}"

    except Exception as e:
        return f"ERROR: Percentage calculation failed: {str(e)}"

@tool
def information_lookup(query: str) -> str:
    """
    Look up basic information from the available knowledge base.

    Args:
        query: The information the user wants to find.
    """
    knowledge_base = {
        "india": "The capital of India is New Delhi.",
        "france": "The capital of France is Paris.",
        "japan": "The capital of Japan is Tokyo.",
        "python": "Python is a high-level programming language.",
        "langgraph": "LangGraph is a framework for building stateful,multi-step AI agent workflows."
    }

    try:
        query_lower = query.lower()

        for key, information in knowledge_base.items():
            if key in query_lower:
                return information

        return (
            f"ERROR: No information found for '{query}'. "
            "The requested information is not available "
            "in the current knowledge base."
        )

    except Exception as e:
        return f"ERROR: Information lookup failed: {str(e)}"

tools = [
    calculator,
    information_lookup,
    percentage_calculator
]
from llm import llm_with_tools

question = "Calculate 150 multiplied by 20 using the calculator tool."

response = llm_with_tools.invoke(question)

print("\n---LLM Response ---")

print(response)

print("\n---Tool Callls---")

print(response.tool_calls)

if response.tool_calls:

    for tool_call in response.tool_calls:
        print("\nTool name:",tool_call["name"])
        print("Arguments:",tool_call["args"])
        print("Tool Call ID:",tool_call["id"])

    else:
        print("the LLM did not request any tools.")
        
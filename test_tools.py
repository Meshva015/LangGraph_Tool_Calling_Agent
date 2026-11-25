
from tools import (
    calculator,
    percentage_calculator,
    information_lookup
)

print("\n--- CALCULATOR TEST ---")

result = calculator.invoke({
    "a": 150,
    "b": 20,
    "operation": "multiply"
})

print(result)

print("\n--- PERCENTAGE TEST ---")

result = percentage_calculator.invoke({
    "value": 3000,
    "percentage": 10,
    "operation": "increase"
})

print(result)

print("\n--- INFORMATION LOOKUP TEST ---")

result = information_lookup.invoke({
    "query": "India"
})

print(result)

print("\n--- FAILED TOOL TEST ---")

result = calculator.invoke({
    "a": 100,
    "b": 0,
    "operation": "divide"
})

print(result)
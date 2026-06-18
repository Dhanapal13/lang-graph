from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class MyState(TypedDict):
    text: str
    char_count: int

def my_node_1(state: MyState) -> dict:
    updated = state["text"] + " Hello "
    print(f"my_node_1: {state['text']} -> Updated {updated}")
    return {"text": updated}

def my_node_2(state: MyState) -> dict:
    updated = state["text"] + "Langgraph!! "
    print(f"my_node_2: {state['text']} -> Updated {updated}")
    return {"text": updated}

def my_node_3(state: MyState) -> dict:
    count = len(state["text"])
    print(f"my_node_3: counted {count}")
    return {"char_count": count}

builder = StateGraph(MyState)

builder.add_node("node_1",my_node_1)
builder.add_node("node_2",my_node_2)
builder.add_node("node_3",my_node_3)

# Connect nodes

builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", "node_3")
builder.add_edge("node_3", END)

graph = builder.compile()

initial_state: MyState = { "text": "Started", "char_count": 0}

result = graph.invoke(initial_state)
print(f"Final State: ", result)


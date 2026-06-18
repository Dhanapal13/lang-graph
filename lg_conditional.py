# A graph reads keywrods and call nodes based on sentiment

from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Literal

class SentimentState(TypedDict):
    text: str
    sentiment: str
    response: str

def analysis_sentiment(state: SentimentState) -> dict:
    """In real system - make LLM call and get sentiments"""
    text = state["text"].lower()
    sentiment = None
    if any(w for w in text.split() if w in ["great", "love", "good"]):
        sentiment = "Positive"
    elif any(w for w in text.split() if w in ["bad", "poor", "terrible"]):
        sentiment = "Negative"
    else:
        sentiment ="Neutral"

    print(f"Sentiment {sentiment}")
    return {
        "sentiment": sentiment
    }

def positive_sentiment(state: SentimentState) -> dict:
    print("Positive sentiment received")
    return {
        "response": "Thank you for good feedback"
    }

def negative_sentiment(state: SentimentState) -> dict:
    print("Negative sentiment received")
    return {
        "response": "Let us know what went wrong!"
    }

def neutral_sentiment(state: SentimentState) -> dict:
    print("Neutral sentiment received")
    return {
        "response": "Got it. Any suggestion!!"
    }

def sentiment_handler(state: SentimentState) -> Literal["positive_sentiment", "negative_sentiment", "neutral_sentiment"]:
    if state["sentiment"] == "Positive":
        return "positive_sentiment"
    if state["sentiment"] == "Negative":
        return "negative_sentiment"
    if state["sentiment"] == "Neutral":
        return "neutral_sentiment"
    

builder = StateGraph(SentimentState)

builder.add_node("analysis", analysis_sentiment)
builder.add_node("positive", positive_sentiment)
builder.add_node("negative", negative_sentiment)
builder.add_node("neutral", neutral_sentiment)

builder.add_edge(START, "analysis")
builder.add_conditional_edges("analysis", sentiment_handler, {
    "positive_sentiment": "positive",
    "negative_sentiment" : "negative",
    "neutral_sentiment" : "neutral",
})
builder.add_edge("positive", END)
builder.add_edge("negative", END)
builder.add_edge("neutral", END)

graph = builder.compile()
result = graph.invoke({
    "text": "Good Play...", "response": "", "sentiment":""
})
print(result["response"])


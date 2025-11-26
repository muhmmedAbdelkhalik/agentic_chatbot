from typing import Annotated
from typing_extensions import TypedDict, List
from langgraph.graph.message import add_messages


class State(TypedDict):
    """
    State for the graph
    - messages: Annotated list of messages with add_messages function
    """
    messages: Annotated[List, add_messages]


from langchain_community.tools import TavilySearchResults
from langgraph.prebuilt import ToolNode


def get_tools():
    """
    Return the tools to be used in chatbot
    """
    tools = [TavilySearchResults(max_results=2)]
    return tools


def create_tool_node(tools):
    """
    Create a tool node for the graph
    """
    return ToolNode(tools=tools)

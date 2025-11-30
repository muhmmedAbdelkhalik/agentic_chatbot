from langgraph.graph import StateGraph
from langgraph.prebuilt import tools_condition
from src.langgraph_agentic_ai.nodes.tool_chatbot_node import ToolChatbotNode
from src.langgraph_agentic_ai.state.state import State
from langgraph.graph import START, END
from src.langgraph_agentic_ai.nodes.basic_chatbot_node import BasicChatbotNode
from src.langgraph_agentic_ai.tools.search_tool import get_tools, create_tool_node
from src.langgraph_agentic_ai.nodes.ai_news_node import AINewsNode


class GraphBuilder:
    def __init__(self, llm_model: str):
        self.llm_model = llm_model
        self.graph_builder = StateGraph(State)

    def basic_chatbot_build_graph(self):
        """
        Build the graph for the agentic AI for Basic Chatbot
        """
        # Define basic chatbot node
        self.basic_chatbot_node = BasicChatbotNode(self.llm_model)

        # Add nodes
        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.run)

        # Defin direct edges
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

        return self.graph_builder

    def tools_chatbot_build_graph(self):
        """
        Build the graph for the agentic AI for Tools Chatbot
        """
        # Define tool
        tools = get_tools()
        tool_node = create_tool_node(tools)

        # Define llm
        llm = self.llm_model

        # Define chatbot node
        chatbot_node = ToolChatbotNode(llm).run(tools)

        # Add nodes
        self.graph_builder.add_node("chatbot", chatbot_node)
        self.graph_builder.add_node("tools", tool_node)

        # Defin conditional and direct edges
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")
        self.graph_builder.add_edge("chatbot", END)
        return self.graph_builder


    def news_chatbot_build_graph(self):
        """
        Build the graph for the agentic AI for News Chatbot
        """

        # Add nodes
        news_node = AINewsNode(self.llm_model)


        self.graph_builder.add_node("news", news_node.fetch_news)
        self.graph_builder.add_node("summarize", news_node.summarize_news)
        self.graph_builder.add_node("result", news_node.save_result)

        # Define direct edges
        self.graph_builder.set_entry_point("news") # Set the entry point to the news node (Same to START)
        self.graph_builder.add_edge("news", "summarize")
        self.graph_builder.add_edge("summarize", "result")
        self.graph_builder.add_edge("result", END)
        return self.graph_builder

    def setup_graph(self, usecase: str):
        """
        Setup the graph based on the use case
        """
        if usecase == "Basic":
            self.basic_chatbot_build_graph()
        elif usecase == "Tools":
            self.tools_chatbot_build_graph()
        elif usecase == "News":
            self.news_chatbot_build_graph()
        else:
            raise ValueError(f"Error: No use case selected: {usecase}")
        return self.graph_builder.compile()

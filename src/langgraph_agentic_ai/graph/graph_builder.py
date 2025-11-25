from langgraph.graph import StateGraph
from src.langgraph_agentic_ai.state.state import State
from langgraph.graph import START, END
from src.langgraph_agentic_ai.nodes.basic_chatbot_node import BasicChatbotNode

class GraphBuilder:
    def __init__(self, llm_model: str):
        self.llm_model = llm_model
        self.graph_builder = StateGraph(State)
    
    def basic_chatbot_build_graph(self):
        """
        Build the graph for the agentic AI for Basic Chatbot
        """

        self.basic_chatbot_node = BasicChatbotNode(self.llm_model)
        
        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.run)
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

        return self.graph_builder
from src.langgraph_agentic_ai.state.state import State


class BasicChatbotNode:
    def __init__(self, llm_model: str):
        self.llm_model = llm_model

    def run(self, state: State) -> dict:
        """
        Process the user input and generate the response
        """
        return {"messages": self.llm_model.invoke(state["messages"])}

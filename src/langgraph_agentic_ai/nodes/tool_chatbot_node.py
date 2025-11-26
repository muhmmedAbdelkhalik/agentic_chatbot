from src.langgraph_agentic_ai.state.state import State


class ToolChatbotNode:
    def __init__(self, llm_model: str):
        self.llm_model = llm_model

    # def run(self, state: State) -> dict:
    #     """
    #     Process the user input and generate the response with tools
    #     """
    #     user_input = state["messages"][-1] if state["messages"] else ""
    #     llm_response = self.llm_model.invoke(
    #         [{"role": "user", "content": user_input}])

    #     tools_response = f"Tools integration: {user_input}"

    #     return {"messages": [llm_response, tools_response]}

    def run(self, tools):
        """
        Create a chatbot node for the graph
        """
        llm_with_tools = self.llm_model.bind_tools(tools)

        def chatbot_node(state: State):
            return {"messages": llm_with_tools.invoke(state["messages"])}
        return chatbot_node

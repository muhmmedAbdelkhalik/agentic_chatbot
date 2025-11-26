import streamlit as st

from langgraph.graph import StateGraph
from src.langgraph_agentic_ai.state.state import State


class DisplayResultStreamlit:
    def __init__(self, usecase: str, graph: StateGraph, user_message: str):
        self.usecase = usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        if self.usecase == "Basic":
            self.display_basic_chatbot_result_on_ui()
        else:
            raise ValueError(f"Error: No use case selected: {self.usecase}")

    def display_basic_chatbot_result_on_ui(self):
        graph = self.graph
        user_message = self.user_message
        for event in graph.stream({"messages": ("user", user_message)}):
            print("event", event)
            for value in event.values():
                print(user_message)
                with st.chat_message("user"):
                    st.write(user_message)
                print(value['messages'].content)
                with st.chat_message("assistant"):
                    st.write(value['messages'].content)

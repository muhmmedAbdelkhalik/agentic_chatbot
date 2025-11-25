import os
import streamlit as st
from langchain_groq import Groq

class GroqLLM:
    def __init__(self, user_controls: dict):
        self.user_controls = user_controls

    def get_llm_model(self):
        try:
            groq_api_key= self.user_controls["GROQ_API_KEY"]
            selected_groq_model= self.user_controls["selected_groq_model"]
            if not groq_api_key:
                st.error("Groq API key is required")
                return None
            if not selected_groq_model:
                st.error("Groq model is required")
                return None
            llm = Groq(api_key=groq_api_key, model=selected_groq_model)
            return llm
        except Exception as e:
            st.error(f"Error getting Groq LLM model: {e}")
            return None
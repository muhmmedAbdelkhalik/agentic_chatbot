from configparser import ConfigParser

class Config:
    def __init__(self, config_file: str = "src/langgraph_agentic_ai/config/default.ini"):
        self.config = ConfigParser()
        self.config.read(config_file)

    def get(self, section: str, option: str):
        return self.config.get(section, option)

    def get_project_name(self):
        return self.get('DEFAULT', 'PROJECT_NAME')

    def get_page_title(self):
        return self.get('DEFAULT', 'PAGE_TITLE')

    def get_llm_options(self):
        llm_options = self.get('DEFAULT', 'LLM_OPTIONS')
        return [opt.strip() for opt in llm_options.split(",")]

    def get_usecase_options(self):
        usecase_options = self.get('DEFAULT', 'USECASE_OPTIONS')
        return [opt.strip() for opt in usecase_options.split(",")]

    def get_groq_model_options(self):
        groq_model_options = self.get('DEFAULT', 'GROQ_MODEL_OPTIONS')
        return [opt.strip() for opt in groq_model_options.split(",")]
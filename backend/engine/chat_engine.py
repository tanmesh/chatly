from langchain_openai import ChatOpenAI

class ChatEngine:
    def __init__(self, model, tools):
        llm = ChatOpenAI(model=model)
        self.llm = llm.bind_tools(tools)

    # Rest of the class code...
    def set_model(self, model):
        self.llm_with_tools = ChatOpenAI(model=model).bind_tools(self.llm.tools)

    def add_tool(self, tool):
        self.llm = self.llm_with_tools.bind_tools([tool])

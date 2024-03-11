from langchain_openai import ChatOpenAI


class ChatEngine:
    """
    A class representing a chat engine using the LangChain OpenAI interface.

    Attributes:
        llm (ChatOpenAI): The LangChain OpenAI interface with bound tools.
    """

    def __init__(self, model, tools):
        """
        Initializes the ChatEngine with a model and a set of tools.

        Args:
            model (str): The name or ID of the language model to be used.
            tools (list): A list of tools to be bound to the LangChain OpenAI interface.
        """
        llm = ChatOpenAI(model=model)
        self.llm = llm.bind_tools(tools)

    def set_model(self, model):
        """
        Sets a new language model for the ChatEngine and rebinds existing tools.

        Args:
            model (str): The name or ID of the new language model.
        """
        self.llm_with_tools = ChatOpenAI(model=model).bind_tools(self.llm.tools)

    def add_tool(self, tool):
        """
        Adds a new tool to the ChatEngine and rebinds existing tools.

        Args:
            tool: The tool to be added to the ChatEngine.
        """
        self.llm = self.llm_with_tools.bind_tools([tool])

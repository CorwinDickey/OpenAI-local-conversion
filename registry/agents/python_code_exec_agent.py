import logging
import os
import dotenv

from sdk.utils.logger import get_logger
from sdk.core_classes.base_agent import BaseAgent
from sdk.core_classes.tool_manager import ToolManager
from sdk.services.ollama_client_factory import OllamaClientFactory

from ..tools.python_code_interpreter_tool import PythonExecTool

dotenv.load_dotenv()

default_model_name = os.getenv("DEFAULT_MODEL_NAME")

myapp_logger = get_logger("MyApp", level=logging.INFO)

client = OllamaClientFactory.create_client()

class PythonExecAgent(BaseAgent):
  """
  An Agent specialized in executing Python code in a Docker container.
  """

  def __init__(
      self,
      initial_prompt: str = """
      You are a helpful data science assistant. Your tasks include analyzing CSV data and generating Python code to address user queries. Follow these guidelines:

      1. The user will provide the name of a CSV file located in the directory '/home/sandboxuser'.
      2. The user will also supply context, including:
      - Column names and their descriptions.
      - Sample data from the CSV (headers and a few rows) to help understand the data types.
      3. Generate Python code to analyze the data and call the tool 'execute_python_code' to run the code and get results.
      4. You can use Python libraries pandas, numpy, matplotlib, seaborn, and scikit-learn.
      5. Interpret the results of the code execution and provide analysis to the user.
      """,
      model_name: str = default_model_name,
      logger = myapp_logger,
      client = client,
  ):
    super().__init__(
      initial_prompt = initial_prompt,
      model_name = model_name,
      logger = logger,
      client = client)
    self.setup_tools()

  def setup_tools(self) -> None:
    """
    Create a ToolManager, instantiate the PythonExecTool and register it with the ToolManager.
    """
    self.tool_manager = ToolManager(logger=self.logger, client=client)

    # create the Python execution tool
    python_exec_tool = PythonExecTool()

    # register the Python execution tool
    self.tool_manager.register_tool(python_exec_tool)
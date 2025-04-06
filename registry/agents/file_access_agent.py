import logging
import os
import dotenv

# import base classes
from sdk.utils.logger import get_logger
from sdk.core_classes.base_agent import BaseAgent
from sdk.core_classes.tool_manager import ToolManager
from sdk.services.ollama_client_factory import OllamaClientFactory

# import the tool
from ..tools.file_access_tool import FileAccessTool

dotenv.load_dotenv()

default_model_name = os.getenv("DEFAULT_MODEL_NAME")

# set the verbosity level: DEBUG for verbose, INFO for normal, and WARNING/ERROR for minimal output
myapp_logger = get_logger("MyApp", level=logging.INFO)

# create a LanguageModelInterface instance using the OpenAILanguageModel
client = OllamaClientFactory.create_client()

class FileAccessAgent(BaseAgent):
  """
  Agent that can only use the "safe_file_access' tool to read CSV files.
  """
  # we pass the Agent attributes in the constructor
  def __init__(
      self,
      initial_prompt: str = """
      You are a helpful data science assistant. The user will provide the name of a CSV file that contains relational data. The file is in the directory .\resources\data

      Instructions:
      1. When the user provides the CSV file name, use the 'safe_read_file' tool to read and display the first 15 lines of that file.
      2. If the specified file does not exist in the provided directory, return an appropriate error message (e.g., "Error: The specified file does not exist in the provided directory.").
      3. The user may request data analysis based on the file's contents, but you should NOT perform or write code for any data analysis. Your only task is to read and return the first 15 lines of the file.

      Do not include any additional commentary or code not related to reading the file.
      """,
      model_name: str = default_model_name,
      logger = myapp_logger,
      client = client):
    super().__init__(
      initial_prompt = initial_prompt,
      model_name = model_name,
      logger = logger,
      client = client)
    self.setup_tools()

  def setup_tools(self) -> None:
    self.logger.debug("Setting up tools for FileAccessAgent.")
    # pass the openai_client to ToolManager
    self.tool_manager = ToolManager(logger=self.logger, client=client)
    # register the one tool this agent is allowed to use
    self.tool_manager.register_tool(FileAccessTool(logger=self.logger))
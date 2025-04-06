from typing import Dict, Any
import pandas as pd
import os

from sdk.utils.logger import get_logger
from sdk.core_classes.tool_interface import ToolInterface
from docker.docker_worker import DockerWorker

class FileAccessTool(ToolInterface):
  """
  A tool to read CSV files and copy them to a Docker container.
  """

  def __init__(self, logger = None):
    self.logger = logger or get_logger(self.__class__.__name__)

  def get_definition(self) -> Dict[str, Any]:
    self.logger.debug("Returning tool definition for safe_file_access")
    return {
      "function": {
        "name": "safe_file_access",
        "description": (
          "Read the contents of a file in a secure manner "
          "and transfer it to the Python code interpreter docker container"
        ),
        "parameters": {
          "type": "object",
          "properties": {
            "filename": {
              "type": "string",
              "description": "Name of the file to read"
            }
          },
          "required": ["filename"]
        }
      }
    }
  
  def run(self, arguments: Dict[str, Any]) -> str:
    filename = arguments["filename"]
    self.logger.debug(f"Running safe_file_access with filename: {filename}")

    return self.safe_file_access(filename)
  
  def safe_file_access(self, filename: str) -> str:
    if not filename.endswith('.csv'):
      error_msg = "Error: The file is not a CSV file."
      self.logger.warning(f"{error_msg} - Filename provided: {filename}")
      return error_msg
    
    # ensure the path is correct
    if not os.path.dirname(filename):
      filename = os.path.join('./data', filename)

    self.logger.debug(f"Attempting to read file at path: {filename}")
    try:
      df = pd.read_csv(filename)
      self.logger.debug(f"File '{filename}' loaded successfully.")
      dw = DockerWorker()
      copy_output = dw.copy_file_to_container(local_file_name=filename)
      head_str = df.head(15).to_string()
      return f"{copy_output}\nThe file content for the first 15 rows is:\n{head_str}"
    except FileNotFoundError:
      error_msg = f"Error: the file '{filename}' was not found."
      self.logger.error(error_msg)
      return error_msg
    except Exception as e:
      error_msg = f"Error while reading the CSV file: {str(e)}"
      self.logger.error(error_msg, exc_info=True)
      return error_msg

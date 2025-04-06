import subprocess
import os
import dotenv

from sdk.utils.logger import get_logger

dotenv.load_dotenv()

default_sandbox_name = os.getenv("DEFAULT_SANDBOX_CONTAINER_NAME")

class DockerWorker:
  """
  A class for standing up and verifying docker containers.
  """

  def __init__(self, logger = None):
    self.logger = logger or get_logger(self.__class__.__name__)

  # runs the compose.yaml file to standup the docker environment
  def compose_up(self) -> None:
    cmd = ["docker", "compose", "-f", "docker/compose.yaml", "up", "-d", "--no-recreate"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or result.stdout.strip() != "":
      msg = "The docker composition failed to stand up."
      self.logger.error(msg)
      raise RuntimeError(msg)

  # checks if the specified container is running
  def check_container(self, container_name: str = default_sandbox_name, should_throw: bool = False) -> subprocess.CompletedProcess[str]:
    cmd = ["docker", "inspect", "-f", "{{.State.Running}}", container_name]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 or result.stdout.strip() != "true":
      msg = f"The container '{container_name}' is not running."
      if should_throw:
        self.logger.error(msg)
        raise RuntimeError(msg)
      else:
        self.logger.warning(msg)
    return result
  
  # copies a file from the local directory into the specified docker container
  def copy_file_to_container(self, local_file_name: str, container_name: str = default_sandbox_name) -> str:
    container_home_path = "/home/sandboxuser"
    self.logger.debug(f"Copying '{local_file_name}' to container '{container_name}'.")

    if not os.path.isfile(local_file_name):
      error_msg = f"The local file '{local_file_name}' does not exist."
      self.logger.error(error_msg)
      raise FileNotFoundError(error_msg)
    
    # check if the container is running
    self.check_container(container_name, True)
    
    # copy the file into the container
    container_path = f"{container_name}:{container_home_path}/{os.path.basename(local_file_name)}"
    self.logger.debug(f"Running command: docker cp {local_file_name} {container_path}")
    subprocess.run(["docker", "cp", local_file_name, container_path], check=True)

    # verify the file was copied
    verify_cmd = ["docker", "exec", container_name, "test", "-f",
                  f"{container_home_path}/{os.path.basename(local_file_name)}"]
    verify_result = subprocess.run(verify_cmd, capture_output=True, text=True)
    if verify_result.returncode != 0:
      error_msg = f"Failed to verify the file '{local_file_name}' in the container '{container_name}'."
      self.logger.error(error_msg)
      raise RuntimeError(error_msg)
    
    success_msg = f"Copied {local_file_name} into {container_name}:{container_home_path}/."
    self.logger.debug(success_msg)
    return success_msg

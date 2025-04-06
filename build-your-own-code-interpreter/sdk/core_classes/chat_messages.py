from typing import List, Dict

class ChatMessages:
  """
  Stores all messages in a conversation (developer, user, assistant).
  """

  def __init__(self, initial_prompt: str):
    self.messages: List[Dict[str, str]] = []
    self.add_system_message(initial_prompt)

  def add_system_message(self, content: str) -> None:
    self.messages.append({"role": "system", "content": content})

  def add_user_message(self, content: str) -> None:
    self.messages.append({"role": "user", "content": content})

  def add_assistant_message(self, content: str) -> None:
    self.messages.append({"role": "assistant", "content": content})

  def add_tool_message(self, content: str) -> None:
    self.messages.append({"role": "tool", "content": content})

  def get_messages(self) -> List[Dict[str, str]]:
    return self.messages
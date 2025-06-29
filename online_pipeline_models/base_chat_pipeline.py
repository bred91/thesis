from abc import ABC, abstractmethod
from typing import List, Dict

class BaseChatPipeline(ABC):
    """
    Base class for chat-based pipelines.
    Each one must maintain an internal conversation state.
    """

    def __init__(self):
        self.chat_history: List[Dict[str, str]] = []

    @abstractmethod
    def _respond(self, user_message: str) -> str:
        """Implemented by subclasses: generates the model's response."""

    def ask(self, user_message: str) -> str:
        """
        Adds the user's turn to the history, calls `_respond`, saves the reply, and returns it.
        """
        self.chat_history.append({"role": "user", "content": user_message})
        assistant_reply = self._respond(user_message)
        self.chat_history.append({"role": "assistant", "content": assistant_reply})
        return assistant_reply

    def reset(self):
        """Clears the history (useful for tests or new conversations)."""
        self.chat_history.clear()

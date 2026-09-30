from collections import deque
from typing import List, Dict


class ConversationMemory:
    """
    In-memory conversation buffer that keeps track of the last N conversation turns
    (user and voice assistant interactions) within memory.
    """

    def __init__(self, max_turns: int = 15):
        """
        Initialize conversation memory.

        :param max_turns: Number of conversation turns (user + assistant pairs)
                          to retain in memory. Defaults to 15 (storing last 10-15 conversations).
        """
        self.max_turns = max_turns
        # Each turn has 2 messages (user and assistant), so capacity = max_turns * 2
        self._history: deque = deque(maxlen=max_turns * 2)

    def add_user_message(self, text: str) -> None:
        """Add a user message to memory."""
        if text and text.strip():
            self._history.append({"role": "user", "content": text.strip()})

    def add_assistant_message(self, text: str) -> None:
        """Add an assistant response to memory."""
        if text and text.strip():
            self._history.append({"role": "assistant", "content": text.strip()})

    def add_turn(self, user_text: str, assistant_text: str) -> None:
        """Add a complete user-assistant interaction turn to memory."""
        self.add_user_message(user_text)
        self.add_assistant_message(assistant_text)

    def get_messages(self) -> List[Dict[str, str]]:
        """
        Retrieve all stored conversation messages in order.
        Compatible with OpenAI/Groq chat completions format.
        """
        return list(self._history)

    def get_turns_count(self) -> int:
        """Return the number of complete interaction turns currently stored."""
        return len(self._history) // 2

    def get_formatted_history(self) -> str:
        """Return human-readable formatted string of stored conversations."""
        lines = []
        for msg in self._history:
            sender = "User" if msg["role"] == "user" else "Assistant"
            lines.append(f"{sender}: {msg['content']}")
        return "\n".join(lines)

    def clear(self) -> None:
        """Reset and clear all stored memory."""
        self._history.clear()

    def __len__(self) -> int:
        """Return the total number of individual messages in memory."""
        return len(self._history)

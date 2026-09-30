from collections import deque


class ConversationMemory:
    """
    In-memory conversation buffer that keeps track of recent conversation turns.
    """

    def __init__(self, max_turns: int = 15):
        self._history = deque(maxlen=max_turns * 2)

    def add_turn(self, user_text: str, assistant_text: str):
        """Add a complete user-assistant interaction turn to memory."""
        if user_text and user_text.strip():
            self._history.append({"role": "user", "content": user_text.strip()})
        if assistant_text and assistant_text.strip():
            self._history.append({"role": "assistant", "content": assistant_text.strip()})

    def get_messages(self):
        """Retrieve all stored conversation messages in order."""
        return list(self._history)

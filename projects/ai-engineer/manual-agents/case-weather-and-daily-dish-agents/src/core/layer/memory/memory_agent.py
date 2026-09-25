from typing import Any


class MemoryAgent:
    """Manages conversational history and stateful memory key-values for agents."""

    def __init__(self, max_history: int = 5) -> None:
        """
        Args:
            max_history (int): Maximum number of recent interactions to keep in memory.
        """
        self._max_history = max_history
        self._history: list[dict[str, str]] = []
        self._storage: dict[str, Any] = {}

    def add_interaction(self, user_message: str, assistant_response: str) -> None:
        """Adds a new user-assistant interaction pair to the memory stack."""
        self._history.append({"user": user_message, "assistant": assistant_response})

        # Trim history if it exceeds the maximum capacity
        if len(self._history) > self._max_history:
            self._history.pop(0)

    def get_history(self) -> list[dict[str, str]]:
        """Returns the current stored conversation history."""
        return self._history

    def store(self, key: str, value: Any) -> None:
        """Stores a key-value pair in memory state (e.g., weather data by city)."""
        self._storage[key] = value

    def recall(self, key: str) -> Any | None:
        """Retrieves a stored value by key from memory state."""
        return self._storage.get(key)

    def clear(self) -> None:
        """Clears all stored conversation history and state."""
        self._history.clear()
        self._storage.clear()

from src.core.layer.memory.memory_agent import MemoryAgent


def test_memory_agent_tracking() -> None:
    """Validates that conversation history is correctly stored and retrieved."""
    memory = MemoryAgent(max_history=3)

    memory.add_interaction("Hello", "Hi there!")
    memory.add_interaction("What's the weather?", "It's sunny.")

    history = memory.get_history()
    assert len(history) == 2
    assert history[0]["user"] == "Hello"
    assert history[0]["assistant"] == "Hi there!"

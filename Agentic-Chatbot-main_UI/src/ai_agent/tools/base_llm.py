from abc import ABC, abstractmethod

class BaseLLM(ABC):
    """Abstract base class for all LLM wrappers."""

    @abstractmethod
    def chat(self, messages: list[dict]) -> str:
        """Send chat messages to the LLM and return the response."""
        pass

    @abstractmethod
    def name(self) -> str:
        """Return the name of the model."""
        pass

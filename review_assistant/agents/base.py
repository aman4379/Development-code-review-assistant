from abc import ABC, abstractmethod
from typing import Dict, Any


class Agent(ABC):
    name: str = "agent"
    description: str = ""

    def __init__(self, client=None) -> None:
        self.client = client

    @abstractmethod
    def build_prompt(self, code: str, language: str, standards: str, objectives: str) -> str:
        ...

    def run(self, code: str, language: str, standards: str, objectives: str) -> str:
        system_prompt = (
            "You are a senior software engineer performing precise, actionable code reviews. "
            "Respond with concise bullet points and small code edits where useful."
        )
        user_prompt = self.build_prompt(code=code, language=language, standards=standards, objectives=objectives)
        if self.client is None or not getattr(self.client, "is_available", False):
            # Offline fallback path handled by client's chat method
            return f"## {self.name}\n" + (self.client.chat(system_prompt, user_prompt) if self.client else "No LLM client available.")
        content = self.client.chat(system_prompt, user_prompt)
        return f"## {self.name}\n{content}"
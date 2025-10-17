from .base import Agent


class BestPracticesAgent(Agent):
    name = "Best Practices & Design"
    description = "Recommend improvements for readability, maintainability, performance, and security."

    def build_prompt(self, code: str, language: str, standards: str, objectives: str) -> str:
        return f"""
Act as a best practices reviewer.
Language: {language}
Objectives: {objectives}
Standards:
{standards}

Code:
```{language}
{code}
```

Please provide:
- Readability and maintainability improvements
- API design consistency and modularity suggestions
- Performance hotspots and optimizations
- Security concerns and mitigations
- Small improved code edits where helpful
""".strip()

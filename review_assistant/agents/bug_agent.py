from .base import Agent


class BugAgent(Agent):
    name = "Bug & Reliability"
    description = "Identify potential bugs, edge cases, exceptions, and runtime risks."

    def build_prompt(self, code: str, language: str, standards: str, objectives: str) -> str:
        return f"""
Act as a bug and reliability reviewer.
Language: {language}
Objectives: {objectives}
Standards:
{standards}

Code:
```{language}
{code}
```

Please provide:
- Potential bugs and incorrect assumptions
- Edge cases and input validation gaps
- Concurrency, resource, and error handling issues
- Small corrected code edits or tests to prevent issues
""".strip()

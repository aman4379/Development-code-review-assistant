from typing import List
from .base import Agent


class StyleAgent(Agent):
    name = "Style & Formatting"
    description = "Check style, naming, formatting, docstrings, and lint compliance."

    def build_prompt(self, code: str, language: str, standards: str, objectives: str) -> str:
        return f"""
Act as a style and formatting reviewer.
Language: {language}
Objectives: {objectives}
Standards:
{standards}

Code:
```{language}
{code}
```

Please provide:
- Key style issues with references to guideline sections when possible
- Naming and docstring suggestions
- Linting suggestions (PEP8, ESLint, etc.)
- Small corrected code edits where beneficial
""".strip()

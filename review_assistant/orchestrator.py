from typing import Dict, Any, List, Tuple

from review_assistant.agents.style_agent import StyleAgent
from review_assistant.agents.bug_agent import BugAgent
from review_assistant.agents.best_practices_agent import BestPracticesAgent


class ReviewOrchestrator:
    def __init__(self, client=None, use_llm: bool = True) -> None:
        self.client = client
        self.use_llm = use_llm
        self.agents = [
            StyleAgent(client=client),
            BugAgent(client=client),
            BestPracticesAgent(client=client),
        ]

    def run_review(self, code: str, language: str, standards: str, objectives: str) -> Tuple[str, Dict[str, str]]:
        agent_traces: Dict[str, str] = {}
        sections: List[str] = []
        for agent in self.agents:
            output = agent.run(code=code, language=language, standards=standards, objectives=objectives)
            agent_traces[agent.name] = output
            sections.append(output)

        summary = self._synthesize_summary(sections)
        report = self._compose_report(summary, sections, code, language)
        return report, agent_traces

    def _synthesize_summary(self, sections: List[str]) -> str:
        # Lightweight synthesis to highlight top items without an extra LLM call
        bullets: List[str] = []
        for section in sections:
            for line in section.splitlines():
                line = line.strip()
                if line.startswith("-") and len(bullets) < 12:
                    bullets.append(line)
        if not bullets:
            bullets = ["- No critical findings. Consider general refactors for clarity."]
        return "\n".join(["### Key Findings"] + bullets)

    def _compose_report(self, summary: str, sections: List[str], code: str, language: str) -> str:
        report_parts: List[str] = []
        report_parts.append("# Code Review Report\n")
        report_parts.append(summary)
        report_parts.append("\n---\n")
        report_parts.append("### Reviewed Code Snippet")
        report_parts.append(f"```{language}\n{code}\n```")
        report_parts.append("\n---\n")
        report_parts.append("### Detailed Agent Feedback")
        for sec in sections:
            report_parts.append(sec)
            report_parts.append("\n")
        return "\n".join(report_parts)

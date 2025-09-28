from __future__ import annotations
from multi_agent.session import MultiAgentSession
from dataclasses import dataclass, asdict
from mega_common.config import CONFIG

@dataclass
class CaseSection:
    title: str
    content: str

@dataclass
class ClinicalCase:
    topic: str
    plan: list[str]
    explanations: dict[str,str]
    critic: dict
    failsafe: dict

    def to_markdown(self) -> str:
        lines = [f"# Caso Clínico: {self.topic}", "", "## Plano", *[f"- {p}" for p in self.plan], "", "## Explicações"]
        for lvl, txt in self.explanations.items():
            lines.append(f"### {lvl.capitalize()}\n{txt}\n")
        lines.append("## Análise Crítica")
        lines.append(f"```json\n{self.critic}\n```\n")
        lines.append("## Fail-Safe")
        lines.append(f"```json\n{self.failsafe}\n```")
        return "\n".join(lines)

    def to_dict(self):
        return asdict(self)

def compose_case(topic: str) -> ClinicalCase:
    cfg = CONFIG.case_generator
    sess = MultiAgentSession()
    plan = sess.run_plan(topic=topic)["plan"]
    explanations = sess.explain_levels(topic) if cfg.include_explainer else {}
    critic = sess.critic.act(passage=" ".join(plan)) if cfg.include_critic else {}
    failsafe = sess.failsafe.act(answer=" ".join(plan)) if cfg.include_failsafe else {}
    return ClinicalCase(topic=topic, plan=plan, explanations=explanations, critic=critic, failsafe=failsafe)
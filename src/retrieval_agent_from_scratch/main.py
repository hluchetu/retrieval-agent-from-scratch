from __future__ import annotations

from sophons.agents.agent import Agent

from .agent import build_agent

_agent: Agent | None = None


def _get_agent() -> Agent:
    global _agent
    if _agent is None:
        _agent = build_agent()
    return _agent


def run(request: str, on_after_model=None) -> str:
    agent = _get_agent()

    if on_after_model:
        agent.add_hook(on_after_model)

    return agent(request).message

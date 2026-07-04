from __future__ import annotations

from sophons.agents.hooks import AfterModelCall

from .agent import build_agent


def run(request: str, on_after_model=None) -> str:
    agent = build_agent()

    if on_after_model:
        agent.add_hook(on_after_model)

    return agent(request).message

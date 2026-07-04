from __future__ import annotations

from sophons.agents.agent import Agent
from sophons.integrations.models.deepseek import DeepSeekModel
from sophons.tools import RetrieverTool

from .config import settings
from .knowledge import build_retriever


def build_agent() -> Agent:
    retriever = build_retriever()

    search_tool = RetrieverTool(
        name="search_docs",
        description=(
            "Search the company documentation for information about billing, "
            "refunds, subscriptions, and account policies. "
            "Use this whenever the user asks about pricing, plans, cancellation, "
            "payment, or any policy question."
        ),
        retriever=retriever,
        top_k=4,
    )

    return Agent(
        model=DeepSeekModel(model="deepseek-chat", api_key=settings.deepseek_api_key),
        tools=[search_tool],
        system_prompt=(
            "You are a support assistant with access to company documentation. "
            "Always search the docs before answering policy questions. "
            "If the documentation does not contain an answer, say so clearly — "
            "do not make up information."
        ),
    )

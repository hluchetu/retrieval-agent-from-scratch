# retrieval-agent-from-scratch

A retrieval-augmented agent built from scratch on top of [Sophons](https://github.com/hluchetu/sophons).

Part 6 of the [Architecture Patterns Behind AI Agents](https://luchetu.com/articles/agent-patterns-retrieval) series.

## What it does

The agent answers questions by searching a local knowledge base of documents. If the first search returns irrelevant results, it rewrites the query and tries again. If the knowledge base has no answer, it says so — it does not generate one from training data.

## How it works

```
User question
      │
      ▼
┌─────────────┐
│    Agent    │  deepseek-reasoner — decides when and what to search
└──────┬──────┘
       │  calls
       ▼
┌─────────────┐
│   search()  │  embeds the query, finds closest chunks in the vector store
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ ChromaDB    │  local vector store — your knowledge base lives here
└─────────────┘
```

The agent uses `deepseek-reasoner` for reasoning. Documents are embedded with OpenAI `text-embedding-3-small` and stored in a local ChromaDB collection.

## Project structure

```
retrieval-agent-from-scratch/
├── docs/                          ← sample knowledge base documents
├── src/retrieval_agent_from_scratch/
│   ├── config.py                  ← API keys and settings
│   ├── knowledge.py               ← load and embed documents into ChromaDB
│   ├── retriever.py               ← search tool the agent calls
│   ├── agent.py                   ← the ReAct agent with retrieval tool
│   ├── main.py                    ← run()
│   └── cli.py                     ← terminal interface
└── pyproject.toml
```

## Setup

```bash
# Install dependencies
uv sync

# Add your API keys
cp .env.example .env
# Fill in DEEPSEEK_API_KEY and OPENAI_API_KEY

# Load the knowledge base (run once)
uv run load-knowledge

# Start chatting
uv run retrieval-chat
```

## Usage

```
uv run retrieval-chat
```

Ask questions about the documents in the `docs/` folder. The agent will search the knowledge base and answer based on what it finds. Try asking about something that is not in the docs to see how it handles missing information.

## Part of a series

| # | Pattern | Repo |
|---|---------|------|
| 1 | ReAct | [react-agent-from-scratch](https://github.com/hluchetu/ReAct-from-scratch) |
| 2 | Planning | [planning-agent-from-scratch](https://github.com/hluchetu/planning-agent-from-scratch) |
| 3 | Reflection | [reflection-agent-from-scratch](https://github.com/hluchetu/reflection-agent-from-scratch) |
| 4 | Routing | [routing-agent-from-scratch](https://github.com/hluchetu/routing-agent-from-scratch) |
| 5 | Multi-Agent | [multi-agent-from-scratch](https://github.com/hluchetu/multi-agent-from-scratch) |
| 6 | **Retrieval** | **this repo** |

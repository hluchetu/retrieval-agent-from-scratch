from __future__ import annotations

import argparse
from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

from sophons.agents.hooks import AfterModelCall

from .main import run

console = Console()

_PROMPT_STYLE = Style.from_dict({"prompt": "bold #5f87ff"})
_HISTORY_FILE = Path.home() / ".retrieval_agent_history"


def _print_header() -> None:
    console.print()
    console.print(
        Panel.fit(
            "[bold white]Retrieval Agent[/bold white]  [dim]model: deepseek-chat  store: chromadb[/dim]\n"
            "[dim]Type your question and press Enter. [bold]exit[/bold] or Ctrl+C to quit.[/dim]",
            border_style="bright_black",
            padding=(0, 2),
        )
    )
    console.print()


def _print_user(text: str) -> None:
    console.print(Panel(
        Text(text, style="white"),
        title="[bold #5f87ff]You[/bold #5f87ff]",
        border_style="#5f87ff",
        padding=(0, 1),
    ))


def _print_response(text: str) -> None:
    console.print(Panel(
        Markdown(text),
        title="[bold #2dba4e]Agent[/bold #2dba4e]",
        border_style="#2dba4e",
        padding=(0, 1),
    ))


def main() -> None:
    parser = argparse.ArgumentParser(prog="retrieval-chat", description="Retrieval agent CLI")
    parser.parse_args()

    _print_header()

    session: PromptSession = PromptSession(
        history=FileHistory(str(_HISTORY_FILE)),
        style=_PROMPT_STYLE,
    )

    while True:
        try:
            user_input = session.prompt("  You › ", style=_PROMPT_STYLE).strip()
        except KeyboardInterrupt:
            console.print("\n[dim]Interrupted.[/dim]")
            break
        except EOFError:
            break

        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit", "/exit", "/quit"}:
            console.print("[dim]Goodbye.[/dim]")
            break

        console.print()
        _print_user(user_input)
        console.print()

        try:
            with console.status("[dim]Searching docs...[/dim]", spinner="dots"):
                response = run(request=user_input)

            console.print()
            _print_response(response)
            console.print()

        except KeyboardInterrupt:
            console.print("\n[dim]Cancelled.[/dim]\n")
        except Exception as exc:
            console.print(f"\n[bold red]Error:[/bold red] {exc}\n")

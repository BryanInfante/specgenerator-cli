from contextlib import contextmanager
from typing import Generator

from rich.console import Console
from rich.markdown import Markdown
from rich.table import Table

console = Console()


@contextmanager
def print_spinner(message: str) -> Generator[None, None, None]:
    with console.status(f"[bold blue]{message}"):
        yield


def print_success(files: list[str]) -> None:
    table = Table(title="Archivos generados")
    table.add_column("Archivo", style="cyan")
    table.add_column("Ruta", style="green")

    for file_path in files:
        file_name = file_path.split("/")[-1]
        table.add_row(file_name, file_path)

    console.print(table)


def print_error(message: str) -> None:
    console.print(f"[bold red]Error:[/bold red] {message}")


def print_markdown(content: str) -> None:
    md = Markdown(content)
    console.print(md)

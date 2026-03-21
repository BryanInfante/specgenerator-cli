from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from spec_gen.config import (
    ApiKeyNotFoundError,
    get_api_key,
    load_config,
    mask_api_key,
    save_config,
)
from spec_gen.generator import generate_spec
from spec_gen.providers import get_provider
from spec_gen.renderer import print_error, print_markdown, print_spinner, print_success

console = Console()


@click.group()
def main() -> None:
    pass


@main.command()
@click.argument("idea")
@click.option("--output", "-o", default=".", help="Directorio de salida")
@click.option("--lang", default="es", type=click.Choice(["es", "en"]), help="Idioma")
@click.option("--force", "-f", is_flag=True, help="Sobrescribir sin confirmar")
@click.option("--no-preview", is_flag=True, help="Omitir preview de archivos generados")
def init(idea: str, output: str, lang: str, force: bool, no_preview: bool) -> None:
    output_path = Path(output).resolve()

    if not force:
        existing_files = [
            f
            for f in ["REQUIREMENTS.md", "DESIGN.md", "TASKS.md"]
            if (output_path / f).exists()
        ]
        if existing_files:
            console.print(
                f"[yellow]Ya existen archivos: {', '.join(existing_files)}[/yellow]"
            )
            if not click.confirm("¿Sobrescribir?"):
                console.print("[yellow]Operación cancelada.[/yellow]")
                return

    try:
        config = load_config()
        config["api_key"] = get_api_key()

        with print_spinner("Generando especificaciones..."):
            provider = get_provider(config)
            spec = generate_spec(idea, provider, lang)

        output_path.mkdir(parents=True, exist_ok=True)

        files_created = []
        for filename, content in [
            ("REQUIREMENTS.md", spec["requirements"]),
            ("DESIGN.md", spec["design"]),
            ("TASKS.md", spec["tasks"]),
        ]:
            file_path = output_path / filename
            file_path.write_text(content, encoding="utf-8")
            files_created.append(str(file_path))

        print_success(files_created)

        if not no_preview:
            console.print("\n[bold]Preview de archivos generados:[/bold]\n")
            for filename, content in [
                ("REQUIREMENTS.md", spec["requirements"]),
                ("DESIGN.md", spec["design"]),
                ("TASKS.md", spec["tasks"]),
            ]:
                lines = content.split("\n")
                preview_lines = lines[:20]
                preview_content = "\n".join(preview_lines)
                if len(lines) > 20:
                    preview_content += "\n\n[dim]... (continúa)[/dim]"

                console.print(f"[bold cyan]--- {filename} ---[/bold cyan]")
                print_markdown(preview_content)
                console.print()

    except ApiKeyNotFoundError:
        print_error(
            "La variable de entorno SPEC_GEN_API_KEY no está configurada.\n"
            "Configúrala con: export SPEC_GEN_API_KEY=tu-api-key"
        )
    except Exception as e:
        print_error(f"Error: {e}")
        console.print("[dim]Intenta de nuevo o verifica tu conexión.[/dim]")


@main.command()
@click.option(
    "--file",
    "-f",
    required=True,
    type=click.Choice(["requirements", "design", "tasks"]),
)
@click.option("--force", "-f", is_flag=True, help="Sobrescribir sin confirmar")
def regen(file: str, force: bool) -> None:
    file_map = {
        "requirements": "REQUIREMENTS.md",
        "design": "DESIGN.md",
        "tasks": "TASKS.md",
    }

    filename = file_map[file]
    file_path = Path(filename)

    if not file_path.exists():
        print_error(
            f"El archivo {filename} no existe. Ejecuta 'spec-gen init' primero."
        )
        return

    if not force:
        if not click.confirm(f"¿Sobrescribir {filename}?"):
            console.print("[yellow]Operación cancelada.[/yellow]")
            return

    try:
        req_context = ""
        des_context = ""

        if file != "requirements" and Path("REQUIREMENTS.md").exists():
            req_context = Path("REQUIREMENTS.md").read_text(encoding="utf-8")

        if file != "design" and Path("DESIGN.md").exists():
            des_context = Path("DESIGN.md").read_text(encoding="utf-8")

        config = load_config()
        config["api_key"] = get_api_key()

        idea = "Proyecto existente. Regenerando archivo específico."

        with print_spinner(f"Regenerando {filename}..."):
            provider = get_provider(config)
            spec = generate_spec(
                idea,
                provider,
                config["output"]["language"],
                requirements_context=req_context,
                design_context=des_context,
            )

        file_content = spec[file]
        file_path.write_text(file_content, encoding="utf-8")

        print_success([str(file_path.resolve())])

    except ApiKeyNotFoundError:
        print_error("SPEC_GEN_API_KEY no está configurada.")
    except Exception as e:
        print_error(f"Error: {e}")


@main.command()
@click.option(
    "--file",
    "-f",
    default="all",
    type=click.Choice(["requirements", "design", "tasks", "all"]),
)
def show(file: str) -> None:
    file_map = {
        "requirements": "REQUIREMENTS.md",
        "design": "DESIGN.md",
        "tasks": "TASKS.md",
    }

    if file == "all":
        files_to_show = ["requirements", "design", "tasks"]
    else:
        files_to_show = [file]

    for file_type in files_to_show:
        filename = file_map[file_type]
        file_path = Path(filename)

        if not file_path.exists():
            console.print(f"[yellow]{filename} no existe.[/yellow]")
            continue

        content = file_path.read_text(encoding="utf-8")
        console.print(f"\n[bold cyan]--- {filename} ---[/bold cyan]\n")
        print_markdown(content)


@main.command()
@click.option("--show", is_flag=True, help="Mostrar configuración actual")
def config(show: bool) -> None:
    if show:
        _show_config()
    else:
        _wizard_config()


def _show_config() -> None:
    config_data = load_config()

    table = Table(title="Configuración de spec-gen")
    table.add_column("Opción", style="cyan")
    table.add_column("Valor", style="green")

    table.add_row("Provider", config_data["provider"]["name"])
    table.add_row("Base URL", config_data["provider"]["base_url"])
    table.add_row("Modelo", config_data["provider"]["model"])
    table.add_row("Idioma", config_data["output"]["language"])

    try:
        api_key = get_api_key()
        table.add_row("API Key", mask_api_key(api_key))
    except ApiKeyNotFoundError:
        table.add_row("API Key", "No configurada")

    console.print(table)


def _wizard_config() -> None:
    console.print("[bold]Configuración de spec-gen[/bold]\n")

    current_config = load_config()

    provider_name = click.prompt(
        "Provider",
        default=current_config["provider"]["name"],
        type=click.Choice(["groq", "qwen", "opencode"], case_sensitive=False),
    )

    base_url = click.prompt(
        "Base URL",
        default=current_config["provider"]["base_url"],
    )

    model = click.prompt(
        "Modelo",
        default=current_config["provider"]["model"],
    )

    language = click.prompt(
        "Idioma (es/en)",
        default=current_config["output"]["language"],
        type=click.Choice(["es", "en"], case_sensitive=False),
    )

    config_data = {
        "provider": {
            "name": provider_name.lower(),
            "base_url": base_url,
            "model": model,
        },
        "output": {
            "language": language.lower(),
            "overwrite": current_config["output"]["overwrite"],
        },
    }

    save_config(config_data)

    console.print("\n[green]Configuración guardada correctamente.[/green]")
    console.print("\nRecuerda configurar tu API key:")
    console.print("  export SPEC_GEN_API_KEY=tu-api-key")


if __name__ == "__main__":
    main()

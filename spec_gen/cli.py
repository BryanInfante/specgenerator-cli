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

console = Console()


@click.group()
def main() -> None:
    pass


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
        type=click.Choice(["qwen", "opencode"], case_sensitive=False),
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

from pathlib import Path

from spec_gen.providers.base import BaseProvider

_PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_prompt(name: str) -> str:
    prompt_file = _PROMPTS_DIR / f"{name}.md"
    return prompt_file.read_text(encoding="utf-8")


def render_prompt(template: str, **kwargs: str) -> str:
    result = template
    for key, value in kwargs.items():
        placeholder = f"{{{{{key}}}}}"
        result = result.replace(placeholder, value or "")
    return result


def generate_spec(idea: str, provider: BaseProvider, lang: str = "es") -> dict:
    requirements_template = load_prompt("requirements")
    requirements_prompt = render_prompt(
        requirements_template,
        idea=idea,
    )

    requirements_content = provider.complete(requirements_prompt)

    design_template = load_prompt("design")
    design_prompt = render_prompt(
        design_template,
        idea=idea,
        requirements_context=requirements_content,
    )

    design_content = provider.complete(design_prompt)

    tasks_template = load_prompt("tasks")
    tasks_prompt = render_prompt(
        tasks_template,
        idea=idea,
        requirements_context=requirements_content,
        design_context=design_content,
    )

    tasks_content = provider.complete(tasks_prompt)

    return {
        "requirements": requirements_content,
        "design": design_content,
        "tasks": tasks_content,
    }

from unittest.mock import MagicMock

import pytest

from spec_gen.generator import generate_spec, load_prompt, render_prompt


class TestLoadPrompt:
    def test_load_requirements_prompt(self):
        prompt = load_prompt("requirements")
        assert "ROLE" in prompt
        assert "CONTEXT" in prompt
        assert "OUTPUT" in prompt
        assert "{{idea}}" in prompt

    def test_load_design_prompt(self):
        prompt = load_prompt("design")
        assert "ROLE" in prompt
        assert "{{idea}}" in prompt
        assert "{{requirements_context}}" in prompt

    def test_load_tasks_prompt(self):
        prompt = load_prompt("tasks")
        assert "ROLE" in prompt
        assert "{{idea}}" in prompt
        assert "{{requirements_context}}" in prompt
        assert "{{design_context}}" in prompt


class TestRenderPrompt:
    def test_render_prompt_with_single_placeholder(self):
        template = "Hola {{name}}, bienvenido a {{place}}"
        result = render_prompt(template, name="Juan", place="Python")
        assert result == "Hola Juan, bienvenido a Python"

    def test_render_prompt_with_missing_placeholder(self):
        template = "Hola {{name}}, tu email es {{email}}"
        result = render_prompt(template, name="Juan")
        assert result == "Hola Juan, tu email es {{email}}"

    def test_render_prompt_with_empty_values(self):
        template = "Hola {{name}}"
        result = render_prompt(template, name="")
        assert result == "Hola "

    def test_render_prompt_with_all_placeholders_replaced(self):
        template = "{{header}}\n{{body}}\n{{footer}}"
        result = render_prompt(
            template,
            header="# Título",
            body="Contenido",
            footer="---\nFin",
        )
        assert result == "# Título\nContenido\n---\nFin"


class TestGenerateSpec:
    @pytest.fixture
    def mock_provider(self):
        provider = MagicMock()
        provider.complete.side_effect = [
            "# REQUIREMENTS.md\n\nContenido de requisitos",
            "# DESIGN.md\n\nContenido de diseño",
            "# TASKS.md\n\n- [ ] T-01 Tarea",
        ]
        return provider

    def test_generate_spec_calls_provider_three_times(self, mock_provider):
        generate_spec("una idea", mock_provider)

        assert mock_provider.complete.call_count == 3

    def test_generate_spec_returns_dict(self, mock_provider):
        result = generate_spec("una idea", mock_provider)

        assert isinstance(result, dict)
        assert "requirements" in result
        assert "design" in result
        assert "tasks" in result

    def test_generate_spec_returns_non_empty_content(self, mock_provider):
        result = generate_spec("una idea", mock_provider)

        assert len(result["requirements"]) > 0
        assert len(result["design"]) > 0
        assert len(result["tasks"]) > 0

    def test_generate_spec_passes_idea_to_first_call(self, mock_provider):
        idea = "una API REST para gestionar tareas"
        generate_spec(idea, mock_provider)

        first_call_args = mock_provider.complete.call_args_list[0][0][0]
        assert idea in first_call_args

    def test_generate_spec_passes_requirements_to_design_call(self, mock_provider):
        requirements_content = "# Requisitos del proyecto"
        mock_provider.complete.side_effect = [
            requirements_content,
            "# Diseño",
            "# Tareas",
        ]

        generate_spec("una idea", mock_provider)

        second_call_args = mock_provider.complete.call_args_list[1][0][0]
        assert requirements_content in second_call_args

    def test_generate_spec_passes_context_to_tasks_call(self, mock_provider):
        requirements_content = "# Requisitos"
        design_content = "# Diseño"
        mock_provider.complete.side_effect = [
            requirements_content,
            design_content,
            "# Tareas",
        ]

        generate_spec("una idea", mock_provider)

        third_call_args = mock_provider.complete.call_args_list[2][0][0]
        assert requirements_content in third_call_args
        assert design_content in third_call_args

from pathlib import Path

import pytest

from src.core.config import ProjectConfig


def test_load_config_exposes_sections_and_resolves_paths(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text(
        "project:\n  seed: 7\ndata:\n  raw_path: data/raw.txt\nmodel: {}\ntraining: {}\ngeneration: {}\n",
        encoding="utf-8",
    )

    config = ProjectConfig(config_path)

    assert config.project["seed"] == 7
    assert config.data["raw_path"] == "data/raw.txt"
    assert config.get_path("data", "raw_path") == (ProjectConfig.PROJECT_ROOT / "data/raw.txt").resolve()


def test_config_rejects_non_mapping_yaml(tmp_path: Path) -> None:
    config_path = tmp_path / "invalid.yaml"
    config_path.write_text("- item\n", encoding="utf-8")

    with pytest.raises(ValueError, match="dictionary"):
        ProjectConfig(config_path)


def test_get_returns_default_for_missing_nested_key(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text("project: {}\n", encoding="utf-8")
    config = ProjectConfig(config_path)

    assert config.get("missing", "value", default="fallback") == "fallback"
    with pytest.raises(KeyError):
        config.get_path("missing", "path")


def test_to_dict_returns_independent_copy(tmp_path: Path) -> None:
    config_path = tmp_path / "config.yaml"
    config_path.write_text("project:\n  seed: 7\n", encoding="utf-8")
    config = ProjectConfig(config_path)
    copied = config.to_dict()
    copied["project"]["seed"] = 99

    assert config.project["seed"] == 7

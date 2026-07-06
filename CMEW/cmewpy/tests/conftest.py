from pathlib import Path

import pytest


@pytest.fixture
def path_to_kgo():
    return Path(__file__).parent / "kgo"


@pytest.fixture
def path_to_mock_data():
    return Path(__file__).parent / "mock_data"


@pytest.fixture
def path_to_kgo_dict(path_to_kgo):
    return path_to_kgo / "basic_dict.yml"


@pytest.fixture
def path_to_blank_recipe_kgo(path_to_kgo):
    return path_to_kgo / "blank_recipe_radiation_budget.yml"


@pytest.fixture
def path_to_kgo_extended_recipe(path_to_kgo):
    return path_to_kgo / "extended_radiation_budget_recipe.yml"


@pytest.fixture
def path_to_kgo_yaml_dict(path_to_kgo):
    return path_to_kgo / "model_runs_as_dict.yml"


@pytest.fixture
def path_to_radiation_budget_variables(path_to_kgo):
    return path_to_kgo / "radiation_budget_variables.txt"


@pytest.fixture
def path_to_recipe_additionals_removed(path_to_kgo):
    return path_to_kgo / "recipe_additional_datasets_removed.yml"


@pytest.fixture
def path_to_combined_variables(path_to_kgo):
    return path_to_kgo / "variables.txt"


@pytest.fixture
def path_to_cmip6_datasets_yaml(path_to_mock_data):
    return path_to_mock_data / "cmip6_datasets.yml"


@pytest.fixture
def path_to_mock_ini(path_to_mock_data):
    return path_to_mock_data / "initial_config.ini"


@pytest.fixture
def path_to_mock_yaml_list(path_to_mock_data):
    return path_to_mock_data / "model_runs_as_list.yml"


@pytest.fixture
def path_to_mock_nl(path_to_mock_data):
    return path_to_mock_data / "model_runs.nl"


@pytest.fixture
def path_to_original_radiation_budget_recipe(path_to_mock_data):
    return path_to_mock_data / "original_recipe_radiation_budget.yml"


@pytest.fixture
def path_to_zec_recipe(path_to_mock_data):
    return path_to_mock_data / "original_recipe_zec.yml"


@pytest.fixture
def path_to_mock_recipe_paths(path_to_mock_data):
    return path_to_mock_data / "recipe_paths.yml"


@pytest.fixture
def path_to_recipe_with_additionals(path_to_mock_data):
    return path_to_mock_data / "recipe_with_additional_datasets.yml"


@pytest.fixture
def path_to_updated_recipe_kgo(path_to_mock_data):
    return path_to_mock_data / "updated_recipe_radiation_budget.yml"

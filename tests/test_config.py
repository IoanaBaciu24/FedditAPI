import pytest
import tempfile
import os
import yaml
from app.core.config import Config


@pytest.fixture
def sample_config_file():
    # Create a temporary YAML config file
    config_data = {
        "BASE_URL": "https://example.com",
        "SUBFEDDITS": "subfeddits",
        "COMMENTS": "comments",
    }
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        yaml.dump(config_data, tmp)
        tmp_path = tmp.name
    yield tmp_path
    os.remove(tmp_path)


def test_config_loading(sample_config_file):
    config = Config(sample_config_file)
    assert config["BASE_URL"] == "https://example.com"
    assert config["SUBFEDDITS"] == "subfeddits"
    assert config.get("COMMENTS") == "comments"
    assert config.get("NOT_EXISTING", "default") == "default"


def test_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        Config("nonexistent.yaml")


def test_config_invalid_yaml():
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
        tmp.write("::: invalid yaml :::")
        tmp_path = tmp.name

    with pytest.raises(RuntimeError):
        Config(tmp_path)

    os.remove(tmp_path)

from pathlib import Path

import pytest

_HERE = Path(__file__).parent


@pytest.fixture
def iris_workflow_path():
    yield _HERE / "iris.ga"

from pathlib import Path

import pytest


@pytest.fixture
def test_dir() -> Path:
    """Return test data directory"""
    return Path(__file__).expanduser().absolute().parent


@pytest.fixture
def test_data_dir(test_dir: Path) -> Path:
    """Return the test data directory"""
    return test_dir / "testdata"

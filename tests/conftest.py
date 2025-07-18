from pathlib import Path
import pytest

TEST_ROOT = Path(__file__).parent

@pytest.fixture(scope="session")
def test_data_dir():
    """
    Fixture to provide the path to the test data directory.
    
    :return: Path to the test data directory.
    """
    return TEST_ROOT / ".TEST_DATA"



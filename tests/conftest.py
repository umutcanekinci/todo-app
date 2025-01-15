import pytest
from scripts.rect import Rect

# To make fixtures available to all test files, you can define them in a conftest.py file.
@pytest.fixture
def rect():
    return Rect(0, 0, 10, 10)

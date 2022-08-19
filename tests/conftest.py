import pytest
import sqlalchemy



@pytest.fixture(scope="session")
def session():
    return "Session"
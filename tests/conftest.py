import pytest
import sqlalchemy


@pytest.fixture
def session():
    return Session
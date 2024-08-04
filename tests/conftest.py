import pytest
from fastapi.testclient import TestClient

from tech_clg.app import app


@pytest.fixture
def client():
    return TestClient(app)

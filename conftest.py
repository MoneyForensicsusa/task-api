import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def test_task():
    data = {
        'title': "Review ALINEDS Proposal",
        'description': "Review and finalize the Texas DIR ITSAC staff augmentation proposal before submission deadline",
        "priority": 2
    }
    response = client.post('/tasks', json=data)
    yield response

    client.delete(f'/tasks/{response.json()['id']}')

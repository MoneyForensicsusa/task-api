from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

#Test for POST route
def test_post_task(test_task):
    assert test_task.status_code == 201
    data = test_task.json()
    assert 'id' in data
    assert data['title'] == "Review ALINEDS Proposal"
    assert data['description'] == "Review and finalize the Texas DIR ITSAC staff augmentation proposal before submission deadline"
    assert data['priority'] == 2

#Test for DELETE route
def test_delete_task(test_task):
    task_id = test_task.json()['id']
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200
    recall = client.get(f'/tasks/{task_id}')
    assert recall.status_code == 404

#Test for GET route
def test_get_task(test_task):
    task_id = test_task.json()['id']
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 200
    data = response.json()
    assert 'id' in data
    assert data['title'] == 'Review ALINEDS Proposal'
    assert data['description']  == "Review and finalize the Texas DIR ITSAC staff augmentation proposal before submission deadline"
    assert data['priority'] == 2
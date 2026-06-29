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

#Test for PATCH route
def test_patch_status(test_task):
    task_id = test_task.json()['id']
    response = client.patch(f'/tasks/{task_id}/status', json={'status': 'in_progress'})
    assert response.status_code == 200
    assert response.json()['status'] == "in_progress"

#Test for PATCH route for invalid status
def test_patch_invalid_status(test_task):
    task_id = test_task.json()['id']
    response = client.patch(f'/tasks/{task_id}/status', json={'status': 'bannana'})
    assert response.status_code == 422

#Test for GET tasks stats route
def test_task_stats():
    data = [
        {
            "title": "Review Q3 Budget Report",
            "description": "Analyze and summarize the Q3 financial report for stakeholder presentation",
            "priority": 2
        },
        {
            "title": "Update Security Compliance Documentation",
            "description": "Review and update NIST CSF compliance docs before annual audit deadline",
            "priority": 1
        },
        {
            "title": "Onboard New Team Member",
            "description": "Prepare onboarding materials and schedule orientation sessions for new hire",
            "priority": 3
        }
    ]
    ids =[]
    for d in data:
        response = client.post('/tasks', json=d)
        ids.append(response.json()['id'])
    # patch one of the task status
    task_id = ids[2]
    patched = client.patch(f'/tasks/{task_id}/status', json={'status': 'done'})
    #get the stats and assert
    stats_response = client.get('/tasks/stats')
    assert stats_response.status_code == 200
    stats = stats_response.json()
    assert stats['total'] >= 3
    assert stats['pending'] >= 2
    assert stats['done'] >= 1
    #cleanup
    for id in ids:
        client.delete(f'/tasks/{id}')

#Test for priority level route
def test_priority_level(test_task):
    level = test_task.json()['priority']
    response = client.get(f'/tasks/priority/{level}')
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["priority"] == level


    
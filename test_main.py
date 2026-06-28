from fastapi.testclient import TestClient
from main import app

cleint = TestClient(app)

#Test for POST route
def test_post_task(test_customer):
    assert test_customer.status_code == 201
    data = test_customer.json()
    assert id in data
    assert data['title'] == "Review ALINEDS Proposal"
    assert data['description'] == "Review and finalize the Texas DIR ITSAC staff augmentation proposal before submission deadline"
    assert data['priority'] == 2
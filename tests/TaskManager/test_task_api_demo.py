import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from controllers.taskmanager import app
@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_post_valid(client):
    response = client.post('/tasks', json={
        'userId': 1,
        'category': 'school',
        'colorShade': 2,
        'title': 'Do homework',
        'description': 'Math exercises',
        'dueDate': '2024-07-25',
        'doDate': '2024-07-23',
        'url': 'http://test.com',
        'orderIndex': 1
    })
    assert response.status_code == 201
    assert response.json['success']

def test_post_invalid(client):
    resp = client.post('/tasks', json={
        'userId': 1,
        'colorShade': 55,  # Invalid
        'title': ''        # Blank
    })
    assert resp.status_code == 400
    assert not resp.json['success']
    assert 'Title required.' in resp.json['errors']

def test_get_tasks(client):
    resp = client.get('/tasks?userId=1')
    assert resp.status_code == 200
    assert resp.json['success']

def test_put_invalid(client):
    resp = client.put('/tasks/1', json={
        'title': ''
    })
    assert resp.status_code == 400
    assert not resp.json['success']

def test_delete_task(client):
    resp = client.delete('/tasks/1')
    assert resp.status_code in [200, 404]

def test_drag_drop(client):
    payload = [{"taskId": 1, "orderIndex": 2}, {"taskId": 2, "orderIndex": 1}]
    resp = client.put('/tasks/reorder', json=payload)
    assert resp.status_code == 200
    assert resp.json['success']

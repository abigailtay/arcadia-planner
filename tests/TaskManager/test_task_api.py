import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from controllers.taskmanager import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_create_task_valid(client):
    resp = client.post('/tasks', json={
        'userId': 1,
        'category': 'Work',
        'colorShade': 2,
        'title': 'Test Task',
        'description': 'Testing',
        'dueDate': '2024-07-01',
        'doDate': '2024-06-30',
        'url': 'http://test.com',
        'orderIndex': 1
    })
    assert resp.status_code == 201
    assert resp.json['success'] is True

def test_create_task_invalid(client):
    resp = client.post('/tasks', json={
        'userId': 1,
        'colorShade': 100,
        'title': ''  # Blank
    })
    assert resp.status_code == 400
    assert resp.json['success'] is False

def test_get_tasks(client):
    resp = client.get('/tasks?userId=1')
    assert resp.status_code == 200
    assert resp.json['success'] is True

def test_update_task_invalid(client):
    resp = client.put('/tasks/1', json={
        'title': ''
    })
    assert resp.status_code == 400
    assert resp.json['success'] is False

def test_delete_task(client):
    resp = client.delete('/tasks/1')
    assert resp.status_code in [200, 404]

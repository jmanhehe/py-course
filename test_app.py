import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Test to get all tasks
def test_get_tasks(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert response.json == {"tasks": [
    {
        "id": 1,
        "description": "This is the first Description Updated",
        "category": "This is the first Category Updated",
        "status": "completed"
    },
    {
        "id": 2,
        "description": "This is the second Description",
        "category": "This is the second Category",
        "status": "pending"
    }]}

# Test to get a specific task
def test_get_specific_task(client):
    response = client.get('/tasks/1')
    assert response.status_code == 200
    assert response.json == {
        "id": 1,
        "description": "This is the first Description Updated",
        "category": "This is the first Category Updated",
        "status": "completed"
    }

# Test to add a new task
def test_add_task(client):
    response = client.post('/tasks/add', json={
        "id": 3,
        "description": "This is the third Description",
        "category": "This is the third Category"
    })
    assert response.status_code == 200
    assert response.json == {
        "status": "success",
        "message": "Task added successfully!",
        "task": {
            "id": 3,
            "description": "This is the third Description",
            "category": "This is the third Category",
            "status": "pending"
        }
    }

# - 3 test cases for the DELETE endpoint, one for each of the following scenarios:
# - No password
# - Incorrect password
# - Correct password 
# - Comment out as needed to test each scenario
# - previous test will create a new task, and last delete test will delete newly created task

def test_delete_task_no_password(client):
    response = client.delete('/tasks/3')
    assert response.status_code == 400
    assert response.json == {"error": "Missing JSON in request"}

def test_delete_task_wrong_password(client):
    response = client.delete('/tasks/3', json={"password": "asd"})
    assert response.status_code == 401
    assert response.json == {"error": "Incorrect password"}

def test_delete_task_correct_password(client):
    response = client.delete('/tasks/3', json={"password": "123"})
    assert response.status_code == 200
    assert response.json == {"status": "success", "message": "Task with id 3 deleted successfully!"}

# Test for updating a task
def test_update_task(client):
    response = client.put('/tasks/1', json={
        "description": "This is the first Description Updated",
        "category": "This is the first Category Updated",
        "status": "completed"
    })
    assert response.status_code == 200
    assert response.json == {
        "status": "success",
        "message": "Task updated successfully!",
        "task": {
            "id": 1,
            "description": "This is the first Description Updated",
            "category": "This is the first Category Updated",
            "status": "completed"
        }
    }

# Test for completing a task
def test_complete_task(client):
    response = client.put('/tasks/1/complete')
    assert response.status_code == 200
    assert response.json == {
        "status": "success",
        "message": "Task with id 1 completed successfully!"
    }

# Test for getting categories
# Response from the endpoint somehow returns categories in weird order, not sure if its always the same order.
# This might fail cause of that.
# EDIT: Think this is fixed by the use of a .sort() on the categories list.
def test_get_categories(client):
    response = client.get('/tasks/categories')
    assert response.status_code == 200
    assert response.json == {"categories": [
        "This is the first Category Updated",
        "This is the second Category"
    ]}

# Test for getting all tasks under a category
def test_get_tasks_by_category(client):
    response = client.get('/tasks/category/This is the second Category')
    assert response.status_code == 200
    assert response.json == {"tasks": [
        {
            "id": 2,
            "description": "This is the second Description",
            "category": "This is the second Category",
            "status": "pending"
        }
    ]}
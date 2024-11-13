from flask import Flask, render_template, redirect, url_for, request
from functools import wraps
import json

app = Flask(__name__)

# NOT NEEDED WITHOUT TEST_TASKS.JSON
# def test_file():
#     if test_file
#         with open(testfile)
#         return testfile
#     else 
#         with open(file)
#         return file

# HOME
@app.route('/', methods=['GET'])
def tasks():
    with open('tasks.json', 'r') as file:
        tasks = json.load(file)
        
    return render_template('index2.html', tasks=tasks)

# GET TASKS
@app.route('/tasks', methods=['GET'])
def get_tasks():
    with open('tasks.json', 'r') as file:
        tasks = json.load(file)

    if request.args.get('completed') == 'true':
        return {"tasks": [task for task in tasks if task['status'] == 'completed']}
    elif request.args.get('completed') == 'false':
        return {"tasks": [task for task in tasks if task['status'] != 'completed']}
    else: 
        return {"tasks": tasks}

# ADD TASK
@app.route('/tasks/add', methods=['POST'])
def add_task():
    # Check that all required fields are present
    required_fields = ['id', 'description', 'category']

    if request.is_json:
        data = request.json
    else:
        data = request.form

    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return {"status": "error", "message": f"Missing fields: {', '.join(missing_fields)}"}, 400

    # Load existing tasks from tasks.json
    try:
        with open('tasks.json', 'r') as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []  # Initialize tasks list if file doesn't exist or is corrupted

    try:
        task_id = int(data.get('id'))
    except ValueError:
        return {"status": "error", "message": "Task ID must be an integer"}, 400
    
    if any(task['id'] == task_id for task in tasks):
        return {"status": "error", "message": f"Task with id {task_id} already exists"}, 400

    new_task = {
        'id': task_id,
        'description': data.get('description'),
        'category': data.get('category'),
        'status': 'pending'
    }
    tasks.append(new_task)

    # Save updated tasks to tasks.json
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)

    print('Task added:', new_task)
    return {"status": "success", "message": "Task added successfully!", "task": new_task}, 200

# GET SPECIFIC TASK
@app.route('/tasks/<int:id>', methods=['GET'])
def get_specific_task(id):
    with open('tasks.json', 'r') as file:
        tasks = json.load(file)
    task = next((task for task in tasks if task['id'] == id), None)
    if task is None:
        return "Task not found", 404
    print(task)
    return task

# DECORATOR FOR PASSWORD
def password_req(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.is_json:
            return {"error": "Missing JSON in request"}, 400
        
        data = request.get_json()

        if data.get("password") != "123":
            return {"error": "Incorrect password"}, 401
        
        return f(*args, **kwargs)
    return decorated

# DELETE TASK
@app.route('/tasks/<int:id>', methods=['DELETE'])
@password_req
def delete_task(id):
    try:
        with open('tasks.json', 'r') as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return "Tasks file not found or is corrupted", 500
    
    initial_length = len(tasks)
    tasks = [task for task in tasks if task['id'] != id]

    if len(tasks) == initial_length:
        print("404 error")
        return "Task not found", 404
    
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)

    return {"status": "success", "message": f"Task with id {id} deleted successfully!"}, 200

# UPDATE TASK
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):

    if request.is_json:
        data = request.json
    else:
        data = request.form

    try:
        with open('tasks.json', 'r') as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return "Tasks file not found or is corrupted", 500
    
    task = next((task for task in tasks if task['id'] == id), None)
    if task is None:
        return "Task not found", 404
    
    task.update({key: data.get(key) for key in ['description', 'category', 'status'] if data.get(key) is not None})

    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)
    print('this is my PUT task', task)
    return {"status": "success", "message": "Task updated successfully!", "task": task}

# COMPLETE TASK
@app.route('/tasks/<int:id>/complete', methods=['PUT'])
def complete_task(id):
    try:
        with open('tasks.json', 'r') as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return "Tasks file not found or is corrupted", 500
    
    task = next((task for task in tasks if task['id'] == id), None)
    if task is None:
        return "Task not found", 404
    
    task['status'] = 'completed'

    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)
    print('this is my complete task', task)
    return {"status": "success", "message": f"Task with id {id} completed successfully!"}

# GET CATEGORIES
@app.route('/tasks/categories', methods=['GET'])
def get_categories():
    with open('tasks.json', 'r') as file:
        tasks = json.load(file)
    categories = list(set(task['category'] for task in tasks))
    categories.sort()
    print(categories)
    return {"categories": categories}

# GET TASKS BY CATEGORY
@app.route('/tasks/category/<category>', methods=['GET'])
def get_tasks_by_category(category):
    with open('tasks.json', 'r') as file:
        tasks = json.load(file)
    tasks = [task for task in tasks if task['category'] == category]
    return {"tasks": tasks}

if __name__ == '__main__':
    app.run(debug=True, port=5001)
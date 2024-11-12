from flask import Flask, render_template, redirect, url_for, request
import json

app = Flask(__name__)

# HOME
@app.route('/', methods=['GET'])
def tasks():
    with open('tasks.json', 'r') as file:
        tasks = json.load(file)

    return render_template('index2.html', tasks=tasks)

# ADD TASK
@app.route('/tasks/add', methods=['POST'])
def add_task():
    # Check that all required fields are present
    required_fields = ['id', 'description', 'category', 'status']
    missing_fields = [field for field in required_fields if field not in request.form]
    if missing_fields:
        return {"status": "error", "message": f"Missing fields: {', '.join(missing_fields)}"}, 400

    # Load existing tasks from tasks.json
    try:
        with open('tasks.json', 'r') as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        tasks = []  # Initialize tasks list if file doesn't exist or is corrupted

    try:
        task_id = int(request.form.get('id'))
    except ValueError:
        return {"status": "error", "message": "Task ID must be an integer"}, 400
    
    if any(task['id'] == task_id for task in tasks):
        return {"status": "error", "message": f"Task with id {task_id} already exists"}, 400

    # Create new task with auto-generated id
    new_task = {
        'id': task_id,
        'description': request.form.get('description'),
        'category': request.form.get('category'),
        'status': request.form.get('status')
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

# DELETE TASK
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    try:
        with open('tasks.json', 'r') as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return "Tasks file not found or is corrupted", 500
    
    initial_length = len(tasks)
    tasks = [task for task in tasks if task['id'] != id]

    if len(tasks) == initial_length:
        return "Task not found", 404
    
    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)

    return {"status": "success", "message": f"Task with id {id} deleted successfully!"}, 200

# UPDATE TASK
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    try:
        with open('tasks.json', 'r') as file:
            tasks = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return "Tasks file not found or is corrupted", 500
    
    task = next((task for task in tasks if task['id'] == id), None)
    if task is None:
        return "Task not found", 404
    
    task.update({key: request.form.get(key) for key in ['description', 'category', 'status'] if request.form.get(key) is not None})

    with open('tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)
    print('this is my PUT task', task)
    return task


if __name__ == '__main__':
    app.run(debug=True)
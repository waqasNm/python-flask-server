from flask import Flask, jsonify, render_template
from flask import request
from bson.objectid import ObjectId
from pymongo import MongoClient
client = MongoClient('localhost',27017)
db = client.todo
collection = db.items

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Task-1',
        'description': u'this is Task-1 description',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

#///Get All Tasks////
@app.route('/tasks',methods = ['GET'])
def getTasks():
    return jsonify({'tasks':tasks})

#///Get Single Task////
@app.route('/tasks/<int:task_id>',methods = ['GET'])
def getTask(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        return jsonify({'error':404})
    return jsonify({'tasks':task})

#///Add Tasks////
@app.route('/tasks', methods=['POST'])
def create():
    print(request.json)
    if not request.json or not 'title' in request.json:
        return jsonify({'error':404})
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json['description'],
        'done': False
    }
    tasks.append(task)
    return jsonify({"tasks":tasks}),201

#////Delete Task////
@app.route('/tasks/<int:task_id>', methods = ['DELETE'])
def deleteTask(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        return jsonify({"error": 404})
    tasks.remove(task[0])
    return jsonify({'tasks':tasks})

#///Update Task////
@app.route('/tasks/<int:task_id>', methods = ['PUT'])
def updateTask(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        return jsonify({'error':404})
    if not request.json:
        return jsonify({'error':400})
    if 'title' in request.json and type(request.json['title']) != str:
        return jsonify({'error':400})
    if 'description' in request.json and type(request.json['description']) != str:
        return jsonify({'error':404})
    if 'done' in request.json and type(request.json['done']) is not bool:
        return jsonify({'error':404})
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})

# ///Get all todos with pymongo////
@app.route('/todos', methods = ['GET'])
def todos():
    return  getTasks()

#///Add Todo with pymongo///
@app.route('/add-todo', methods = ['POST'])
def addTodo():
    print(request.json)
    collection.insert_one(request.json)
    return  getTasks()

# ///Delete Todo with pymongo///
@app.route('/delete-todo/<id>', methods = ['DELETE'])
def deleteTodo(id):
    print(id)
    collection.delete_many({'_id':ObjectId(id)})
    return getTasks()

# ///Update Todo with pymongo///
@app.route('/update-todo', methods = ['PUT'])
def updateTodo():
    item = request.json
    collection.update_one({'_id':ObjectId(item['_id'])},{'$set':{'task':item['task']}} )
    return getTasks()

# /// Get all todos function ///
def getTasks():
    todos = []
    for key in collection.find():
        todos.append({'_id':str(key['_id']),'task':key['task']})
    return jsonify(todos)
# ////End////

@app.route('/')
def display():
    return render_template('demo.html')

@app.route('/profile/<username>')
def profile(username):
    return "Hello World!" + username


if __name__=='__main__':
    app.run()
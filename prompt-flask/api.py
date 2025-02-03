from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista de tareas (simulación de una base de datos)
tasks = [
    {"id": 1, "title": "Comprar leche", "done": False},
    {"id": 2, "title": "Sacar la basura", "done": True}
]

# Obtener todas las tareas
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

# Obtener una tarea por ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Tarea no encontrada"}), 404
    return jsonify(task)

# Crear una nueva tarea
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    if "title" not in data:
        return jsonify({"error": "El título es obligatorio"}), 400

    new_task = {
        "id": tasks[-1]["id"] + 1 if tasks else 1,
        "title": data["title"],
        "done": data.get("done", False)
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

# Actualizar una tarea existente
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return jsonify({"error": "Tarea no encontrada"}), 404

    data = request.json
    task["title"] = data.get("title", task["title"])
    task["done"] = data.get("done", task["done"])
    return jsonify(task)

# Eliminar una tarea
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return jsonify({"message": "Tarea eliminada"}), 200

if __name__ == '__main__':
    app.run(debug=True)
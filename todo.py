from flask import Flask , jsonify , request

app = Flask(__name__)

#Initial Data in todo list
items = [
    {"id":1, "name":"Item 1", "description":"This is item 1"},{
        "id":2, "name":"Item 2", "description":"This is item 2"
    }
]
@app.route('/')
def home():
    return "Welcome to my one and only TODO App"

@app.route("/items",methods=['GET'])
def get_items():
    return jsonify(items)

@app.route("/items/<int:item_id>", methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404 
    
@app.route("/items", methods=['POST'])
def create_item():
    if not request.json or 'name' not in request.json:
        return jsonify({"error": "Bad Request"}), 400   
    new_item = {
        "id": items[-1]["id"] + 1 if items else 1,
        "name": request.json["name"],
        "description": request.json["description"]
    }
    items.append(new_item)
    return jsonify(new_item), 201

@app.route("/items/<int:item_id>", methods=['PUT'])
def update_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    
    if not request.json:
        return jsonify({"error": "Bad Request"}), 400
    
    item["name"] = request.json.get("name", item["name"])
    item["description"] = request.json.get("description", item["description"])
    
    return jsonify(item)

@app.route("/items/<int:item_id>", methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item["id"] != item_id]
    return jsonify({"message": "Item deleted successfully"}), 204

if __name__ == '__main__':
    app.run(debug=True)
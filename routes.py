from flask import Flask, request, jsonify

from app.api import enrich_item_with_off
from app.database import list_items, find_item, create_item, update_item as db_update_item, delete_item

app = Flask(__name__)


# GET all items
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(list_items()), 200


# GET one item
@app.route("/inventory/<int:id>", methods=["GET"])
def get_item(id):
    item = find_item(id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    if "off" not in item:
        try:
            enrich_item_with_off(item)
        except Exception:
            pass
    return jsonify(item), 200


# POST new item
@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.json
    if not data.get("name") or not data.get("quantity") or not data.get("price"):
        return jsonify({"error": "name, quantity and price are required"}), 400
    item = {
        "name": data.get("name"),
        "quantity": data.get("quantity"),
        "price": data.get("price"),
    }
    if data.get("barcode"):
        item["barcode"] = data.get("barcode")
    try:
        item = enrich_item_with_off(item)
    except Exception:
        pass
    result = create_item(item)
    return jsonify(result), 201


# PATCH item
@app.route("/inventory/<int:id>", methods=["PATCH"])
def update_item_endpoint(id):
    data = request.json
    item = db_update_item(id, data)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


# DELETE item
@app.route("/inventory/<int:id>", methods=["DELETE"])
def delete_item_endpoint(id):
    if not delete_item(id):
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"message": f"Item {id} deleted successfully"}), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)
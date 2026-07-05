from flask import Flask, request, jsonify

from app.api import enrich_item_with_off

app = Flask(__name__)

# In-memory food inventory
inventory = [
    {"id": 1, "name": "Apples", "quantity": 20, "price": 2.50},
    {"id": 2, "name": "Milk", "quantity": 10, "price": 1.80},
    {"id": 3, "name": "Bread", "quantity": 8, "price": 3.20},
]


# find item by id
def find_item(item_id):
    return next((item for item in inventory if item["id"] == item_id), None)


# GET all items
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200


# GET one item
@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = find_item(item_id)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    # If we don't already have enrichment info, attempt to fetch it
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

    # Validate required fields
    if not data.get("name") or not data.get("quantity") or not data.get("price"):
        return jsonify({"error": "name, quantity and price are required"}), 400

    new_id = max(item["id"] for item in inventory) + 1 if inventory else 1

    new_item = {
        "id":       new_id,
        "name":     data.get("name"),
        "quantity": data.get("quantity"),
        "price":    data.get("price"),
    }

    # Try to enrich the item with OpenFoodFacts data (by barcode or name)
    try:
        new_item = enrich_item_with_off(new_item)
    except Exception:
        # Never fail the request if enrichment fails, still create the item
        pass

    inventory.append(new_item)
    return jsonify(new_item), 201


# PATCH item
@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = find_item(item_id)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.json

    # Only update fields that were actually sent
    if "name"     in data: item["name"]     = data["name"]
    if "quantity" in data: item["quantity"] = data["quantity"]
    if "price"    in data: item["price"]    = data["price"]

    return jsonify(item), 200


# DELETE item
@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = find_item(item_id)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    inventory.remove(item)
    return jsonify({"message": f"Item {item_id} deleted successfully"}), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)
from flask import Flask, request, jsonify

from app.api import enrich_item_with_off

app = Flask(__name__)

# In-memory inventory
hardware_tools = [
    {"id": 1, "name": "Wrench",     "quantity": 10, "price": 250.00},
    {"id": 2, "name": "Screwdriver","quantity": 25, "price": 150.00},
    {"id": 3, "name": "Hammer",     "quantity": 8,  "price": 400.00},
]

# find item by id
def find_item(id):
    return next((item for item in hardware_tools if item["id"] == id), None)


# GET all items
@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(hardware_tools), 200


# GET one item
@app.route("/inventory/<int:id>", methods=["GET"])
def get_item(id):
    item = find_item(id)

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

    # Generate a new id — highest current id + 1
    new_id = max(item["id"] for item in hardware_tools) + 1 if hardware_tools else 1

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

    hardware_tools.append(new_item)
    return jsonify(new_item), 201


# PATCH item
@app.route("/inventory/<int:id>", methods=["PATCH"])
def update_item(id):
    item = find_item(id)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.json

    # Only update fields that were actually sent
    if "name"     in data: item["name"]     = data["name"]
    if "quantity" in data: item["quantity"] = data["quantity"]
    if "price"    in data: item["price"]    = data["price"]

    return jsonify(item), 200


# DELETE item
@app.route("/inventory/<int:id>", methods=["DELETE"])
def delete_item(id):
    item = find_item(id)

    if not item:
        return jsonify({"error": "Item not found"}), 404

    hardware_tools.remove(item)
    return jsonify({"message": f"Item {id} deleted successfully"}), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)
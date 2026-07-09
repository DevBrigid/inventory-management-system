import json
import os
from typing import List, Optional, Dict

DB_PATH = os.environ.get("INVENTORY_DB_PATH", os.path.join(os.path.dirname(os.path.dirname(__file__)), "inventory.json"))


def _load_inventory() -> List[Dict]:
    if not os.path.exists(DB_PATH):
        return [
            {"id": 1, "name": "Apples", "quantity": 20, "price": 2.50},
            {"id": 2, "name": "Milk", "quantity": 10, "price": 1.80},
            {"id": 3, "name": "Bread", "quantity": 8, "price": 3.20},
        ]
    try:
        with open(DB_PATH, "r", encoding="utf-8") as handle:
            data = json.load(handle)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def _save_inventory(items: List[Dict]) -> None:
    directory = os.path.dirname(DB_PATH)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as handle:
        json.dump(items, handle, indent=2)


inventory: List[Dict] = _load_inventory()


def _sync_inventory() -> List[Dict]:
    global inventory
    inventory = _load_inventory()
    return inventory


def find_item(item_id: int) -> Optional[Dict]:
    return next((item for item in _sync_inventory() if item["id"] == item_id), None)


def list_items() -> List[Dict]:
    return _sync_inventory()


def create_item(item: Dict) -> Dict:
    items = _sync_inventory()
    item_id = max((existing["id"] for existing in items), default=0) + 1
    item["id"] = item_id
    items.append(item)
    _save_inventory(items)
    inventory = items
    return item


def update_item(item_id: int, updates: Dict) -> Optional[Dict]:
    items = _sync_inventory()
    item = next((existing for existing in items if existing["id"] == item_id), None)
    if not item:
        return None
    item.update({k: updates[k] for k in ("name", "quantity", "price", "barcode") if k in updates})
    _save_inventory(items)
    inventory = items
    return item


def delete_item(item_id: int) -> bool:
    items = _sync_inventory()
    item = next((existing for existing in items if existing["id"] == item_id), None)
    if not item:
        return False
    items.remove(item)
    _save_inventory(items)
    inventory = items
    return True


__all__ = ["inventory", "find_item", "list_items", "create_item", "update_item", "delete_item"]

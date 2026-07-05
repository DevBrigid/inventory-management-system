from typing import List, Optional, Dict

inventory: List[Dict] = [
    {"id": 1, "name": "Apples", "quantity": 20, "price": 2.50},
    {"id": 2, "name": "Milk", "quantity": 10, "price": 1.80},
    {"id": 3, "name": "Bread", "quantity": 8, "price": 3.20},
]


def find_item(item_id: int) -> Optional[Dict]:
    return next((item for item in inventory if item["id"] == item_id), None)


def list_items() -> List[Dict]:
    return inventory


def create_item(item: Dict) -> Dict:
    item_id = max((existing["id"] for existing in inventory), default=0) + 1
    item["id"] = item_id
    inventory.append(item)
    return item


def update_item(item_id: int, updates: Dict) -> Optional[Dict]:
    item = find_item(item_id)
    if not item:
        return None
    item.update({k: updates[k] for k in ("name", "quantity", "price", "barcode") if k in updates})
    return item


def delete_item(item_id: int) -> bool:
    item = find_item(item_id)
    if not item:
        return False
    inventory.remove(item)
    return True


__all__ = ["inventory", "find_item", "list_items", "create_item", "update_item", "delete_item"]

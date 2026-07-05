from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List


@dataclass
class InventoryItem:
    id: int
    name: str
    quantity: int
    price: float
    barcode: Optional[str] = None
    off: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InventoryItem":
        return cls(
            id=data["id"],
            name=data["name"],
            quantity=data.get("quantity", 0),
            price=data.get("price", 0.0),
            barcode=data.get("barcode"),
            off=data.get("off", {}),
        )


def find_item(items: List[InventoryItem], item_id: int) -> Optional[InventoryItem]:
    return next((item for item in items if item.id == item_id), None)


def sample_inventory() -> List[InventoryItem]:
    return [
        InventoryItem(id=1, name="Apples", quantity=20, price=2.5),
        InventoryItem(id=2, name="Milk", quantity=10, price=1.8),
        InventoryItem(id=3, name="Bread", quantity=8, price=3.2),
    ]


__all__ = ["InventoryItem", "find_item", "sample_inventory"]

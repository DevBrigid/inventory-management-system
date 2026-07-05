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
        InventoryItem(id=1, name="Wrench", quantity=10, price=250.0),
        InventoryItem(id=2, name="Screwdriver", quantity=25, price=150.0),
        InventoryItem(id=3, name="Hammer", quantity=8, price=400.0),
    ]


__all__ = ["InventoryItem", "find_item", "sample_inventory"]

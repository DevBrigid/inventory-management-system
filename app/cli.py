import argparse
import requests

from app.database import list_items, create_item, update_item, delete_item
from app.api import enrich_item_with_off


def show_items():
    items = list_items()
    if not items:
        print("No inventory items.")
        return
    for item in items:
        print(item)


def add_item(args):
    item = {
        "name": args.name,
        "quantity": args.quantity,
        "price": args.price,
    }
    if args.barcode:
        item["barcode"] = args.barcode
    try:
        item = enrich_item_with_off(item)
    except Exception:
        pass
    created = create_item(item)
    print("Created:", created)


def update_item_cmd(args):
    updates = {}
    if args.name:
        updates["name"] = args.name
    if args.quantity is not None:
        updates["quantity"] = args.quantity
    if args.price is not None:
        updates["price"] = args.price
    if args.barcode:
        updates["barcode"] = args.barcode
    updated = update_item(args.id, updates)
    if not updated:
        print("Item not found.")
        return
    print("Updated:", updated)


def delete_item_cmd(args):
    if delete_item(args.id):
        print(f"Deleted item {args.id}")
    else:
        print("Item not found.")


def main():
    parser = argparse.ArgumentParser(description="Inventory admin CLI")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="List inventory items")

    add_parser = sub.add_parser("add", help="Add a new inventory item")
    add_parser.add_argument("--name", required=True)
    add_parser.add_argument("--quantity", type=int, required=True)
    add_parser.add_argument("--price", type=float, required=True)
    add_parser.add_argument("--barcode")

    upd_parser = sub.add_parser("update", help="Update an existing item")
    upd_parser.add_argument("id", type=int)
    upd_parser.add_argument("--name")
    upd_parser.add_argument("--quantity", type=int)
    upd_parser.add_argument("--price", type=float)
    upd_parser.add_argument("--barcode")

    del_parser = sub.add_parser("delete", help="Delete an item")
    del_parser.add_argument("id", type=int)

    args = parser.parse_args()
    if args.command == "list":
        show_items()
    elif args.command == "add":
        add_item(args)
    elif args.command == "update":
        update_item_cmd(args)
    elif args.command == "delete":
        delete_item_cmd(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

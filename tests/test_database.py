import os
import subprocess
import sys
import tempfile
import unittest

from app import database


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.original_inventory = list(database.inventory)
        database.inventory[:] = [
            {"id": 1, "name": "Apples", "quantity": 20, "price": 2.5},
            {"id": 2, "name": "Milk", "quantity": 10, "price": 1.8},
        ]

    def tearDown(self):
        database.inventory[:] = self.original_inventory

    def test_list_items_returns_food_inventory(self):
        items = database.list_items()
        self.assertEqual(len(items), 2)
        self.assertEqual(items[0]["name"], "Apples")
        self.assertEqual(items[1]["name"], "Milk")

    def test_create_and_delete_item(self):
        created = database.create_item({"name": "Bread", "quantity": 8, "price": 3.2})
        self.assertEqual(created["id"], 3)
        self.assertEqual(created["name"], "Bread")

        deleted = database.delete_item(3)
        self.assertTrue(deleted)
        self.assertIsNone(database.find_item(3))

    def test_inventory_persists_across_processes(self):
        with tempfile.NamedTemporaryFile("w+", suffix=".json", delete=False) as handle:
            temp_path = handle.name

        try:
            env = os.environ.copy()
            env["INVENTORY_DB_PATH"] = temp_path
            first = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    "from app import database; database.create_item({'name': 'Cheese', 'quantity': 2, 'price': 4.5})",
                ],
                cwd=os.path.dirname(os.path.dirname(__file__)),
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertEqual(first.returncode, 0, msg=first.stderr)

            second = subprocess.run(
                [
                    sys.executable,
                    "-c",
                    "from app import database; print(len(database.list_items()))",
                ],
                cwd=os.path.dirname(os.path.dirname(__file__)),
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertEqual(second.stdout.strip(), "3")
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)


if __name__ == "__main__":
    unittest.main()

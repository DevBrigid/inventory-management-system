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


if __name__ == "__main__":
    unittest.main()

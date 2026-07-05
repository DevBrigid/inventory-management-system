import unittest

from routes import app


class RoutesTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_get_inventory_returns_food_items(self):
        response = self.client.get("/inventory")
        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertTrue(payload)
        self.assertEqual(payload[0]["name"], "Apples")

    def test_add_item_returns_created_item(self):
        response = self.client.post(
            "/inventory",
            json={"name": "Cheese", "quantity": 4, "price": 5.5},
        )
        self.assertEqual(response.status_code, 201)
        payload = response.get_json()
        self.assertEqual(payload["name"], "Cheese")
        self.assertEqual(payload["quantity"], 4)


if __name__ == "__main__":
    unittest.main()

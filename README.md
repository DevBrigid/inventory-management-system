# Food Inventory App

A simple Flask inventory app for managing food items, with optional OpenFoodFacts enrichment.

## Features

- Local in-memory food inventory storage
- Add, read, update, and delete inventory items
- Optional OpenFoodFacts lookup by barcode or name
- Response includes `off` details when a matching product is found

## Install

```bash
python3 -m pip install -r requirements.txt
```

## Run API

```bash
python3 main.py
```

## Run CLI

From the project root, you can run the inventory commands directly:

```bash
inventory-cli list
inventory-cli add --name "Cheese" --quantity 4 --price 5.5
inventory-cli update 1 --name "Apples" --quantity 30
inventory-cli delete 1
```

If you want to run it explicitly with Python, use:

```bash
python3 cli.py list
```

The API listens on port `5555` by default.

## API endpoints

- `GET /inventory` - list all items
- `GET /inventory/<id>` - get one item
- `POST /inventory` - add an item
- `PATCH /inventory/<id>` - update an item
- `DELETE /inventory/<id>` - delete an item

## Example payload

```json
{
  "name": "Bananas",
  "quantity": 12,
  "price": 1.75,
  "barcode": "5038495001234"
}
```

If the barcode or name matches an OpenFoodFacts product, the response may include:

```json
"off": {
  "product_name": "Bananas",
  "brands": "Brand",
  "image_url": "...",
  "nutriments": { "energy-kcal": 89 },
  "code": "5038495001234"
}
```

## Tests

Run the test suite with:

```bash
python3 -m unittest discover -s tests -v
```

# Inventory App

Simple Flask inventory app with OpenFoodFacts enrichment.

## Features

- Local in-memory inventory storage
- Add, read, update, delete inventory items
- Optional OpenFoodFacts lookup by barcode or name
- Response includes `off` details when found

## Install

```bash
python3 -m pip install -r requirements.txt
```

## Run API

```bash
python3 main.py
```

## Run CLI

```bash
python3 -m app.cli list
```

The app listens on port `5555` by default.

## API endpoints

- `GET /inventory` - list all items
- `GET /inventory/<id>` - get one item
- `POST /inventory` - add item
- `PATCH /inventory/<id>` - update item
- `DELETE /inventory/<id>` - delete item

## POST payload example

```json
{
  "name": "Canned Tomatoes",
  "quantity": 5,
  "price": 120.0,
  "barcode": "3073780011534"
}
```

If `barcode` or `name` matches an OpenFoodFacts product, the response may include:

```json
"off": {
  "product_name": "Tomato Plums",
  "brands": "Brand",
  "image_url": "...",
  "nutriments": { ... },
  "code": "3073780011534"
}
```

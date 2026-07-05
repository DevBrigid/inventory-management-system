from typing import Optional, Dict, Any
import requests

BASE_URL = "https://world.openfoodfacts.org"
DEFAULT_TIMEOUT = 5


def fetch_product_by_barcode(barcode: str, timeout: int = DEFAULT_TIMEOUT) -> Optional[Dict[str, Any]]:
	# fetch product by barcode
	if not barcode:
		return None
	try:
		url = f"{BASE_URL}/api/v0/product/{barcode}.json"
		resp = requests.get(url, timeout=timeout)
		resp.raise_for_status()
		data = resp.json()
		return data.get("product") if data.get("status") == 1 else None
	except requests.RequestException:
		return None


def search_product_by_name(name: str, timeout: int = DEFAULT_TIMEOUT) -> Optional[Dict[str, Any]]:
	# search by name, return first result
	if not name:
		return None
	try:
		params = {"search_terms": name, "action": "process", "json": 1, "page_size": 1}
		url = f"{BASE_URL}/cgi/search.pl"
		resp = requests.get(url, params=params, timeout=timeout)
		resp.raise_for_status()
		data = resp.json()
		products = data.get("products") or []
		return products[0] if products else None
	except requests.RequestException:
		return None


def get_product_details(query: str, by: str = "barcode") -> Optional[Dict[str, Any]]:
	# lookup by barcode or name
	return fetch_product_by_barcode(query) if by == "barcode" else search_product_by_name(query)


def enrich_item_with_off(item: Dict[str, Any]) -> Dict[str, Any]:
	# try barcode first, then name; attach minimal `off` data
	if not isinstance(item, dict):
		return item

	code = item.get("barcode") or item.get("ean") or item.get("upc")
	off = fetch_product_by_barcode(str(code)) if code else None
	if not off:
		name = item.get("name")
		if name:
			off = search_product_by_name(str(name))

	if off:
		item.setdefault("off", {})
		for k in ("product_name", "brands", "image_url", "nutriments", "ingredients_text"):
			if k in off:
				item["off"][k] = off.get(k)
		if off.get("code"):
			item["off"]["code"] = off.get("code")

	return item


__all__ = [
	"fetch_product_by_barcode",
	"search_product_by_name",
	"get_product_details",
	"enrich_item_with_off",
]


import json
import os

SHOPPING_FILE = "shopping.json"


def load_list():
    """Nolasa shopping.json, atgriež sarakstu. Ja fails neeksistē — atgriež []."""
    if not os.path.exists(SHOPPING_FILE):
        return []
    with open(SHOPPING_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_list(items):
    """Saglabā sarakstu shopping.json failā."""
    with open(SHOPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
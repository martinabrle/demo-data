"""In-memory data store – reads every CSV once at import time."""

from __future__ import annotations

import csv
import os
from pathlib import Path
from typing import Dict, List

# ── locate the CSV directory ─────────────────────────────────────────────────
# Prefer the CSV_DATA_DIR env var (set in production); fall back to the repo
# layout for local development (three levels up → Sample_Bike_Sales/).
_CSV_DIR = Path(os.getenv("CSV_DATA_DIR", Path(__file__).resolve().parents[3]))


def _load_csv(filename: str) -> List[Dict[str, str]]:
    """Read a CSV file and return a list of row-dicts (all values are strings)."""
    path = _CSV_DIR / filename

    print(f"Current directory: {Path.cwd()}")
    print(f"Loading CSV: {path}")
    
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        return [row for row in reader]


def _index_by(rows: List[Dict], key: str) -> Dict[str, Dict]:
    """Return a dict keyed by *key* for O(1) lookups."""
    return {row[key]: row for row in rows}


# ── public stores (populated once at startup) ───────────────────────────────
products: List[Dict] = _load_csv("Products.csv")
product_categories: List[Dict] = _load_csv("ProductCategories.csv")
product_category_texts: List[Dict] = _load_csv("ProductCategoryTexts.csv")
product_texts: List[Dict] = _load_csv("ProductTexts.csv")
customers: List[Dict] = _load_csv("Customers.csv")
addresses: List[Dict] = _load_csv("Addresses.csv")
employees: List[Dict] = _load_csv("Employees.csv")
vendors: List[Dict] = _load_csv("Vendors.csv")
sales_orders: List[Dict] = _load_csv("SalesOrders.csv")
sales_order_items: List[Dict] = _load_csv("SalesOrderItems.csv")

# ── indexed look-ups ────────────────────────────────────────────────────────
products_by_id: Dict[str, Dict] = _index_by(products, "PRODUCTID")
product_categories_by_id: Dict[str, Dict] = _index_by(product_categories, "PRODCATEGORYID")
customers_by_id: Dict[str, Dict] = _index_by(customers, "CUSTOMERID")
addresses_by_id: Dict[str, Dict] = _index_by(addresses, "ADDRESSID")
employees_by_id: Dict[str, Dict] = _index_by(employees, "EMPLOYEEID")
vendors_by_id: Dict[str, Dict] = _index_by(vendors, "VENDORID")
sales_orders_by_id: Dict[str, Dict] = _index_by(sales_orders, "SALESORDERID")

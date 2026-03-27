"""In-memory data store – reads every CSV once at import time."""

from __future__ import annotations

import csv
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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


def _load_text_files(directory: str, suffix: str) -> Dict[str, str]:
    """Read text files in *directory* and return a dict keyed by stem."""
    path = _CSV_DIR / directory
    if not path.exists():
        return {}
    return {
        item.stem: item.read_text(encoding="utf-8")
        for item in path.glob(f"*{suffix}")
        if item.is_file()
    }

def _index_by(rows: List[Dict], key: str) -> Dict[str, Dict]:
    """Return a dict keyed by *key* for O(1) lookups."""
    return {row[key]: row for row in rows}


def _index_sales_order_items(rows: List[Dict]) -> Dict[Tuple[str, str], Dict]:
    return {(row["SALESORDERID"], row["SALESORDERITEM"]): row for row in rows}


def _index_category_texts(rows: List[Dict]) -> Dict[Tuple[str, str], Dict]:
    return {(row["PRODCATEGORYID"], row["LANGUAGE"]): row for row in rows}


def _stringify_row_values(row: Dict[str, object]) -> Dict[str, str]:
    return {key: "" if value is None else str(value) for key, value in row.items()}


def _update_indexed_row(index: Dict[str, Dict], row_id: str, changes: Dict[str, object]) -> Optional[Dict[str, str]]:
    row = index.get(row_id)
    if not row:
        return None

    row.update(_stringify_row_values(changes))
    return row


def _delete_indexed_row(rows: List[Dict], index: Dict[str, Dict], row_id: str) -> Optional[Dict[str, str]]:
    row = index.pop(row_id, None)
    if not row:
        return None

    rows.remove(row)
    return row


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
product_pages_by_id: Dict[str, str] = _load_text_files("product_pages", ".md")

# ── indexed look-ups ────────────────────────────────────────────────────────
products_by_id: Dict[str, Dict] = _index_by(products, "PRODUCTID")
product_categories_by_id: Dict[str, Dict] = _index_by(product_categories, "PRODCATEGORYID")
product_category_texts_by_id: Dict[Tuple[str, str], Dict] = _index_category_texts(product_category_texts)
customers_by_id: Dict[str, Dict] = _index_by(customers, "CUSTOMERID")
addresses_by_id: Dict[str, Dict] = _index_by(addresses, "ADDRESSID")
employees_by_id: Dict[str, Dict] = _index_by(employees, "EMPLOYEEID")
vendors_by_id: Dict[str, Dict] = _index_by(vendors, "VENDORID")
sales_orders_by_id: Dict[str, Dict] = _index_by(sales_orders, "SALESORDERID")
sales_order_items_by_id: Dict[Tuple[str, str], Dict] = _index_sales_order_items(sales_order_items)


def update_product(product_id: str, changes: Dict[str, object]) -> Optional[Dict[str, str]]:
    return _update_indexed_row(products_by_id, product_id, changes)


def delete_product(product_id: str) -> Optional[Dict[str, str]]:
    product = _delete_indexed_row(products, products_by_id, product_id)
    if not product:
        return None

    product_pages_by_id.pop(product_id, None)
    return product


def update_sales_order(order_id: str, changes: Dict[str, object]) -> Optional[Dict[str, str]]:
    return _update_indexed_row(sales_orders_by_id, order_id, changes)


def delete_sales_order(order_id: str) -> Optional[Dict[str, str]]:
    order = _delete_indexed_row(sales_orders, sales_orders_by_id, order_id)
    if not order:
        return None

    for item in [row for row in sales_order_items if row["SALESORDERID"] == order_id]:
        sales_order_items.remove(item)
        sales_order_items_by_id.pop((order_id, item["SALESORDERITEM"]), None)
    return order


def update_sales_order_item(
    order_id: str, item_id: str, changes: Dict[str, object]
) -> Optional[Dict[str, str]]:
    item = sales_order_items_by_id.get((order_id, item_id))
    if not item:
        return None

    item.update(_stringify_row_values(changes))
    return item


def delete_sales_order_item(order_id: str, item_id: str) -> Optional[Dict[str, str]]:
    item = sales_order_items_by_id.pop((order_id, item_id), None)
    if not item:
        return None

    sales_order_items.remove(item)
    return item


def update_vendor(vendor_id: str, changes: Dict[str, object]) -> Optional[Dict[str, str]]:
    return _update_indexed_row(vendors_by_id, vendor_id, changes)


def delete_vendor(vendor_id: str) -> Optional[Dict[str, str]]:
    return _delete_indexed_row(vendors, vendors_by_id, vendor_id)


def update_customer(customer_id: str, changes: Dict[str, object]) -> Optional[Dict[str, str]]:
    return _update_indexed_row(customers_by_id, customer_id, changes)


def delete_customer(customer_id: str) -> Optional[Dict[str, str]]:
    return _delete_indexed_row(customers, customers_by_id, customer_id)


def update_address(address_id: str, changes: Dict[str, object]) -> Optional[Dict[str, str]]:
    return _update_indexed_row(addresses_by_id, address_id, changes)


def delete_address(address_id: str) -> Optional[Dict[str, str]]:
    return _delete_indexed_row(addresses, addresses_by_id, address_id)


def update_product_category(category_id: str, changes: Dict[str, object]) -> Optional[Dict[str, str]]:
    return _update_indexed_row(product_categories_by_id, category_id, changes)


def delete_product_category(category_id: str) -> Optional[Dict[str, str]]:
    category = _delete_indexed_row(product_categories, product_categories_by_id, category_id)
    if not category:
        return None

    for key, row in list(product_category_texts_by_id.items()):
        if row["PRODCATEGORYID"] == category_id:
            product_category_texts.remove(row)
            product_category_texts_by_id.pop(key, None)
    return category


def update_product_category_text(
    category_id: str, language: str, changes: Dict[str, object]
) -> Optional[Dict[str, str]]:
    text = product_category_texts_by_id.get((category_id, language))
    if not text:
        return None

    text.update(_stringify_row_values(changes))
    return text


def delete_product_category_text(category_id: str, language: str) -> Optional[Dict[str, str]]:
    text = product_category_texts_by_id.pop((category_id, language), None)
    if not text:
        return None

    product_category_texts.remove(text)
    return text


def update_employee(employee_id: str, changes: Dict[str, object]) -> Optional[Dict[str, str]]:
    return _update_indexed_row(employees_by_id, employee_id, changes)


def delete_employee(employee_id: str) -> Optional[Dict[str, str]]:
    return _delete_indexed_row(employees, employees_by_id, employee_id)

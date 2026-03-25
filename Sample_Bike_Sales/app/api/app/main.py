"""Bike Sales Mock API – FastAPI application."""

from __future__ import annotations

from fastapi import FastAPI

from app.routers import (
    addresses,
    categories,
    customers,
    employees,
    products,
    sales_orders,
    vendors,
)

app = FastAPI(
    title="Bike Sales Mock API",
    description=(
        "A mock REST API serving Sample Bike Sales data entirely from "
        "in-memory CSV store. Protected by Microsoft Entra ID (Azure AD) "
        "via MSAL / JWT validation."
    ),
    version="1.0.0",
)

# ── register routers ────────────────────────────────────────────────────────
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(customers.router)
app.include_router(addresses.router)
app.include_router(employees.router)
app.include_router(vendors.router)
app.include_router(sales_orders.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "service": "Bike Sales Mock API"}


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}

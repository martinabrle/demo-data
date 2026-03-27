"""Customer endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from typing import Dict

from app.auth import validate_token
from app import datastore as ds

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.get("", summary="List customers")
def list_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    _claims: dict = Depends(validate_token),
):
    return ds.customers[skip : skip + limit]


@router.get("/{customer_id}", summary="Get customer by ID")
def get_customer(customer_id: str, _claims: dict = Depends(validate_token)):
    customer = ds.customers_by_id.get(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.patch("/{customer_id}", summary="Update customer")
def update_customer(
    customer_id: str,
    changes: Dict[str, object] = Body(...),
    _claims: dict = Depends(validate_token),
):
    if "CUSTOMERID" in changes and str(changes["CUSTOMERID"]) != customer_id:
        raise HTTPException(status_code=400, detail="CUSTOMERID in body must match path")

    customer = ds.update_customer(customer_id, changes)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.delete("/{customer_id}", summary="Delete customer")
def delete_customer(customer_id: str, _claims: dict = Depends(validate_token)):
    customer = ds.delete_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"deleted": True, "customer": customer}


@router.get("/{customer_id}/orders", summary="List orders for a customer")
def list_customer_orders(
    customer_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    _claims: dict = Depends(validate_token),
):
    orders = [o for o in ds.sales_orders if o.get("PARTNERID") == customer_id]
    return orders[skip : skip + limit]

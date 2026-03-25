"""Sales Order endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from app.auth import validate_token
from app import datastore as ds

router = APIRouter(prefix="/sales-orders", tags=["Sales Orders"])


@router.get("", summary="List sales orders")
def list_orders(
    partner_id: Optional[str] = Query(None, description="Filter by PARTNERID (customer)"),
    status: Optional[str] = Query(None, description="Filter by LIFECYCLESTATUS"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    _claims: dict = Depends(validate_token),
):
    items = ds.sales_orders
    if partner_id:
        items = [o for o in items if o.get("PARTNERID") == partner_id]
    if status:
        items = [o for o in items if o.get("LIFECYCLESTATUS") == status.upper()]
    return items[skip : skip + limit]


@router.get("/{order_id}", summary="Get sales order by ID")
def get_order(order_id: str, _claims: dict = Depends(validate_token)):
    order = ds.sales_orders_by_id.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Sales order not found")
    return order


@router.get("/{order_id}/items", summary="List items in a sales order")
def get_order_items(order_id: str, _claims: dict = Depends(validate_token)):
    items = [i for i in ds.sales_order_items if i["SALESORDERID"] == order_id]
    if not items:
        raise HTTPException(status_code=404, detail="No items found for this order")
    return items

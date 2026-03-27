"""Sales Order endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from typing import Dict, Optional

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


@router.patch("/{order_id}", summary="Update sales order")
def update_order(
    order_id: str,
    changes: Dict[str, object] = Body(...),
    _claims: dict = Depends(validate_token),
):
    if "SALESORDERID" in changes and str(changes["SALESORDERID"]) != order_id:
        raise HTTPException(status_code=400, detail="SALESORDERID in body must match path")

    order = ds.update_sales_order(order_id, changes)
    if not order:
        raise HTTPException(status_code=404, detail="Sales order not found")
    return order


@router.delete("/{order_id}", summary="Delete sales order")
def delete_order(order_id: str, _claims: dict = Depends(validate_token)):
    order = ds.delete_sales_order(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Sales order not found")
    return {"deleted": True, "sales_order": order}


@router.get("/{order_id}/items", summary="List items in a sales order")
def get_order_items(order_id: str, _claims: dict = Depends(validate_token)):
    items = [i for i in ds.sales_order_items if i["SALESORDERID"] == order_id]
    if not items:
        raise HTTPException(status_code=404, detail="No items found for this order")
    return items


@router.patch("/{order_id}/items/{item_id}", summary="Update sales order item")
def update_order_item(
    order_id: str,
    item_id: str,
    changes: Dict[str, object] = Body(...),
    _claims: dict = Depends(validate_token),
):
    if "SALESORDERID" in changes and str(changes["SALESORDERID"]) != order_id:
        raise HTTPException(status_code=400, detail="SALESORDERID in body must match path")
    if "SALESORDERITEM" in changes and str(changes["SALESORDERITEM"]) != item_id:
        raise HTTPException(status_code=400, detail="SALESORDERITEM in body must match path")

    item = ds.update_sales_order_item(order_id, item_id, changes)
    if not item:
        raise HTTPException(status_code=404, detail="Sales order item not found")
    return item


@router.delete("/{order_id}/items/{item_id}", summary="Delete sales order item")
def delete_order_item(order_id: str, item_id: str, _claims: dict = Depends(validate_token)):
    item = ds.delete_sales_order_item(order_id, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Sales order item not found")
    return {"deleted": True, "sales_order_item": item}

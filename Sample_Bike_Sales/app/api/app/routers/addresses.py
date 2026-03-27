"""Address endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from typing import Dict, Optional

from app.auth import validate_token
from app import datastore as ds

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.get("", summary="List addresses")
def list_addresses(
    country: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    _claims: dict = Depends(validate_token),
):
    items = ds.addresses
    if country:
        items = [a for a in items if a.get("COUNTRY") == country.upper()]
    return items[skip : skip + limit]


@router.get("/{address_id}", summary="Get address by ID")
def get_address(address_id: str, _claims: dict = Depends(validate_token)):
    addr = ds.addresses_by_id.get(address_id)
    if not addr:
        raise HTTPException(status_code=404, detail="Address not found")
    return addr


@router.patch("/{address_id}", summary="Update address")
def update_address(
    address_id: str,
    changes: Dict[str, object] = Body(...),
    _claims: dict = Depends(validate_token),
):
    if "ADDRESSID" in changes and str(changes["ADDRESSID"]) != address_id:
        raise HTTPException(status_code=400, detail="ADDRESSID in body must match path")

    addr = ds.update_address(address_id, changes)
    if not addr:
        raise HTTPException(status_code=404, detail="Address not found")
    return addr


@router.delete("/{address_id}", summary="Delete address")
def delete_address(address_id: str, _claims: dict = Depends(validate_token)):
    addr = ds.delete_address(address_id)
    if not addr:
        raise HTTPException(status_code=404, detail="Address not found")
    return {"deleted": True, "address": addr}

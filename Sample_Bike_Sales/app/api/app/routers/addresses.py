"""Address endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

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

"""Vendor endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth import validate_token
from app import datastore as ds

router = APIRouter(prefix="/vendors", tags=["Vendors"])


@router.get("", summary="List vendors")
def list_vendors(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    _claims: dict = Depends(validate_token),
):
    return ds.vendors[skip : skip + limit]


@router.get("/{vendor_id}", summary="Get vendor by ID")
def get_vendor(vendor_id: str, _claims: dict = Depends(validate_token)):
    vendor = ds.vendors_by_id.get(vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor

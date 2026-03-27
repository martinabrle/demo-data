"""Vendor endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from typing import Dict

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


@router.patch("/{vendor_id}", summary="Update vendor")
def update_vendor(
    vendor_id: str,
    changes: Dict[str, object] = Body(...),
    _claims: dict = Depends(validate_token),
):
    if "VENDORID" in changes and str(changes["VENDORID"]) != vendor_id:
        raise HTTPException(status_code=400, detail="VENDORID in body must match path")

    vendor = ds.update_vendor(vendor_id, changes)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor


@router.delete("/{vendor_id}", summary="Delete vendor")
def delete_vendor(vendor_id: str, _claims: dict = Depends(validate_token)):
    vendor = ds.delete_vendor(vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return {"deleted": True, "vendor": vendor}

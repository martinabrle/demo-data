"""Product endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional

from app.auth import validate_token
from app import datastore as ds

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", summary="List products")
def list_products(
    category: Optional[str] = Query(None, description="Filter by PRODCATEGORYID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    _claims: dict = Depends(validate_token),
):
    items = ds.products
    if category:
        items = [p for p in items if p.get("PRODCATEGORYID") == category]
    return items[skip : skip + limit]


@router.get("/{product_id}", summary="Get product by ID")
def get_product(product_id: str, _claims: dict = Depends(validate_token)):
    product = ds.products_by_id.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/{product_id}/texts", summary="Get product texts / descriptions")
def get_product_texts(
    product_id: str,
    language: Optional[str] = Query(None),
    _claims: dict = Depends(validate_token),
):
    texts = [t for t in ds.product_texts if t["PRODUCTID"] == product_id]
    if language:
        texts = [t for t in texts if t.get("LANGUAGE") == language.upper()]
    if not texts:
        raise HTTPException(status_code=404, detail="No texts found for this product")
    return texts

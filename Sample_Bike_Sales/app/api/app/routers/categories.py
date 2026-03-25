"""Product Category endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from app.auth import validate_token
from app import datastore as ds

router = APIRouter(prefix="/product-categories", tags=["Product Categories"])


@router.get("", summary="List product categories")
def list_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    _claims: dict = Depends(validate_token),
):
    return ds.product_categories[skip : skip + limit]


@router.get("/{category_id}", summary="Get product category by ID")
def get_category(category_id: str, _claims: dict = Depends(validate_token)):
    cat = ds.product_categories_by_id.get(category_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Product category not found")
    return cat


@router.get("/{category_id}/texts", summary="Get product category texts")
def get_category_texts(
    category_id: str,
    language: Optional[str] = Query(None),
    _claims: dict = Depends(validate_token),
):
    texts = [t for t in ds.product_category_texts if t["PRODCATEGORYID"] == category_id]
    if language:
        texts = [t for t in texts if t.get("LANGUAGE") == language.upper()]
    if not texts:
        raise HTTPException(status_code=404, detail="No texts found for this category")
    return texts


@router.get("/{category_id}/products", summary="List products in a category")
def list_products_in_category(
    category_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    _claims: dict = Depends(validate_token),
):
    items = [p for p in ds.products if p.get("PRODCATEGORYID") == category_id]
    return items[skip : skip + limit]

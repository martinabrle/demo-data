"""Employee endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth import validate_token
from app import datastore as ds

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("", summary="List employees")
def list_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
    _claims: dict = Depends(validate_token),
):
    return ds.employees[skip : skip + limit]


@router.get("/{employee_id}", summary="Get employee by ID")
def get_employee(employee_id: str, _claims: dict = Depends(validate_token)):
    emp = ds.employees_by_id.get(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

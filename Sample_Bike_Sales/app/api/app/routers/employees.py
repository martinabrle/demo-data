"""Employee endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Body, Depends, HTTPException, Query
from typing import Dict

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


@router.patch("/{employee_id}", summary="Update employee")
def update_employee(
    employee_id: str,
    changes: Dict[str, object] = Body(...),
    _claims: dict = Depends(validate_token),
):
    if "EMPLOYEEID" in changes and str(changes["EMPLOYEEID"]) != employee_id:
        raise HTTPException(status_code=400, detail="EMPLOYEEID in body must match path")

    emp = ds.update_employee(employee_id, changes)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@router.delete("/{employee_id}", summary="Delete employee")
def delete_employee(employee_id: str, _claims: dict = Depends(validate_token)):
    emp = ds.delete_employee(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"deleted": True, "employee": emp}

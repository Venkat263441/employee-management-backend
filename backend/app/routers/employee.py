from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models
from ..security import get_current_user
from ..database import get_db
from ..models.employee import Employee
from ..schemas.employee import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate,
)
from ..dependencies import require_admin




router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


@router.get("/protected")
def protected_employee_api(
    current_user: models.User = Depends(get_current_user)
):
    return {
        "message": "You are authorized",
        "user_id": current_user.id,
        "email": current_user.email,
        "role": current_user.role
    }

# =========================
# CREATE EMPLOYEE
# =========================

@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_employee(
    employee_data: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    # Check employee code
    existing_employee = (
        db.query(Employee)
        .filter(Employee.employee_code == employee_data.employee_code)
        .first()
    )

    if existing_employee:
        raise HTTPException(
            status_code=400,
            detail="Employee code already exists"
        )

    # Check email
    existing_email = (
        db.query(Employee)
        .filter(Employee.email == employee_data.email)
        .first()
    )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Employee email already exists"
        )

    employee = Employee(
        **employee_data.model_dump()
    )

    db.add(employee)
    db.commit()
    db.refresh(employee)

    return employee


# =========================
# GET ALL EMPLOYEES
# =========================

@router.get(
    "",
    response_model=list[EmployeeResponse]
)
def get_employees(
    db: Session = Depends(get_db)
):
    employees = (
        db.query(Employee)
        .order_by(Employee.id.desc())
        .all()
    )

    return employees


# =========================
# GET EMPLOYEE BY ID
# =========================

@router.get(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


# =========================
# UPDATE EMPLOYEE
# =========================

@router.put(
    "/{employee_id}",
    response_model=EmployeeResponse
)
def update_employee(
    employee_id: int,
    employee_data: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    update_data = employee_data.model_dump(
        exclude_unset=True
    )

    # Check email if email is being updated
    if "email" in update_data:

        existing_email = (
            db.query(Employee)
            .filter(
                Employee.email == update_data["email"],
                Employee.id != employee_id
            )
            .first()
        )

        if existing_email:
            raise HTTPException(
                status_code=400,
                detail="Employee email already exists"
            )

    # Update fields
    for field, value in update_data.items():
        setattr(employee, field, value)

    db.commit()
    db.refresh(employee)

    return employee


# =========================
# DELETE EMPLOYEE
# =========================

@router.delete(
    "/{employee_id}"
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    db.delete(employee)
    db.commit()

    return {
        "status": "success",
        "message": "Employee deleted successfully"
    }
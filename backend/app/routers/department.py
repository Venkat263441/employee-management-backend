from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..security import get_current_user
from ..database import get_db
from .. import models
from ..schemas import DepartmentCreate, DepartmentResponse
from ..dependencies import require_admin


router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


@router.post("/", response_model=DepartmentResponse)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    existing_department = (
        db.query(models.Department)
        .filter(models.Department.name == department.name)
        .first()
    )

    if existing_department:
        raise HTTPException(
            status_code=400,
            detail="Department already exists"
        )

    new_department = models.Department(
        name=department.name,
        description=department.description,
        is_active=True
    )

    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return new_department


@router.get("/", response_model=list[DepartmentResponse])
def get_departments(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)

):
    return db.query(models.Department).all()


@router.put("/{department_id}")
def update_department(
    department_id: int,
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    existing_department = (
        db.query(models.Department)
        .filter(models.Department.id == department_id)
        .first()
    )

    if existing_department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    existing_department.name = department.name
    existing_department.description = department.description

    db.commit()
    db.refresh(existing_department)

    return existing_department


@router.delete("/{department_id}")
def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    department = (
        db.query(models.Department)
        .filter(models.Department.id == department_id)
        .first()
    )

    if department is None:
        raise HTTPException(
            status_code=404,
            detail="Department not found"
        )

    db.delete(department)
    db.commit()

    return {
        "message": "Department deleted successfully"
    }


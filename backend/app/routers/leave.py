from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models
from ..schemas import (
    LeaveCreate,
    LeaveUpdate,
    LeaveResponse
)
from ..security import get_current_user
from ..dependencies import require_admin


router = APIRouter(
    prefix="/leaves",
    tags=["Leave Management"]
)


# =========================================================
# CREATE LEAVE
# =========================================================

@router.post("/", response_model=LeaveResponse)
def create_leave(
    leave: LeaveCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    employee = (
        db.query(models.Employee)
        .filter(
            models.Employee.id == leave.employee_id
        )
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    if leave.start_date > leave.end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be after end date"
        )

    new_leave = models.Leave(
        employee_id=leave.employee_id,
        leave_type=leave.leave_type,
        start_date=leave.start_date,
        end_date=leave.end_date,
        reason=leave.reason,
        status="PENDING"
    )

    db.add(new_leave)
    db.commit()
    db.refresh(new_leave)

    return new_leave


# =========================================================
# GET ALL LEAVES
# =========================================================

@router.get("/", response_model=list[LeaveResponse])
def get_leaves(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    return (
        db.query(models.Leave)
        .order_by(models.Leave.id.desc())
        .all()
    )


# =========================================================
# GET LEAVE BY ID
# =========================================================

@router.get("/{leave_id}", response_model=LeaveResponse)
def get_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    leave = (
        db.query(models.Leave)
        .filter(models.Leave.id == leave_id)
        .first()
    )

    if leave is None:
        raise HTTPException(
            status_code=404,
            detail="Leave record not found"
        )

    return leave


# =========================================================
# UPDATE LEAVE
# =========================================================

@router.put("/{leave_id}", response_model=LeaveResponse)
def update_leave(
    leave_id: int,
    leave_data: LeaveUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    leave = (
        db.query(models.Leave)
        .filter(models.Leave.id == leave_id)
        .first()
    )

    if leave is None:
        raise HTTPException(
            status_code=404,
            detail="Leave record not found"
        )

    if leave_data.start_date > leave_data.end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date cannot be after end date"
        )

    leave.leave_type = leave_data.leave_type
    leave.start_date = leave_data.start_date
    leave.end_date = leave_data.end_date
    leave.reason = leave_data.reason
    leave.status = leave_data.status
    leave.remarks = leave_data.remarks

    db.commit()
    db.refresh(leave)

    return leave


# =========================================================
# DELETE LEAVE
# =========================================================

@router.delete("/{leave_id}")
def delete_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):

    leave = (
        db.query(models.Leave)
        .filter(models.Leave.id == leave_id)
        .first()
    )

    if leave is None:
        raise HTTPException(
            status_code=404,
            detail="Leave record not found"
        )

    db.delete(leave)
    db.commit()

    return {
        "message": "Leave deleted successfully"
    }


# =========================================================
# APPROVE LEAVE
# =========================================================

@router.put("/{leave_id}/approve", response_model=LeaveResponse)
def approve_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):

    leave = (
        db.query(models.Leave)
        .filter(models.Leave.id == leave_id)
        .first()
    )

    if leave is None:
        raise HTTPException(
            status_code=404,
            detail="Leave record not found"
        )

    if leave.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail="Only pending leaves can be approved"
        )

    leave.status = "APPROVED"
    leave.remarks = "Leave approved by admin"

    db.commit()
    db.refresh(leave)

    return leave


# =========================================================
# REJECT LEAVE
# =========================================================

@router.put("/{leave_id}/reject", response_model=LeaveResponse)
def reject_leave(
    leave_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):

    leave = (
        db.query(models.Leave)
        .filter(models.Leave.id == leave_id)
        .first()
    )

    if leave is None:
        raise HTTPException(
            status_code=404,
            detail="Leave record not found"
        )

    if leave.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail="Only pending leaves can be rejected"
        )

    leave.status = "REJECTED"
    leave.remarks = "Leave rejected by admin"

    db.commit()
    db.refresh(leave)

    return leave
from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models
from ..dependencies import require_admin


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def get_dashboard_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    total_users = db.query(models.User).count()

    total_employees = db.query(models.Employee).count()

    active_employees = (
        db.query(models.Employee)
        .filter(models.Employee.status == "ACTIVE")
        .count()
    )

    inactive_employees = (
        db.query(models.Employee)
        .filter(models.Employee.status != "ACTIVE")
        .count()
    )

    total_departments = db.query(models.Department).count()

    today = date.today()

    today_attendance = (
        db.query(models.Attendance)
        .filter(models.Attendance.attendance_date == today)
        .count()
    )

    present_today = (
        db.query(models.Attendance)
        .filter(
            models.Attendance.attendance_date == today,
            models.Attendance.status == "PRESENT"
        )
        .count()
    )

    absent_today = (
        db.query(models.Attendance)
        .filter(
            models.Attendance.attendance_date == today,
            models.Attendance.status == "ABSENT"
        )
        .count()
    )

    total_leaves = db.query(models.Leave).count()

    pending_leaves = (
        db.query(models.Leave)
        .filter(models.Leave.status == "PENDING")
        .count()
    )

    approved_leaves = (
        db.query(models.Leave)
        .filter(models.Leave.status == "APPROVED")
        .count()
    )

    rejected_leaves = (
        db.query(models.Leave)
        .filter(models.Leave.status == "REJECTED")
        .count()
    )

    return {
        "users": {
            "total": total_users
        },

        "employees": {
            "total": total_employees,
            "active": active_employees,
            "inactive": inactive_employees
        },

        "departments": {
            "total": total_departments
        },

        "attendance": {
            "today": today_attendance,
            "present": present_today,
            "absent": absent_today
        },

        "leaves": {
            "total": total_leaves,
            "pending": pending_leaves,
            "approved": approved_leaves,
            "rejected": rejected_leaves
        }
    }


@router.get("/attendance")
def get_attendance_report(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    total_attendance = db.query(models.Attendance).count()

    present = (
        db.query(models.Attendance)
        .filter(models.Attendance.status == "PRESENT")
        .count()
    )

    absent = (
        db.query(models.Attendance)
        .filter(models.Attendance.status == "ABSENT")
        .count()
    )

    late = (
        db.query(models.Attendance)
        .filter(models.Attendance.status == "LATE")
        .count()
    )

    leave = (
        db.query(models.Attendance)
        .filter(models.Attendance.status == "LEAVE")
        .count()
    )

    return {
        "total_attendance": total_attendance,
        "present": present,
        "absent": absent,
        "late": late,
        "leave": leave
    }


@router.get("/leaves")
def get_leave_report(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    total_leaves = db.query(models.Leave).count()

    pending = (
        db.query(models.Leave)
        .filter(models.Leave.status == "PENDING")
        .count()
    )

    approved = (
        db.query(models.Leave)
        .filter(models.Leave.status == "APPROVED")
        .count()
    )

    rejected = (
        db.query(models.Leave)
        .filter(models.Leave.status == "REJECTED")
        .count()
    )

    return {
        "total_leaves": total_leaves,
        "pending": pending,
        "approved": approved,
        "rejected": rejected
    }


@router.get("/employees")
def get_employee_report(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    total_employees = db.query(models.Employee).count()

    active_employees = (
        db.query(models.Employee)
        .filter(models.Employee.status == "ACTIVE")
        .count()
    )

    inactive_employees = (
        db.query(models.Employee)
        .filter(models.Employee.status != "ACTIVE")
        .count()
    )

    return {
        "total_employees": total_employees,
        "active_employees": active_employees,
        "inactive_employees": inactive_employees
    }


@router.get("/departments")
def get_department_report(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_admin)
):
    departments = db.query(models.Department).all()

    result = []

    for department in departments:

        employee_count = (
            db.query(models.Employee)
            .filter(
                models.Employee.department_id == department.id
            )
            .count()
        )

        result.append({
            "department_id": department.id,
            "department_name": department.name,
            "employee_count": employee_count
        })

    return result
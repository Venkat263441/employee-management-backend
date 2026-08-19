from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict


class AttendanceCreate(BaseModel):
    employee_id: int
    attendance_date: date
    check_in: time | None = None
    check_out: time | None = None
    status: str = "PRESENT"
    remarks: str | None = None


class AttendanceResponse(BaseModel):
    id: int
    employee_id: int
    attendance_date: date
    check_in: time | None
    check_out: time | None
    status: str
    remarks: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AttendanceUpdate(BaseModel):
    employee_id: int
    attendance_date: date
    check_in: time | None = None
    check_out: time | None = None
    status: str
    remarks: str | None = None

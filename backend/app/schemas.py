from datetime import date, datetime, time
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "EMPLOYEE"

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class DepartmentCreate(BaseModel):
    name: str
    description: str | None = None


class DepartmentResponse(BaseModel):
    id: int
    name: str
    description: str | None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EmployeeCreate(BaseModel):
    employee_code: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None
    date_of_birth: date | None = None
    gender: str | None = None
    department_id: int
    designation: str
    joining_date: date
    salary: Decimal | None = None
    address: str | None = None
    profile_image: str | None = None
    status: str = "ACTIVE"


class EmployeeUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    date_of_birth: date | None = None
    gender: str | None = None
    department_id: int | None = None
    designation: str | None = None
    joining_date: date | None = None
    salary: Decimal | None = None
    address: str | None = None
    profile_image: str | None = None
    status: str | None = None


class EmployeeResponse(BaseModel):
    id: int
    employee_code: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None
    date_of_birth: date | None
    gender: str | None
    department_id: int
    designation: str
    joining_date: date
    salary: Decimal | None
    address: str | None
    profile_image: str | None
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)






class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str



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

    class Config:
        from_attributes = True


class AttendanceUpdate(BaseModel):
    employee_id: int
    attendance_date: date
    check_in: time | None = None
    check_out: time | None = None
    status: str
    remarks: str | None = None



class LeaveCreate(BaseModel):
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: str | None = None


class LeaveUpdate(BaseModel):
    leave_type: str
    start_date: date
    end_date: date
    reason: str | None = None
    status: str
    remarks: str | None = None


class LeaveResponse(BaseModel):
    id: int
    employee_id: int
    leave_type: str
    start_date: date
    end_date: date
    reason: str | None
    status: str
    remarks: str | None

    class Config:
        from_attributes = True

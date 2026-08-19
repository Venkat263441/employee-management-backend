from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr


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

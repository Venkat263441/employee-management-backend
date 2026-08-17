from fastapi import FastAPI
from sqlalchemy import text

from .database import Base, engine
from . import models
from .routers import employee,department,user, auth,attendance,leave,dashboard


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Employee Management System API",
    description="Backend API for Employee Management System",
    version="1.0.0"
)


app.include_router(
    employee.router
)
app.include_router(
    department.router
)
app.include_router(
    user.router
)

app.include_router(
    auth.router
)

app.include_router(
    attendance.router
)

app.include_router(
    leave.router
)

app.include_router(
    dashboard.router
)

@app.get("/health")
def health_check():

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "success",
            "message": "Employee Management API is running",
            "database": "PostgreSQL connected"
        }

    except Exception as e:

        return {
            "status": "error",
            "message": "Database connection failed",
            "error": str(e)
        }
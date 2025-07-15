from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, computed_field, EmailStr
from typing import Annotated, Optional
import json
from datetime import date, datetime
from decimal import Decimal
from fastapi.responses import JSONResponse

# Initialize FastAPI app
app = FastAPI(title="Employee Records Management API")

# Pydantic model for Employee with raw and computed fields
class Employee(BaseModel):
    id: Annotated[str, Field(..., description="Unique ID of the employee, e.g., E001", pattern="^E[0-9]{3}$")]
    name: Annotated[str, Field(..., min_length=1, description="Name of the employee")]
    email: Annotated[EmailStr, Field(..., description="Email of the employee")]
    department: Annotated[str, Field(..., min_length=1, description="Department of the employee")]
    date_joined: Annotated[date, Field(..., description="Date the employee joined")]
    salary: Annotated[Decimal, Field(..., gt=0, decimal_places=2, description="Salary of the employee")]

    @computed_field
    def name_upper(self) -> str:
        """Convert name to uppercase."""
        return self.name.upper()

    @computed_field
    def email_masked(self) -> str:
        """Mask the email for privacy."""
        parts = self.email.split('@')
        return f"{parts[0][:2]}***@{parts[1]}" if len(parts) > 1 else self.email

    @computed_field
    def name_reversed(self) -> str:
        """Reverse the name string."""
        return self.name[::-1]

    @computed_field
    def department_title(self) -> str:
        """Convert department to title case."""
        return self.department.title()

    @computed_field
    def date_joined_formatted(self) -> str:
        """Format date as DD-MM-YYYY."""
        return self.date_joined.strftime("%d-%m-%Y")

    @computed_field
    def salary_with_currency(self) -> str:
        """Add currency symbol to salary."""
        return f"₹{self.salary}"

    @computed_field
    def time_since_joined(self) -> str:
        """Approximate time since the date joined."""
        delta = datetime.now().date() - self.date_joined
        days = delta.days
        if days < 30:
            return f"{days} days"
        elif days < 365:
            return f"{days // 30} months"
        else:
            return f"{days // 365} years"

# Pydantic model for updating employee data (partial updates)
class UpdateEmployee(BaseModel):
    name: Annotated[Optional[str], Field(None, min_length=1)]
    email: Annotated[Optional[EmailStr], Field(None)]
    department: Annotated[Optional[str], Field(None, min_length=1)]
    date_joined: Annotated[Optional[date], Field(None)]
    salary: Annotated[Optional[Decimal], Field(None, gt=0, decimal_places=2)]

# Utility functions for JSON file handling
def load_data():
    try:
        with open('employees.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid JSON in employees.json")

def save_data(data):
    try:
        with open('employees.json', 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save data: {str(e)}")

# API Endpoints
@app.get("/", summary="Welcome Message")
async def hello():
    return {"message": "Employee Records Management API"}

@app.get("/about", summary="About the API")
async def about():
    return {"message": "A fully functional API to manage employee records with formatted data."}

@app.get("/employees", summary="List All Employees")
async def list_employees():
    data = load_data()
    employees = [Employee(**emp, id=emp_id) for emp_id, emp in data.items()]
    return employees

@app.get("/employees/{employee_id}", summary="Get Employee by ID")
async def get_employee(employee_id: str):
    data = load_data()
    if employee_id not in data:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee = Employee(**data[employee_id], id=employee_id)
    return employee

@app.post("/employees", summary="Create Employee", status_code=201)
async def create_employee(employee: Employee):
    data = load_data()
    if employee.id in data:
        raise HTTPException(status_code=400, detail="Employee already exists")
    data[employee.id] = employee.model_dump(exclude={'id'})
    save_data(data)
    return JSONResponse(status_code=201, content={"message": "Employee created successfully"})

@app.put("/employees/{employee_id}", summary="Update Employee")
async def update_employee(employee_id: str, employee_update: UpdateEmployee):
    data = load_data()
    if employee_id not in data:
        raise HTTPException(status_code=404, detail="Employee not found")
    existing_employee = data[employee_id]
    update_data = employee_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        existing_employee[key] = value
    # Recreate Employee object to recompute fields
    existing_employee['id'] = employee_id
    updated_employee = Employee(**existing_employee)
    data[employee_id] = updated_employee.model_dump(exclude={'id'})
    save_data(data)
    return JSONResponse(status_code=200, content={"message": "Employee updated successfully"})

@app.delete("/employees/{employee_id}", summary="Delete Employee")
async def delete_employee(employee_id: str):
    data = load_data()
    if employee_id not in data:
        raise HTTPException(status_code=404, detail="Employee not found")
    del data[employee_id]
    save_data(data)
    return JSONResponse(status_code=200, content={"message": "Employee deleted successfully"})




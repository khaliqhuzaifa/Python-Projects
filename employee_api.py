from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List

app  = FastAPI()

class Employee(BaseModel):
    id: int
    name: str
    department: str
    salary: float = Field(gt=0)

employees: List[Employee] = []

@app.get("/")
def home_page():
    return {"message": "Employee API is running"}

@app.get("/employees")
def get_all_employees():
    return employees

@app.get("/employees/{employee_id}")
def get_one_employee(employee_id: int):
    for employee in employees:
        if employee.id == employee_id:
            return employee
    raise HTTPException(status_code=404, detail="Employee not found!")

@app.post("/employees", status_code=201)
def add_employee(employee: Employee):
    if any(e.id == employee.id for e in employees):
        raise HTTPException(status_code=400, detail="Employee ID already exists!")
    employees.append(employee)
    return employee


@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, updated_employee: Employee):
    for index, employee in enumerate(employees):
        if employee.id == employee_id:
            employees[index] = updated_employee
            return updated_employee
    raise HTTPException(status_code=404, detail="Employee not found!")

@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    for index, employee in enumerate(employees):
        if employee.id == employee_id:
            deleted_employee = employees.pop(index)
            return deleted_employee
    raise HTTPException(status_code=404, detail="Employee not found!")

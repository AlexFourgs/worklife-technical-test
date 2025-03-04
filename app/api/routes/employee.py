from typing import Optional
from uuid import UUID

from fastapi import (
    Depends,
    APIRouter,
)
from sqlalchemy.orm import Session
from starlette import status

from app.db.session import get_db
from app.repository.employee import EmployeeRepository
from app.schema import EmployeeBase

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK)
def get_all(session: Session = Depends(get_db)):
    return EmployeeRepository.get_many(session=session)


@router.get("/{employee_id}", status_code=status.HTTP_200_OK)
def get_employee(session: Session = Depends(get_db), *, employee_id: UUID):
    return EmployeeRepository.get(session=session, id=employee_id)


@router.get("/team/{team_id}", status_code=status.HTTP_200_OK)
def get_employee_by_team_id(session: Session = Depends(get_db), *, team_id: UUID):
    return EmployeeRepository.get_many(session=session, team_id=team_id)


@router.post("/employee", status_code=status.HTTP_201_CREATED)
def create_employee(employee: EmployeeBase, session: Session = Depends(get_db)):
    return EmployeeRepository.create(session=session, obj_in=employee)

from datetime import date
from typing import Optional
from uuid import UUID

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app.db.session import get_db
from app.repository.vacation import VacationRepository
from app.repository.employee import EmployeeRepository
from app.schema import VacationBase

router = APIRouter()


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=Optional[list[VacationBase]]
)
def get_all(session: Session = Depends(get_db)):
    return VacationRepository.get_many(session=session)


@router.get(
    "/{vacation_id}",
    status_code=status.HTTP_200_OK,
    response_model=Optional[VacationBase],
)
def get_vacation(session: Session = Depends(get_db), *, vacation_id: UUID):
    return VacationRepository.get(session=session, id=vacation_id)


@router.get(
    "/search/employee",
    status_code=status.HTTP_200_OK,
    response_model=Optional[list[VacationBase]],
)
def search_vacation_by_employee(
    session: Session = Depends(get_db), *, employee_id: UUID
):
    return VacationRepository.get_many(session=session, employee_id=employee_id)


@router.get(
    "/search/dates_range",
    status_code=status.HTTP_200_OK,
    response_model=Optional[list[VacationBase]],
)
def search_vacation_by_dates(
    session: Session = Depends(get_db),
    *,
    start_date: date,
    end_date: date,
):
    return VacationRepository.get_by_dates_range(
        session=session, start_date=start_date, end_date=end_date
    )


@router.get(
    "/search/team",
    status_code=status.HTTP_200_OK,
    response_model=Optional[list[VacationBase]],
)
def search_vacation_by_team(session: Session = Depends(get_db), *, team_id: UUID):
    return VacationRepository.get_by_team(session=session, team_id=team_id)


@router.post("/vacation", status_code=status.HTTP_201_CREATED)
def create_vacation(vacation: VacationBase, session: Session = Depends(get_db)):
    return VacationRepository.create(session=session, obj_in=vacation)


@router.delete("/{vacation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vacation(session: Session = Depends(get_db), *, vacation_id: UUID):
    VacationRepository.delete(session=session, vacation_id=vacation_id)


@router.put("/{vacation_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_vacation(
    vacation: VacationBase, session: Session = Depends(get_db), *, vacation_id: UUID
):
    VacationRepository.update(session=session, vacation_id=vacation_id, obj_in=vacation)

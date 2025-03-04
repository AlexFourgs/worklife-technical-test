from datetime import date, timedelta

from fastapi import HTTPException
from sqlalchemy import desc, or_, and_

from app.model import VacationModel
from app.repository.base import BaseRepository
from app.repository.employee import EmployeeRepository


class _VacationRepository(BaseRepository):

    def __date_in_range(
        self, current_date: date, lower_range_date: date, higher_range_date: date
    ) -> bool:
        """Check if a given date is in a given range of dates:

        lower_range_date <= current_date <= higher_range_date

        Parameters
        ----------
        current_date : date
            The date to test.
        lower_range_date : date
        higher_range_date : date

        Returns
        -------
        bool
            True if the date is in the range, else False.
        """
        return (current_date >= lower_range_date - timedelta(days=1)) and (
            current_date <= higher_range_date + timedelta(days=1)
        )

    def __calculate_correct_dates(
        self,
        new_start_date: date,
        new_end_date: date,
        existing_start_date: date,
        existing_end_date: date,
    ) -> tuple[date, date]:
        """Calculates new dates to keep in case of overlap.

        Parameters
        ----------
        new_start_date : date
            The new entry starting date
        new_end_date : date
            The new entry ending date
        existing_start_date : date
            The old entry starting date
        existing_end_date : date
            The old entry ending date

        Returns
        -------
        tuple[date, date]
            The correct start_date and end_date for the new entry.
        """
        start_date = new_start_date
        end_date = new_end_date

        # new vacations include old vacations
        if (new_start_date <= existing_start_date - timedelta(days=1)) and (
            new_end_date >= existing_end_date + timedelta(days=1)
        ):
            return start_date, end_date

        # other cases
        if self.__date_in_range(new_start_date, existing_start_date, existing_end_date):
            start_date = existing_start_date

        if self.__date_in_range(new_end_date, existing_start_date, existing_end_date):
            end_date = existing_end_date

        return start_date, end_date

    def __manage_overlap(self, session, obj_in):
        # Retrieving existing vacation for the employee within date ranges of the new entry

        employee_vacations = (
            session.query(self.model)
            .filter(
                (self.model.employee_id == obj_in.employee_id),
                (self.model.paid == obj_in.paid),
            )
            .filter(
                or_(
                    and_(
                        (
                            (self.model.start_date - timedelta(days=1))
                            <= obj_in.end_date
                        ),
                        ((self.model.end_date + timedelta(days=1)) >= obj_in.end_date),
                    ),
                    and_(
                        (
                            (self.model.start_date - timedelta(days=1))
                            <= obj_in.start_date
                        ),
                        (
                            (self.model.end_date + timedelta(days=1))
                            >= obj_in.start_date
                        ),
                    ),
                ),
            )
            .order_by(desc(self.model.start_date))
        )

        # Calculating correct dates for new entry based on old entries dates
        vacation_to_delete = []
        for existing_vacation in employee_vacations:
            start_date, end_date = self.__calculate_correct_dates(
                obj_in.start_date,
                obj_in.end_date,
                existing_vacation.start_date,
                existing_vacation.end_date,
            )

            vacation_to_delete.append(existing_vacation)
            obj_in.start_date = start_date
            obj_in.end_date = end_date

        return vacation_to_delete

    def get_by_id(self, session, vacation_id):
        return self.get(session, self.model.id == vacation_id)

    def get_by_dates_range(self, session, start_date, end_date):
        return session.query(self.model).filter(
            (self.model.start_date <= start_date), (self.model.end_date >= end_date)
        )

    def get_by_team(self, session, team_id):
        # First retrieving employees id in team
        employee_on_team = EmployeeRepository.get_many(session, team_id=team_id)

        # Then filtering vacations on those ids
        all_vacations = []
        for employee in employee_on_team:

            current_employee_vacation = self.get_many(
                session=session, employee_id=employee.id
            )

            if current_employee_vacation:
                all_vacations.extend(current_employee_vacation)

        return all_vacations

    def delete(self, session, vacation_id):
        session.query(self.model).filter(self.model.id == vacation_id).delete()

    def update(self, session, vacation_id, obj_in):
        """Update an entry in the vacation table.

        1. Calculate overlap with existing vacations based on employee_id, type and dates
        2. Delete old entries if necessary
        3. Update entry

        Parameters
        ----------
        session

        obj_in
        """

        vacation_to_delete = self.__manage_overlap(session=session, obj_in=obj_in)

        # Deleting old entries which will be merged with new entry except for entry we'll modify
        for vacation in vacation_to_delete:
            if vacation.id != vacation_id:
                self.delete(session=session, vacation_id=vacation.id)

        obj = self.get(session=session, id=vacation_id)

        obj.start_date = obj_in.start_date
        obj.end_date = obj_in.end_date
        obj.paid = obj_in.paid
        obj.employee_id = obj_in.employee_id

        session.add(obj)

    def create(self, session, obj_in):
        """Create a new entry in the vacation table.

        1. Calculate overlap with existing vacations based on employee_id, type and dates
        2. Delete old entries if necessary
        3. Create new entry

        Parameters
        ----------
        session

        obj_in
        """
        vacation_to_delete = self.__manage_overlap(session=session, obj_in=obj_in)

        # Deleting old entries which will be merged with new entry
        for vacation in vacation_to_delete:
            self.delete(session=session, vacation_id=vacation.id)

        # Creating new entry
        new_obj = self.model(**obj_in.model_dump())
        session.add(new_obj)
        session.flush()
        return {"id": new_obj.id}


VacationRepository = _VacationRepository(model=VacationModel)

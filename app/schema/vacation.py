from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class VacationBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    start_date: date
    end_date: date
    paid: bool
    employee_id: UUID

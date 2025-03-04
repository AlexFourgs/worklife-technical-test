import sqlalchemy as sa
from .base import BaseModel, CustomUUID


class VacationModel(BaseModel):
    __tablename__ = "vacation"
    start_date = sa.Column(sa.Date)
    end_date = sa.Column(sa.Date)
    paid = sa.Column(sa.Boolean)
    employee_id = sa.Column(CustomUUID, sa.ForeignKey("employee.id"))

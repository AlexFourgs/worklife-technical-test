import sqlalchemy as sa
from .base import BaseModel, CustomUUID


class EmployeeModel(BaseModel):
    __tablename__ = "employee"
    first_name = sa.Column(sa.String)
    last_name = sa.Column(sa.String)
    team_id = sa.Column(CustomUUID, sa.ForeignKey("team.id"))

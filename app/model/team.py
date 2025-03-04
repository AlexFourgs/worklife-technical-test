import sqlalchemy as sa
from .base import BaseModel


class TeamModel(BaseModel):
    __tablename__ = "team"
    name = sa.Column(sa.String, unique=True)

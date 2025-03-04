from pydantic import BaseModel, ConfigDict


class TeamBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str

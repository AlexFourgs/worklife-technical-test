from typing import Optional
from uuid import UUID

from fastapi import (
    Depends,
    APIRouter,
)
from sqlalchemy.orm import Session
from starlette import status

from app.db.session import get_db
from app.repository.team import TeamRepository
from app.schema import TeamBase

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=Optional[list])
def get_all(session: Session = Depends(get_db)):
    repo = TeamRepository.get_many(session=session)
    all_teams = []
    for t in repo:
        current_team = {"id": t.id, "name": t.name}
        all_teams.append(current_team)

    return all_teams


@router.get("/{team_id}", status_code=status.HTTP_200_OK)
def get_team(session: Session = Depends(get_db), *, team_id: UUID):
    return TeamRepository.get(session=session, id=team_id)


@router.post("/team", status_code=status.HTTP_201_CREATED)
def create_team(team: TeamBase, session=Depends(get_db)):
    return TeamRepository.create(session=session, obj_in=team)

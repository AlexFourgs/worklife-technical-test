from fastapi import status

from .utils import *
from . import settings

# Using global variables / constant as I was unable
# to use fixtures due to a lack of knowledges on how
# to handle the connection/session with database in tests.
REQUEST_DATA = {"name": "TEST"}


def test_create_team():
    response = client.post("/team/team", json=REQUEST_DATA)
    assert response.status_code == status.HTTP_201_CREATED
    settings.team_test_id = response.json()["id"]


def test_get_team():
    team_test = dict(REQUEST_DATA)
    team_test["id"] = settings.team_test_id
    response = client.get("/team")
    assert response.status_code == status.HTTP_200_OK
    assert team_test in response.json()

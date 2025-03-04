from fastapi import status

from .utils import *
from . import settings

# Using global variables / constant as I was unable
# to use fixtures due to a lack of knowledges on how
# to handle the connection/session with database in tests.
REQUEST_DATA = {
    "first_name": "John",
    "last_name": "Doe",
    "team_id": None,
}


def test_create_employee():
    REQUEST_DATA["team_id"] = settings.team_test_id
    response = client.post("/employee/employee", json=REQUEST_DATA)
    assert response.status_code == status.HTTP_201_CREATED
    settings.employee_test_id = response.json()["id"]


def test_get_employee():
    employee_test = dict(REQUEST_DATA)
    employee_test["id"] = settings.employee_test_id
    response = client.get("/employee")
    assert response.status_code == status.HTTP_200_OK
    assert employee_test in response.json()

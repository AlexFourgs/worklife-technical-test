from sqlalchemy import text
from fastapi import status

from .utils import *
from . import settings

# Using global variables / constant as I was unable
# to use fixtures due to a lack of knowledges on how
# to handle the connection/session with database in tests.
REQUEST_DATA_CREATE_1 = {
    "start_date": "2025-02-05",
    "end_date": "2025-02-10",
    "paid": True,
    "employee_id": None,
}
REQUEST_DATA_CREATE_2 = {
    "start_date": "2025-02-20",
    "end_date": "2025-02-25",
    "paid": True,
    "employee_id": None,
}
REQUEST_DATA_CREATE_3 = {
    "start_date": "2025-02-08",
    "end_date": "2025-02-15",
    "paid": True,
    "employee_id": None,
}

REQUEST_DATA_UPDATE = {
    "start_date": "2025-02-16",
    "end_date": "2025-02-25",
    "paid": True,
    "employee_id": None,
}

DATA_MERGED_1 = {
    "start_date": "2025-02-05",
    "end_date": "2025-02-15",
    "paid": True,
    "employee_id": None,
}
DATA_MERGED_2 = {
    "start_date": "2025-02-05",
    "end_date": "2025-02-25",
    "paid": True,
    "employee_id": None,
}


vacations_test_id = []


def test_create_vacations():
    global vacations_test_id
    REQUEST_DATA_CREATE_1["employee_id"] = settings.employee_test_id
    response = client.post("/vacation/vacation", json=REQUEST_DATA_CREATE_1)
    assert response.status_code == status.HTTP_201_CREATED
    vacations_test_id.append(response.json()["id"])

    REQUEST_DATA_CREATE_2["employee_id"] = settings.employee_test_id
    response = client.post("/vacation/vacation", json=REQUEST_DATA_CREATE_2)
    assert response.status_code == status.HTTP_201_CREATED
    vacations_test_id.append(response.json()["id"])


def test_get_vacations():
    response = client.get("/vacation")
    assert response.status_code == status.HTTP_200_OK


def test_create_vacation_with_overlap():
    global vacations_test_id
    REQUEST_DATA_CREATE_3["employee_id"] = settings.employee_test_id

    response = client.post("/vacation/vacation", json=REQUEST_DATA_CREATE_3)
    assert response.status_code == status.HTTP_201_CREATED
    vacations_test_id.append(response.json()["id"])


def test_get_vacations_merged():
    DATA_MERGED_1["employee_id"] = settings.employee_test_id

    vacation_test_1 = dict(REQUEST_DATA_CREATE_1)
    vacation_test_merged = dict(DATA_MERGED_1)

    response = client.get("/vacation")
    assert response.status_code == status.HTTP_200_OK
    assert vacation_test_1 not in response.json()
    assert vacation_test_merged in response.json()


def test_update_vacation():
    REQUEST_DATA_UPDATE["employee_id"] = settings.employee_test_id
    response = client.put(f"/vacation/{vacations_test_id[2]}", json=REQUEST_DATA_UPDATE)
    assert response.status_code == status.HTTP_204_NO_CONTENT


def test_get_vacations_merged_after_update():
    DATA_MERGED_2["employee_id"] = settings.employee_test_id

    vacation_test_1 = dict(REQUEST_DATA_CREATE_2)
    vacation_test_merged = dict(DATA_MERGED_2)

    response = client.get("/vacation")
    assert response.status_code == status.HTTP_200_OK
    assert vacation_test_1 not in response.json()
    assert vacation_test_merged in response.json()


def test_delete_vacation():
    response = client.delete(f"/vacation/{vacations_test_id[2]}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

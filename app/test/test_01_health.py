from fastapi import status

from .utils import *


def test_return_health_check():
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.text == '"OK"'

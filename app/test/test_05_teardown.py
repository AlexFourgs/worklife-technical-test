from sqlalchemy import text

from .utils import *
from . import settings


def test_employee_teardown():
    pass
    connection = engine.connect()
    connection.execute(
        text(f"DELETE FROM employee WHERE id='{settings.employee_test_id}';")
    )
    connection.commit()


def test_team_teardown():
    pass
    connection = engine.connect()
    connection.execute(text(f"DELETE FROM team WHERE id='{settings.team_test_id}';"))
    connection.commit()

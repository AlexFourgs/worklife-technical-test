from sqlalchemy import create_engine
from fastapi.testclient import TestClient
from app.core.config import settings
from ..main import app

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI.unicode_string())

client = TestClient(app)

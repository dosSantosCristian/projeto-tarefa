import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from main import app
from database import Base

TEST_DATABASE_URL = "sqlite:///./teste.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

@pytest.fixture
def client():
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as cliente:
        yield cliente

    Base.metadata.drop_all(bind=engine)
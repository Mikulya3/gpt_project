import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from app.database.db import Base, get_db
from sqlalchemy.pool import StaticPool

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

#  Fixture to setup test DB once per session
@pytest.fixture()          
def db():
    Base.metadata.create_all(bind=engine)              
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()                                


# Fixture for TestClient with DB override
@pytest.fixture()
def client(db):  
    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)
    app.dependency_overrides.clear()


# Automatically clean tables after each test
@pytest.fixture(autouse=True)
def clean_tables(db):
    db.rollback()  
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()


    


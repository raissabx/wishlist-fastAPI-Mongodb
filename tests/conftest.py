from typing import Dict
from faker import Faker
from fastapi import Depends
from fastapi.testclient import TestClient
from auth.auth_user import create_jwt_token, verify_token
import pytest
from main import app
from auth.auth_user import create_jwt_token


fake = Faker()

@pytest.fixture()
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture
def mock_create_jwt_token():
    encoded_jwt = create_jwt_token({'sub': fake.user_name()})
    
    return encoded_jwt

@pytest.fixture()
def mock_verify_token(token: dict = Depends(verify_token)) -> Dict:
    return token
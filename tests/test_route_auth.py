import faker
from fastapi.testclient import TestClient
import pytest
from main import app
from config.database import collection_auth
from security.security import UserModel

f = faker.Faker()


class TestAuth:

    @pytest.fixture()
    def test_app(self):
        client = TestClient(app)
        yield client

    @pytest.fixture
    def test_user(self):
        return UserModel(
            username=f.user_name(),
            password=f.password()
        ).model_dump()

    @pytest.fixture
    async def test_user_post(
        self,
        test_user,
        test_app
    ):
        try:
            test_app.post(
                '/auth',
                json=test_user
            )
            yield test_user
        finally:
            collection_auth.delete_one({'username': test_user['username']})

    def test_create_user(
            self,
            mock_create_jwt_token,
            mock_verify_token,
            test_app,
            test_user
    ):
        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.post(
            '/auth',
            json=test_user,
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )
        assert response.status_code == 200
        assert response.json() == test_user

    def test_authentication_user_not_exists(
            self,
            test_app,
            test_user_post
    ):
        invalid_username = "nonexistentuser"
        invalid_password = test_user_post["password"]

        response = test_app.post(
            '/token/login',
            data={'username': invalid_username, 'password': invalid_password},
        )

        assert response.status_code == 404
        assert response.json()['detail'] == 'User not found'

    def test_authentication_wrong_password(
            self,
            test_app,
            test_user_post
    ):
        valid_username = test_user_post['username']
        invalid_password = 'wrongpassword'

        response = test_app.post(
            '/token/login',
            data={"username": valid_username, "password": invalid_password}
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

    def test_authentication_success(
            self,
            test_app,
            test_user_post
    ):
        valid_username = test_user_post["username"]
        valid_password = test_user_post["password"]

        response = test_app.post(
            '/token/login',
            data={"username": valid_username, "password": valid_password}
        )

        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

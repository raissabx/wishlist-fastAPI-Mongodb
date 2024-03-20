import faker
from fastapi.testclient import TestClient
import pytest
from models.models import ProductModel
from main import app
from config.database import collection_product

f = faker.Faker()


class TestProduct:

    @pytest.fixture
    def test_app(self):
        client = TestClient(app)
        yield client

    @pytest.fixture
    def product_fixture(self):
        return ProductModel(
            id = f.uuid4(),
            name_product=f.word()
        ).model_dump()

    @pytest.fixture
    async def product_fixture_post(
        self,
        product_fixture,
        test_app,
        mock_create_jwt_token,
        mock_verify_token
    ):
        try:
            mock_verify_token.return_value = mock_create_jwt_token
            test_app.post(
                '/products',
                json=product_fixture,
                headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
            )
            yield product_fixture
        finally:
            collection_product.delete_one(
                {'id': product_fixture['id']}
            )

    def test_create_product(
            self,
            test_app,
            product_fixture,
            mock_create_jwt_token,
            mock_verify_token
    ):
        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.post(
            '/products',
            json=product_fixture,
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )

        assert response.status_code == 200
        assert response.json() == product_fixture

    def test_get_product(
            self,
            test_app,
            product_fixture,
            mock_create_jwt_token,
            mock_verify_token,
            product_fixture_post
    ):
        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.get(
            '/products',
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )

        assert response.status_code == 200

    def test_get_product_id(
            self,
            test_app,
            mock_verify_token,
            mock_create_jwt_token,
            product_fixture_post
    ):
        id = product_fixture_post['id']

        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.get(
            f'/products/{id}',
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )
        assert response.status_code == 200
        assert response.json()['id'] == id

    def test_delete_product(
            self,
            test_app,
            mock_create_jwt_token,
            mock_verify_token,
            product_fixture_post
    ):
        id = product_fixture_post['id']

        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.delete(
            f'/products/{id}',
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )

        assert response.status_code == 200
        customer_db = collection_product.find_one(
            {'id': id}
        )
        assert customer_db is None
        assert response.json()['detail'] == 'Product deleted successfully'

import faker
from fastapi.testclient import TestClient
import pytest
from models.models import CustomerModel, ProductModel
from main import app
from config.database import collection_customer


f = faker.Faker()


class TestCustomer:

    @pytest.fixture()
    def test_app(self):
        client = TestClient(app)
        yield client

    @pytest.fixture
    def customer_fixture(self):
        return CustomerModel(
            name_customer=f.name(),
            email=f.email(),
            favorites=[]
        ).model_dump()

    @pytest.fixture
    async def customer_fixture_post(
        self,
        customer_fixture,
        mock_create_jwt_token,
        mock_verify_token,
        test_app
    ):
        try:
            mock_verify_token.return_value = mock_create_jwt_token
            test_app.post(
                '/customers',
                json=customer_fixture,
                headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
            )
            yield customer_fixture
        finally:
            collection_customer.delete_one(
                {'email': customer_fixture['email']}
            )

    @pytest.fixture
    async def product_fixture_post(
        self,
        mock_create_jwt_token,
        mock_verify_token,
        test_app
    ):
        product = ProductModel(
            id = '1000',
            name_product='celular'
        ).model_dump()

        try:
            mock_verify_token.return_value = mock_create_jwt_token
            test_app.post(
                '/products',
                json=product,
                headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
            )
            yield product
        finally:
            collection_customer.delete_one({'id': product['id']})

    @pytest.fixture
    async def favorites_fixture_post(
        self,
        mock_create_jwt_token,
        mock_verify_token, 
        test_app
    ):
        product = ProductModel(
            id = '2000',
            name_product='geladeira'
        ).model_dump()

        mock_verify_token.return_value = mock_create_jwt_token
        test_app.post(
            '/products',
            json=product,
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )

        product_second = ProductModel(
            id = '3000',
            name_product='fogão'
        ).model_dump()

        mock_verify_token.return_value = mock_create_jwt_token
        test_app.post(
            '/products',
            json=product_second,
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )

        customer = CustomerModel(
            name_customer=f.name(),
            email=f.email(),
            favorites=['2000', '3000']
        ).model_dump()

        try:
            mock_verify_token.return_value = mock_create_jwt_token
            test_app.post(
                '/customers',
                json=customer,
                headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
            )

            yield customer
        finally:
            collection_customer.delete_one({'email': customer['email']})
            collection_customer.delete_one({'id': product['id']})
            collection_customer.delete_one({'id': product_second['id']})

    def test_create_customer(
            self,
            test_app,
            mock_verify_token,
            mock_create_jwt_token,
            customer_fixture
    ):
        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.post(
            '/customers',
            json=customer_fixture,
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )
        assert response.status_code == 200
        assert response.json()['email'] == customer_fixture['email']
        customer_db = collection_customer.find_one(
            {'email': customer_fixture['email']}
        )
        assert customer_db['email'] == customer_fixture['email']

    def test_get_all_customer(
            self,
            test_app,
            mock_verify_token,
            mock_create_jwt_token,
            customer_fixture_post,
            favorites_fixture_post
    ):

        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.get(
            '/customers',
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)

        emails = []
        for customer in response.json():
            emails.append(customer['email'])
        assert customer_fixture_post['email'] in emails
        assert favorites_fixture_post['email'] in emails

    def test_get_customer(
            self,
            test_app,
            mock_verify_token,
            mock_create_jwt_token,
            customer_fixture_post
    ):
        customer_email = customer_fixture_post['email']

        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.get(
            f'/customers/{customer_email}',
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )
        assert response.status_code == 200
        assert response.json()['email'] == customer_email

    def test_update_customer(
            self,
            test_app,
            mock_verify_token,
            mock_create_jwt_token,
            customer_fixture_post
    ):
        customer_email = customer_fixture_post['email']
        customer_fixture_post['name_customer'] = 'Miguel'

        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.put(
            f'/customers/{customer_email}',
            json=customer_fixture_post,
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )

        assert response.status_code == 200
        assert response.json()['email'] == customer_email
        assert response.json()['name_customer'] == 'Miguel'

    def test_delete_customer(
            self,
            test_app,
            mock_verify_token,
            mock_create_jwt_token,
            customer_fixture_post
    ):
        customer_email = customer_fixture_post['email']

        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.delete(
            f'/customers/{customer_email}',
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )

        assert response.status_code == 200
        assert response.json()['detail'] == 'Customer deleted successfully'

        customer_db = collection_customer.find_one({'email': customer_email})
        assert customer_db is None

    def test_add_favorite(
            self,
            test_app,
            mock_verify_token,
            mock_create_jwt_token,
            customer_fixture_post,
            product_fixture_post
    ):
        customer_email = customer_fixture_post['email']
        id_product = product_fixture_post['id']

        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.put(
            f'/customers/{customer_email}/add_favorites/{id_product}',
            json={},
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )

        assert response.status_code == 200
        assert response.json()['detail'] == 'Product added to favorites successfully'  # noqa
        customer_db = collection_customer.find_one({'email': customer_email})
        assert customer_db['favorites'] == [id_product]

    def test_remove_all_favorite(
            self,
            test_app,
            mock_verify_token,
            mock_create_jwt_token,
            favorites_fixture_post
    ):
        customer_email = favorites_fixture_post['email']

        mock_verify_token.return_value = mock_create_jwt_token
        response_remove_favorites = test_app.delete(
            f'/customers/{customer_email}/favorites/',
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )

        assert response_remove_favorites.status_code == 200
        assert response_remove_favorites.json()['detail'] == 'Favorites list cleared successfully'  # noqa

    def test_remove_favorite(
            self,
            test_app,
            mock_verify_token,
            mock_create_jwt_token,
            favorites_fixture_post
    ):
        customer_email = favorites_fixture_post['email']
        id_product = '2000'
        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.delete(
            f'/customers/{customer_email}/remove_favorites/{id_product}',
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )

        assert response.status_code == 200
        customer_db = collection_customer.find_one({'email': customer_email})
        assert customer_db['favorites'] == ['3000']
        assert response.json()['detail'] == 'Product removed from favorites successfully'  # noqa

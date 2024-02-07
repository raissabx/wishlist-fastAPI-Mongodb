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
                '/customer',
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
            name_product='celular'
        ).model_dump()

        try:
            mock_verify_token.return_value = mock_create_jwt_token
            test_app.post(
                '/product/create',
                json=product,
                headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
            )
            yield product
        finally:
            collection_customer.delete_one({'name_product': product})

    @pytest.fixture
    async def favorites_fixture_post(
        self,
        mock_create_jwt_token,
        mock_verify_token, 
        test_app
    ):
        product = ProductModel(
            name_product='geladeira'
        ).model_dump()
        mock_verify_token.return_value = mock_create_jwt_token
        test_app.post(
            '/product/create',
            json=product,
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )

        product_second = ProductModel(
            name_product='fogão'
        ).model_dump()

        mock_verify_token.return_value = mock_create_jwt_token
        test_app.post(
            '/product/create',
            json=product_second,
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )

        customer = CustomerModel(
            name_customer=f.name(),
            email=f.email(),
            favorites=['geladeira', 'fogão']
        ).model_dump()

        try:
            mock_verify_token.return_value = mock_create_jwt_token
            test_app.post(
                '/customer',
                json=customer,
                headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
            )

            yield customer
        finally:
            collection_customer.delete_one({'email': customer['email']})
            collection_customer.delete_one({'name_product': product})
            collection_customer.delete_one({'name_product': product_second})

    def test_create_customer(
            self,
            test_app,
            mock_verify_token,
            mock_create_jwt_token,
            customer_fixture
    ):
        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.post(
            '/customer',
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
            '/customer',
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
            f'/customer/{customer_email}',
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
            f'/customer/{customer_email}/update',
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
            f'/customer/{customer_email}/delete',
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
        name_product = product_fixture_post['name_product']

        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.put(
            f'/customer/{customer_email}/add_favorite/{name_product}',
            json={},
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )

        assert response.status_code == 200
        assert response.json()['detail'] == 'Product added to favorites successfully'  # noqa
        customer_db = collection_customer.find_one({'email': customer_email})
        assert customer_db['favorites'] == [name_product]

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
            f'/customer/{customer_email}/favorites/',
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
        product_name = 'geladeira'
        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.delete(
            f'/customer/{customer_email}/remove_favorite/{product_name}',
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )

        assert response.status_code == 200
        customer_db = collection_customer.find_one({'email': customer_email})
        assert customer_db['favorites'] == ['fogão']
        assert response.json()['detail'] == 'Product removed from favorites successfully'  # noqa

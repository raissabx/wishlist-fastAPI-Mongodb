from http import HTTPStatus
import json
from faker import Faker
import pytest
from models.models import CustomerModel, ProductAPIModel
from unittest.mock import patch
from config.database import collection_customer


fake = Faker()


class TestProductAPI:

    @pytest.fixture
    def create_product(self) -> ProductAPIModel:
        product = {
            'id': 'c0aec577-f102-4ac8-470c-3d84fa8fd094',
            'title': 'Organizador de Gaveta',
            'image': 'http://challenge-api.luizalabs.com/images/c0aec577-f102-4ac8-470c-3d84fa8fd094.jpg',
            'price': 51.66
        }        
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = product

        return product

       
    
    @pytest.fixture
    async def customer_fixture(self, mock_create_jwt_token, mock_verify_token, test_app):
        customer = CustomerModel(
            name_customer = fake.name(),
            email = fake.email(),
            favorites = []
        ).model_dump()

        try: 
            mock_verify_token.return_value = mock_create_jwt_token
            response = test_app.post(
                    '/customer',
                    json=customer,
                    headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
                )
            yield customer
        finally:
            collection_customer.delete_one({'email': customer['email']})

    
    async def test_get_product_page(
            self,
            test_app,
            mock_verify_token,
            mock_create_jwt_token
        ):
        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.get(
            '/product_api/1',
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )
        assert response.status_code == HTTPStatus.OK

    async def test_get_product_id(
            self,
            test_app,
            mock_verify_token,
            mock_create_jwt_token,
            create_product
        ):
        product_id = create_product['id']
        
        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.get(
            f'/product_api/{product_id}/',
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )
        assert response.status_code == 200

    async def test_add_favorite_product(
            self,
            test_app,
            mock_verify_token,
            mock_create_jwt_token,
            create_product,
            customer_fixture
        ):
        product_id = create_product['id']
        customer_email = customer_fixture['email']
        
        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.put(
            f'/product_api/{customer_email}/{product_id}/',
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )

        assert response.status_code == 200
        customer_db = collection_customer.find_one({'email': customer_email})
        assert product_id in customer_db['favorites']


    
    
    async def test_remove_all_favorite(
            self,
            test_app,
            mock_verify_token,
            mock_create_jwt_token,
            create_product,
            customer_fixture
        ):
        product_id = create_product['id']
        customer_email = customer_fixture['email']
        
        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.put(
            f'/product_api/{customer_email}/{product_id}/',
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )
        
        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.delete(
            f'/product_api/{customer_email}/remove_favorite/',
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )

        assert response.status_code == 200

        customer_db = collection_customer.find_one({'email': customer_email})
        assert customer_db['favorites'] == []

        response_data = json.loads(response.text)
        assert response_data.get('detail') == 'Favorites list cleared successfully'

    
    async def test_remove_favorite(
            self,
            test_app,
            mock_verify_token,
            mock_create_jwt_token,
            create_product,
            customer_fixture
        ):
        product_id = create_product['id']
        customer_email = customer_fixture['email']
        
        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.put(
            f'/product_api/{customer_email}/{product_id}/',
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )
        
        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.delete(
            f'/product_api/{customer_email}/remove_favorite/{product_id}',
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )

        assert response.status_code == 200

        customer_db = collection_customer.find_one({'email': customer_email})
        assert customer_db['favorites'] == []

        response_data = json.loads(response.text)
        assert response_data.get('detail') == 'Product removed from favorites successfully'

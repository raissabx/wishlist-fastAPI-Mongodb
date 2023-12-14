import faker
from fastapi.testclient import TestClient
import pytest
from models.models import CustomerModel
from main import app


f = faker.Faker()

@pytest.fixture(scope='module')
def test_app():
    client = TestClient(app)
    yield client

@pytest.fixture
def customer_fixture(scope='module'):
    return CustomerModel(
        name_customer = f.name(),
        email = f.email(),
        favorites = []
    ).model_dump()
    

def test_create_customer(customer_fixture, test_app):
    response = test_app.post('/customer', json=customer_fixture)
    assert response.status_code == 200
    assert response.json()['email'] == customer_fixture['email']


def test_get_all_customer(test_app):
    response = test_app.get('/customer')
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_customer(customer_fixture, test_app):
    response = test_app.post('/customer', json=customer_fixture)
    customer_id = response.json().get('id')
    response = test_app.get(f'/customer/{customer_id}')
    
    assert response.status_code == 200
    assert response.json()['email'] == customer_fixture['email']


def test_update_customer(customer_fixture, test_app):
    response = test_app.post('/customer', json=customer_fixture)
    customer_id = response.json().get('id')
    customer_fixture['email'] = f.email()
    response = test_app.put(f'/customer/{customer_id}', json=customer_fixture)

    assert response.status_code == 200
    assert response.json()['email'] == customer_fixture['email']


def test_delete_customer(customer_fixture, test_app):
    response = test_app.post('/customer', json=customer_fixture)
    customer_id = response.json().get('id')
    response = test_app.delete(f'/customer/{customer_id}')
    
    assert response.status_code == 200
    assert response.json()['detail'] == 'Customer deleted successfully'


def test_add_favorite(customer_fixture, test_app):
    response = test_app.post('/customer', json=customer_fixture)
    customer_id = response.json().get('id')
    product_name = 'geladeira'
    customer_fixture['favorites'].append(product_name)
    response = test_app.put(f'/customer/{customer_id}/add_favorite/{product_name}', json={})
    
    assert response.status_code == 200
    assert response.json()['detail'] == 'Product added to favorites successfully'


def test_remove_all_favorite(test_app, customer_fixture):
    response = test_app.post('/customer', json=customer_fixture)
    customer_id = response.json().get('id')
    response_remove_favorites = test_app.delete(f'/customer/{customer_id}/favorites/')
    
    assert response_remove_favorites.status_code == 200
    assert response_remove_favorites.json()['detail'] == 'Favorites list cleared successfully'


def test_remove_favorite(test_app, customer_fixture):
    response = test_app.post('/customer', json=customer_fixture)
    customer_id = response.json().get('id')
    product_name = 'geladeira'
    customer_fixture['favorites'].append(product_name)
    response = test_app.put(f'/customer/{customer_id}/add_favorite/{product_name}', json={})
    response = test_app.delete(f'/customer/{customer_id}/remove_favorite/{product_name}')

    assert response.status_code == 200
    assert response.json()['detail'] == 'Product removed from favorites successfully'


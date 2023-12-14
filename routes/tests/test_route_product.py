import faker
from fastapi.testclient import TestClient
import pytest
from models.models import ProductModel
from main import app


f = faker.Faker()

@pytest.fixture(scope='module')
def test_app():
    client = TestClient(app)
    yield client

@pytest.fixture
def product_fixture(scope='module'):
    return ProductModel(
        name_product = f.word()
    ).model_dump()


def test_create_product(test_app, product_fixture):
    response = test_app.post('/product', json=product_fixture)
    
    assert response.status_code == 200
    assert response.json() == product_fixture


def test_get_product(test_app, product_fixture):
    response = test_app.post('/product', json=product_fixture)
    response = test_app.get('/product')

    assert response.status_code == 200
    assert product_fixture in response.json()


def test_delete_product(test_app, product_fixture):
    response = test_app.post('/product', json=product_fixture)
    response = test_app.delete(f"/product/{product_fixture['name_product']}")

    assert response.status_code == 200
    assert response.json()['detail'] == 'Product deleted successfully'




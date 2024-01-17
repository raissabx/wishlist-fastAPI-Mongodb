from typing import Optional
from http import HTTPStatus
from models.models import ProductAPIModel


class TestProductAPI:

    def create_product(
            id: str,
            title: str,
            image: str,
            price: float,
            review: Optional[str] = None
    ) -> ProductAPIModel:
        return {
            'id': id,
            'title': title,
            'image': image,
            'price': price,
            'review': review
        }



    async def test_get_product_page(self, test_app, mock_verify_token, mock_create_jwt_token):
        mock_verify_token.return_value = mock_create_jwt_token
        response = test_app.get(
            '/product_api/1',
            headers={'Authorization': f'Bearer {mock_create_jwt_token}'}
        )
        assert response.status_code == HTTPStatus.OK

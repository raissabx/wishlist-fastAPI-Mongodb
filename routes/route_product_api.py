from typing import Dict
from fastapi import APIRouter, Depends, HTTPException
from auth.auth_user import verify_token
from models.models import ProductAPIModel
import requests
from config.database import collection_customer
import os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv('API_PRODUCT_MAGALU')
router = APIRouter()


def verify_product_exists(id: str, token: dict = Depends(verify_token)):
    try:
        get_product_id(id)
        return True
    except HTTPException as e:

        if e.status_code == 404:
            return False
        raise e


@router.get(
        '/product_api/{page}',
        tags=['product_api'],
        summary='Consultar todos os produtos por páginas',
        response_model=list[ProductAPIModel]
)
async def get_all_product(page: int, token: dict = Depends(verify_token)):
    product_by_page_url = f'{API_URL}?page={page}'
    response = requests.get(product_by_page_url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail='Failed to fetch products'
        )

    product_api = response.json().get('products', [])

    return product_api


@router.get(
        '/product_api/{id}/',
        tags=['product_api'],
        summary='Consultar todos os produtos por id',
        response_model=ProductAPIModel
)
async def get_product_id(id: str, token: dict = Depends(verify_token)):
    product_by_id_url = f'{API_URL}{id}/'
    response = requests.get(product_by_id_url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail='Failed to fetch products'
        )
    product_api = response.json()

    if not product_api:
        raise HTTPException(status_code=404, detail='Product not found')

    return product_api


@router.put(
        '/product_api/{customer_email}/{product_id}/',
        tags=['wishlist_api'],
        summary='Adicionar item na lista de favoritos',
        response_model=Dict[str, str]
)
async def add_favorite_product(
    product_id: str,
    customer_email: str,
    token: dict = Depends(verify_token)
):

    customer = collection_customer.find_one({'email': customer_email})
    if not customer:
        raise HTTPException(status_code=404, detail='Customer not found')

    if not verify_product_exists(product_id):
        raise HTTPException(status_code=404, detail='Product not found')

    if str(product_id) in customer['favorites']:
        raise HTTPException(
            status_code=400,
            detail='Product already in favorites list'
        )

    collection_customer.update_one(
        {'email': customer_email},
        {'$push': {'favorites': product_id}}
    )

    return {'detail': 'Product added to favorites successfully'}


@router.delete(
        '/product_api/{customer_email}/remove_favorite/',
        tags=['wishlist_api'],
        summary='Deletar todos os itens da lista de favoritos',
        response_model=Dict[str, str]
)
async def remove_all_favorite(
    customer_email: str,
    token: dict = Depends(verify_token)
):
    customer = collection_customer.find_one({'email': customer_email})
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    collection_customer.update_one(
        {'email': customer_email},
        {'$set': {'favorites': []}}
    )
    return {'detail': 'Favorites list cleared successfully'}


@router.delete(
    '/product_api/{customer_email}/remove_favorite/{product_id}',
    tags=['wishlist_api'],
    summary='Remover um item da lista de favoritos',
    response_model=Dict[str, str]
)
async def remove_favorite(
    customer_email: str,
    product_id: str,
    token: dict = Depends(verify_token)
):
    customer = collection_customer.find_one({'email': customer_email})
    if not customer:
        raise HTTPException(
            status_code=404,
            detail='Customer not found'
        )

    if not verify_product_exists(product_id):
        raise HTTPException(status_code=404, detail='Product not found')

    if product_id not in customer['favorites']:
        raise HTTPException(
            status_code=400,
            detail='Product not in favorites list'
        )

    collection_customer.update_one(
        {'email': customer_email},
        {'$pull': {'favorites': product_id}}
    )
    return {'detail': 'Product removed from favorites successfully'}

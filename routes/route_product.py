from typing import Dict
import uuid
from fastapi import APIRouter, Depends, HTTPException
from auth.auth_user import verify_token
from models.models import ProductModel
from config.database import collection_product

router = APIRouter()


@router.post(
        '/products',
        tags=['products'],
        summary='Cadastrar produtos',
        response_model=ProductModel
)
async def create_product(
    product: ProductModel,
    token: dict = Depends(verify_token)
):
    product_dict = product.model_dump()
    if collection_product.find_one(
        {'id': product_dict['id']}
    ):
        raise HTTPException(status_code=400, detail='Product already exists')
    collection_product.insert_one(product_dict)

    return product_dict


@router.get(
        '/products',
        tags=['products'],
        summary='Consultar todos os produtos',
        response_model=list[ProductModel]
)
async def get_products(token: dict = Depends(verify_token)):
    cursor = collection_product.find()
    product_list = list(cursor)

    return product_list

@router.get(
        '/products/{id}',
        tags=['products'],
        summary='Consultar produtos pelo id',
        response_model=ProductModel
)
async def get_products_id(
    id: str,
    token: dict = Depends(verify_token)
) -> ProductModel:
    product = collection_product.find_one({'id': id})
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')

    return product



@router.delete(
    '/products/{id}',
    tags=['products'],
    summary='Deletar produtos',
    response_model=Dict[str, str]
)
async def delete_product(
    id: str,
    token: dict = Depends(verify_token)
):
    product = collection_product.find_one_and_delete(
        {"id": id}
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted successfully"}

from typing import Dict
from fastapi import APIRouter, Depends, HTTPException
from auth.auth_user import verify_token
from models.models import ProductModel
from config.database import collection_product



router = APIRouter()

@router.post(
        '/product/create',
        tags = ['product'],
        summary = 'Cadastrar produto',
        response_model = ProductModel
)
async def create_product(product: ProductModel, token: dict = Depends(verify_token)):
    product_dict = product.model_dump()
    if collection_product.find_one(
        {'name_product': product_dict['name_product']}
    ):
        raise HTTPException(status_code=400, detail='Product already exists')
    collection_product.insert_one(product_dict)

    return product_dict


@router.get(
        '/product',
        tags = ['product'],
        summary = 'Consultar todos os produtos',
        response_model = list[ProductModel]
)
async def get_product(token: dict = Depends(verify_token)):
    cursor = collection_product.find()
    product_list = list(cursor)

    return product_list


@router.delete(
    '/product/{name_product}',
    tags = ['product'],
    summary = 'Deletar produto',
    response_model = Dict[str, str]
)
async def delete_product(name_product: str, token: dict = Depends(verify_token)):
    product = collection_product.find_one_and_delete({"name_product": name_product})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted successfully"}

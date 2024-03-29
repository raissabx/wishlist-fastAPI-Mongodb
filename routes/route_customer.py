from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException
from auth.auth_user import verify_token
from models.models import CustomerModel
from config.database import collection_customer, collection_product


router = APIRouter()


@router.post(
        '/customers',
        tags=['customers'],
        summary='Cadastrar clientes',
        response_model=CustomerModel
)
async def create_customer(
    customer: CustomerModel,
    token: dict = Depends(verify_token)
) -> CustomerModel:
    customer_dict = customer.model_dump()
    if collection_customer.find_one({'email': customer_dict['email']}):
        raise HTTPException(status_code=400, detail='Customer already exists')
    inserted_customer = collection_customer.insert_one(customer_dict)
    customer_dict['id'] = str(inserted_customer.inserted_id)

    return customer_dict


@router.get(
        '/customers',
        tags=['customers'],
        summary='Consultar todos os clientes',
        response_model=List[CustomerModel]
)
async def get_all_customer(token: dict = Depends(verify_token)):
    customer_list = collection_customer.find()
    return customer_list


@router.get(
        '/customers/{email}',
        tags=['customers'],
        summary='Consultar clientes por email',
        response_model=CustomerModel
)
async def get_customer(
    email: str,
    token: dict = Depends(verify_token)
) -> CustomerModel:
    customer = collection_customer.find_one({'email': email})
    if not customer:
        raise HTTPException(status_code=404, detail='Customer not found')

    customer['email'] = email
    return customer


@router.put(
        '/customers/{email}',
        tags=['customers'],
        summary='Atualizar clientes',
        response_model=CustomerModel
)
async def update_customer(
    customer: CustomerModel,
    email: str,
    token: dict = Depends(verify_token)
):
    customer_dict = customer.model_dump()
    customer_in_db = collection_customer.find_one(
        {'email': email}
    )
    if not customer_in_db:
        raise HTTPException(status_code=404, detail='Customer not found')

    if customer_in_db["email"] != customer_dict["email"]:
        customer_with_new_email = collection_customer.find_one(
            {"email": customer_dict["email"]}
        )
        if customer_with_new_email:
            raise HTTPException(status_code=400, detail='Email already in use')

    collection_customer.update_one({'email': email}, {'$set': customer_dict})
    return customer_dict


@router.delete(
    '/customers/{email}',
    tags=['customers'],
    summary='Deletar clientes',
    response_model=Dict[str, str]
)
async def delete_customer(email: str, token: dict = Depends(verify_token)):
    customer = collection_customer.find_one_and_delete({"email": email})
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"detail": "Customer deleted successfully"}


@router.put(
        '/customers/{customer_email}/add_favorites/{id_product}',
        tags=['wishlist'],
        summary='Adicionar item na lista de favoritos',
        response_model=Dict[str, str]
)
async def add_favorite(
    customer_email: str,
    id_product: str,
    token: dict = Depends(verify_token)
):
    customer = collection_customer.find_one({'email': customer_email})
    if not customer:
        raise HTTPException(status_code=404, detail='Customer not found')

    product = collection_product.find_one({'id': id_product})
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')

    if id_product in customer['favorites']:
        raise HTTPException(
            status_code=400,
            detail='Product already in favorites list'
        )

    collection_customer.update_one(
        {'email': customer_email},
        {'$push': {'favorites': id_product}}
    )
    return {'detail': 'Product added to favorites successfully'}


@router.delete(
        '/customers/{customer_email}/favorites/',
        tags=['wishlist'],
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
    '/customers/{customer_email}/remove_favorites/{id_product}',
    tags=['wishlist'],
    summary='Deletar um item da lista de favoritos',
    response_model=Dict[str, str]
)
async def remove_favorite(
    customer_email: str,
    id_product: str,
    token: dict = Depends(verify_token)
):
    customer = collection_customer.find_one({'email': customer_email})
    if not customer:
        raise HTTPException(status_code=404, detail='Customer not found')

    product = collection_product.find_one({'id': id_product})
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')

    if id_product not in customer['favorites']:
        raise HTTPException(
            status_code=400,
            detail='Product not in favorites list'
        )

    collection_customer.update_one(
        {'email': customer_email},
        {'$pull': {'favorites': id_product}}
    )
    return {'detail': 'Product removed from favorites successfully'}

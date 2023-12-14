from typing import Dict
from fastapi import APIRouter, HTTPException
from models.models import CustomerModel, CustomerOut
from config.database import collection_customer, collection_product
from bson.objectid import ObjectId



router = APIRouter()

@router.post(
        '/customer',
        tags=['customer'],
        summary = 'Cadastrar um cliente',
        response_model = CustomerOut
)
async def create_customer(customer: CustomerModel) -> CustomerOut:
    customer_dict = customer.model_dump()
    
    if collection_customer.find_one({'email': customer_dict['email']}):
        raise HTTPException(status_code=400, detail='Customer already exists')
    
    inserted_customer = collection_customer.insert_one(customer_dict)
    customer_dict['id'] = str(inserted_customer.inserted_id)

    return customer_dict


@router.get(
        '/customer',
        tags=['customer'], 
        summary = 'Consultar todos os clientes',
        response_model = list[CustomerModel]
)
async def get_all_customer():
    cursor = collection_customer.find()
    customer_list = list(cursor)

    return customer_list

@router.get(
        '/customer/{id}',
        tags=['customer'],
        summary = 'Consultar cliente por id',
        response_model = CustomerOut
)
async def get_customer(id: str) -> CustomerOut:
    customer = collection_customer.find_one({'_id': ObjectId(id)})
    if not customer:
        raise HTTPException(status_code=404, detail='Customer not found')
    
    customer['id'] = id
    return customer

@router.put(
        '/customer/{id}',
        tags=['customer'],
        summary = 'Atualizar cliente pelo ID',
        response_model = CustomerModel
)
async def update_customer(customer: CustomerModel, id: str):
    customer_dict = customer.model_dump()
    object_id = ObjectId(id)

    customer_in_db = collection_customer.find_one(
        {'_id': object_id}
    )
    if not customer_in_db:
        raise HTTPException(status_code=404, detail='Customer not found')
    
    if customer_in_db["email"] != customer_dict["email"]:
        customer_with_new_email = collection_customer.find_one(
            {"email": customer_dict["email"]}
        )
        if customer_with_new_email:
            raise HTTPException(status_code=400, detail='Email already in use')
        
    collection_customer.update_one({'_id': object_id}, {'$set': customer_dict})
    return customer_dict
    
@router.delete(
    '/customer/{id}',
    tags=['customer'],
    summary = 'Deletar cliente',
    response_model = Dict[str, str]
)
async def delete_customer(id: str):
    customer = collection_customer.find_one_and_delete({"_id": ObjectId(id)})
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {"detail": "Customer deleted successfully"}


@router.put(
        '/customer/{customer_id}/add_favorite/{name_product}',
        tags=['wishlist'],
        summary = 'Lista de Favoritos',
        response_model = Dict[str, str]
)
async def add_favorite(customer_id: str, name_product: str):
    customer = collection_customer.find_one({'_id': ObjectId(customer_id)})
    if not customer:
        raise HTTPException(status_code=404, detail='Customer not found')

    product = collection_product.find_one({'name_product': name_product})
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    
    if name_product in customer['favorites']:
        raise HTTPException(status_code= 400, detail='Product already in favorites list')
    
    collection_customer.update_one({'_id': ObjectId(customer_id)}, {'$push': {'favorites': name_product}})
    return {'detail': 'Product added to favorites successfully'}


@router.delete(
        '/customer/{customer_id}/favorites/',
        tags=['wishlist'],
        summary = 'Deletar todos os itens da lista de favoritos',
        response_model = Dict[str, str]
)
async def remove_all_favorite(customer_id: str):
    customer = collection_customer.find_one({'_id': ObjectId(customer_id)})
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    collection_customer.update_one({'_id': ObjectId(customer_id)}, {'$set': {'favorites': []}})
    return {'detail': 'Favorites list cleared successfully'}

@router.delete(
    '/customer/{customer_id}/remove_favorite/{name_product}',
    tags=['wishlist'],
    summary= 'Remover um item da lista de favoritos',
    response_model = Dict[str, str]
)
async def remove_favorite(customer_id: str, name_product: str):
    customer = collection_customer.find_one({'_id': ObjectId(customer_id)})
    if not customer:
        raise HTTPException(status_code=404, detail= 'Customer not found')
    
    product = collection_product.find_one({'name_product': name_product})
    if not product:
        raise HTTPException(status_code= 404, detail= 'Product not found')
    
    if name_product not in customer['favorites']:
        raise HTTPException(status_code=400, detail='Product not in favorites list')
    
    collection_customer.update_one({'_id': ObjectId(customer_id)}, {'$pull': {'favorites': name_product}})
    return {'detail': 'Product removed from favorites successfully'}

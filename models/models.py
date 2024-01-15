import re
from typing import Annotated, Optional
from pydantic import BaseModel, Field, BeforeValidator, validator


PyObjectId = Annotated[str, BeforeValidator(str)]


class CustomerModel(BaseModel):
    name_customer: str = Field(title='')
    email: str = Field(title='')
    favorites: list = Field([], title='')


class ProductModel(BaseModel):
    name_product: str

class ProductAPIModel(BaseModel):
    id: str
    title: str
    image: str
    price: float
    review: Optional[str] = None
    
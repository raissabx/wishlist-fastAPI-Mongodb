from typing import Annotated, Optional
from pydantic import BaseModel, Field, BeforeValidator


PyObjectId = Annotated[str, BeforeValidator(str)]


class CustomerModel(BaseModel):
    name_customer: str
    email: str
    favorites: list = []


class CustomerOut(CustomerModel):
    id: str = Field(title='ID of customer')


class ProductModel(BaseModel):
    name_product: str
 






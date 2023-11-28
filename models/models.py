from typing import Annotated, List, Optional
from pydantic import BaseModel, Field, BeforeValidator



PyObjectId = Annotated[str, BeforeValidator(str)]


class CustomerModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name_customer: str
    email: str
    favorites: list = []


class ProductModel(BaseModel):
    name_product: str
 






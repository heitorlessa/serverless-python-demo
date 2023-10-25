from typing import Annotated

from pydantic import BaseModel, Field, PositiveInt
from pydantic.functional_validators import AfterValidator

from product.models.products.validators import validate_product_id

ProductId = Annotated[str, Field(min_length=36, max_length=36), AfterValidator(validate_product_id)]
"""Unique Product ID, represented and validated as a UUID string."""

# schemas here are shared between both CRUD and Stream processor modules


class ProductEntry(BaseModel):
    """Data representation for a product in a DynamoDB.
    In advanced services, ProductEntry is different than Product

    Parameters
    ----------
    name : str
        Product name
    id : ProductId
        Product ID (UUID string)
    price : PositiveInt
        Product price represented as a positive integer
    """

    name: Annotated[str, Field(min_length=1, max_length=30)]
    id: ProductId
    price: PositiveInt
    created_at: PositiveInt

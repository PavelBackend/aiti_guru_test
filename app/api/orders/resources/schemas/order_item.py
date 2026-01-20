from pydantic import BaseModel, Field

class AddItemRequest(BaseModel):
    product_id: int = Field(..., alias='product_id')
    qty: int = Field(gt=0, alias='quantity')

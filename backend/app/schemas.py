from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field

class TransactionOut(BaseModel):
    id: int; merchant: str; category: str; amount: Decimal; occurred_on: date; status: str; card_last4: str; notes: str | None
    model_config = {"from_attributes": True}

class RedeemIn(BaseModel):
    reward_id: int = Field(gt=0)

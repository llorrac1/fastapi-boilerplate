from ..schema import BaseSchema
from datetime import datetime
from typing import Optional
from pydantic import Field
from enum import Enum
from time import time


class BaseAccountSchema(BaseSchema):
    id: str = Field(description="Account ID", example="string")
    account_name: str = Field(description="The name of the account", example="string")
    account_type: str = Field(description="The type of account this is such as ", example="string")
    balance: float = Field(0, description="The current balance of the account", example=0)
    available_balance: float = Field(0, description="The current available balance of the account", example=0)
    currency: str = Field(None, description="The currency of the account", example="string")
    account_holder_id: str = Field(description="The ID of the account holder", example="string")
    active: bool = Field(True, description="Whether the account is active or not", example=True)
    metadata: dict = Field(default_factory=dict, description="Any additional metadata", alias="meta")
    created_at: datetime = Field(description="The date and time the account was created", example="1391759952")
    updated_at: datetime = Field(description="The date and time the account was last updated", example="1391759952")

    class Config:
        schema_extra = {
            "example": {
                "id": "string",
                "account_name": "string",
                "account_type": "string",
                "balance": 0,
                "available_balance": 0,
                "currency": "string",
                "account_holder_id": "string",
                "status": "string",
                "active": True,
                "metadata": {},
                "created_at": "1391759952",
                "updated_at": "1391759952" 
            }
        }


class BaseNewAccountRequestSchema(BaseSchema):
    account_name: str
    account_type: str
    currency: str
    account_holder_id: str
    metadata: dict = None


class UpdateAccountRequestSchema(BaseNewAccountRequestSchema):
    pass


class PublicAccountSchema(BaseAccountSchema):
    pass


class SubLedgerAccountSchema(BaseAccountSchema):
    parent_account_id: str


class NewSubLedgerAccountRequestSchema(BaseNewAccountRequestSchema):
    parent_account_id: str


class UpdateSubLedgerAccountRequestSchema(BaseNewAccountRequestSchema):
    parent_account_id: str


class GeneralLedgerAccountSchema(BaseAccountSchema):
    sub_ledger_accounts: Optional[list[SubLedgerAccountSchema]] = Field(None, description="The sub ledger accounts", example=[])


class NewGeneralLedgerAccountRequestSchema(BaseNewAccountRequestSchema):
    pass


class UpdateGeneralLedgerAccountRequestSchema(BaseNewAccountRequestSchema):
    pass


class LinkedAccountStatusSchema(str, Enum):
    ACTIVE = "active"
    REVOKED = "inactive"
    ERROR = "error"


class LinkedAccountSchema(BaseAccountSchema):
    linked_account_id: str = Field(description="The ID of the linked account", example="string")
    institution_id: str = Field(description="The ID of the institution", example="string")
    institution_name: str = Field(description="The name of the institution", example="string")
    linked_account_status: LinkedAccountStatusSchema = Field(description="The status of the linked account", example="string")
    link_authorized_at: datetime = Field(description="The date and time the account was authorized", example="1391759952")


class NewLinkedAccountRequestSchema(BaseNewAccountRequestSchema):
    linked_account_id: str
    institution_id: str
    institution_name: str


class UpdateLinkedAccountRequestSchema(NewLinkedAccountRequestSchema):
    pass


class MasterAccountSchema(BaseSchema):
    id: str
    account_holder_id: str
    balance: float
    available_balance: float
    type: str # e.g. savings, checking
    linked_accounts: list[LinkedAccountSchema]
    general_ledger_accounts: list[GeneralLedgerAccountSchema]


class AccountBalanceSchema(BaseSchema):
    id: str
    balance: float = Field(0, description="The current balance of the account", example=0)
    available_balance: float = Field(0, description="The current available balance of the account", example=0)
    created_at: datetime
    updated_at: datetime

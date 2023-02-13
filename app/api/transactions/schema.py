from ..schema import BaseSchema
from datetime import datetime
from pydantic import Field
from enum import Enum
from decimal import Decimal
import time

from ...db.sqlite.transactions.db import TransactionInDBModel, TransactionMethod, TransactionStatus, TransactionType

# class TransactionType(str, Enum):
#     CREDIT = 'credit'
#     DEBIT = 'debit'
#     REFUND_CREDIT = 'refund_credit'
#     REFUND_DEBIT = 'refund_debit'
#     TRANSFER_CREDIT = 'transfer_credit'
#     TRANSFER_DEBIT = 'transfer_debit'
#     REVERSAL_CREDIT = 'reversal_credit'
#     REVERSAL_DEBIT = 'reversal_debit'


# class TransactionStatus(str, Enum):
#     PENDING = 'pending'
#     PROCESSED = 'processed'
#     VOID = 'void'


# class TransactionMethod(str, Enum):
#     CASH = 'cash'
#     CHECK = 'check'
#     CREDIT_CARD = 'credit_card'
#     DEBIT_CARD = 'debit_card'
#     ELECTRONIC_TRANSFER = 'electronic_transfer'
#     OTHER = 'other'


# class BaseTransactionSchema(BaseSchema):
#     """Base transaction schema."""
#     id: str = Field(description="The ID of this transaction")
#     account_id: str = Field(description="The ID of the account this transaction belongs to")
#     amount: Decimal = Field(description="The dollar amount of the transaction")
#     reference: str = Field(description="Reference to the transaction", max_length=32)
#     description: str = Field(description="Description of the transaction", max_length=255)
#     transaction_type: TransactionType = Field(description="The type of transaction")
#     transaction_method: TransactionMethod = Field(description="The method of the transaction")
#     transaction_method_id: str = Field(description="The ID of the transaction method such as a card id", default=None)
#     disputed: bool = Field(description="Whether the transaction is disputed", default=False)
#     created_at: datetime.timestamp = Field(description="The date and time the transaction was created in UTC")
#     updated_at: datetime.timestamp = Field(description="The date and time the transaction was last updated in UTC")
#     transaction_status: TransactionStatus = Field(description="The status of the transaction")
#     processed_at: datetime.timestamp = Field(description="The date and time the transaction was processed in UTC", default=None)
#     voided_at: datetime.timestamp = Field(description="The date and time the transaction was voided in UTC", default=None)

class BaseTransactionSchema(TransactionInDBModel, BaseSchema): 
    pass


class NewTransactionRequestSchema(BaseSchema):
    """New transaction request schema."""
    account_id: str = Field(description="The ID of the account this transaction belongs to")
    destination_account_id: str = Field(description="The ID of the destination account this is intended for")
    amount: Decimal = Field(description="The dollar amount of the transaction")
    reference: str = Field(description="Reference to the transaction", max_length=32)
    description: str = Field(description="Description of the transaction", max_length=255)
    transaction_type: TransactionType = Field(description="The type of transaction")
    transaction_method: TransactionMethod = Field(description="The method of the transaction")
    transaction_method_id: str = Field(description="The ID of the transaction method such as a card id", default=None)


class CreatedTransactionSchema(BaseTransactionSchema):
    """Created transaction schema."""
    pass


class PublicTransactionSchema(BaseTransactionSchema):
    """Public transaction schema."""
    # created_at: float = Field(description="The date and time the transaction was created in UTC")
    # updated_at: float = Field(description="The date and time the transaction was last updated in UTC")
    # pass


class UpdateTransactionRequestSchema(BaseSchema):
    """Update transaction request schema."""
    # account_id: str = Field(description="The ID of the account this transaction belongs to")
    # amount: Decimal = Field(description="The dollar amount of the transaction")
    reference: str = Field(description="Reference to the transaction", max_length=32)
    description: str = Field(description="Description of the transaction", max_length=255)
    transaction_method: TransactionMethod = Field(description="The method of the transaction")
    transaction_method_id: str = Field(description="The ID of the transaction method such as a card id", default=None)
    transaction_status: TransactionStatus = Field(description="The status of the transaction")
    processed_at: datetime = Field(description="The date and time the transaction was processed in UTC", default=None)
    voided_at: datetime = Field(description="The date and time the transaction was voided in UTC", default=None)


class VoidTransactionRequestSchema(BaseSchema):
    """Void transaction request schema."""
    transaction_id: str = Field(description="The ID of the transaction to void")
    account_id: str = Field(description="The ID of the account this transaction belongs to")
    voided_at: datetime = Field(description="The date and time the transaction was voided in UTC", default=None)


class ProcessTransactionRequestSchema(BaseSchema): 
    """Process transaction request schema."""
    transaction_id: str = Field(description="The ID of the transaction to process")
    account_id: str = Field(description="The ID of the account this transaction belongs to")
    processed_at: datetime = Field(description="The date and time the transaction was processed in UTC", default=None)


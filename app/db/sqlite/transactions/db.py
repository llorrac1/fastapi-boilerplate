from sqlmodel import SQLModel, Relationship, Field, create_engine, Session, select, JSON
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class TransactionType(str, Enum):
    CREDIT = 'credit'
    DEBIT = 'debit'
    REFUND_CREDIT = 'refund_credit'
    REFUND_DEBIT = 'refund_debit'
    TRANSFER_CREDIT = 'transfer_credit'
    TRANSFER_DEBIT = 'transfer_debit'
    REVERSAL_CREDIT = 'reversal_credit'
    REVERSAL_DEBIT = 'reversal_debit'


class TransactionStatus(str, Enum):
    PENDING = 'pending'
    PROCESSED = 'processed'
    VOID = 'void'


class TransactionMethod(str, Enum):
    CASH = 'cash'
    CHECK = 'check'
    CREDIT_CARD = 'credit_card'
    DEBIT_CARD = 'debit_card'
    ELECTRONIC_TRANSFER = 'electronic_transfer'
    OTHER = 'other'


class BaseTransactionInDBModel(SQLModel):
    id: str = Field(description="The ID of this transaction", primary_key=True, index=True)
    account_id: str = Field(description="The ID of the account this transaction belongs to", index=True)
    destination_account_id: str = Field(description="The ID of the destination account this is intended for", index=True)
    amount: Decimal = Field(description="The dollar amount of the transaction")
    reference: str = Field(description="Reference to the transaction", max_length=32)
    description: str = Field(description="Description of the transaction", max_length=255)
    transaction_type: str = Field(description="The type of transaction", index=True)
    transaction_method: str = Field(description="The method of the transaction", index=True)
    transaction_method_id: str = Field(description="The ID of the transaction method such as a card id", default=None)
    disputed: bool = Field(description="Whether the transaction is disputed", default=False, index=True)
    created_at: datetime = Field(description="The date and time the transaction was created in UTC", index=True)
    updated_at: datetime = Field(description="The date and time the transaction was last updated in UTC")
    transaction_status: TransactionStatus = Field(description="The status of the transaction", index=True)
    processed_at: datetime = Field(description="The date and time the transaction was processed in UTC", default=None)
    voided_at: datetime = Field(description="The date and time the transaction was voided in UTC", default=None)


class TransactionInDBModel(BaseTransactionInDBModel, table=True):
    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


sqlite_file_name = "transactions.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"


engine = create_engine(sqlite_url
# , echo=True
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)


class TransactionsDB:
    def __init__(self):
        self.session = Session(engine)
        create_db_and_tables()

    async def create_transaction(self, transaction: TransactionInDBModel) -> Optional[TransactionInDBModel]:
        try: 
            self.session.add(transaction)
            self.session.commit()
            self.session.refresh(transaction)
            return transaction

        except Exception as e:
            print(e)
            self.session.rollback()
            raise e


    async def get_transaction(self, transaction_id: str) -> Optional[TransactionInDBModel]:
        try: 
            return self.session.get(TransactionInDBModel, transaction_id)
        
        except Exception as e:
            print(e)
            raise e


    async def get_transactions(self, account_id: str) -> Optional[list[TransactionInDBModel]]:
        try:
            return self.session.exec(select(TransactionInDBModel).where(TransactionInDBModel.account_id == account_id)).all()
        
        except Exception as e:
            print(e)
            raise e


    async def update_transaction(self, transaction_id: str, transaction: TransactionInDBModel):
        try:
            print("updated: ", transaction)
            # current_transaction = self.session.exec(select(TransactionInDBModel).where(TransactionInDBModel.id == transaction_id)).first()
            current_transaction = self.session.get(TransactionInDBModel, transaction_id)
            print("existing:", current_transaction)
            current_transaction.reference = transaction.reference
            current_transaction.description = transaction.description
            # current_transaction.transaction_type = transaction.transaction_type
            current_transaction.transaction_method = transaction.transaction_method
            current_transaction.transaction_method_id = transaction.transaction_method_id
            # current_transaction.disputed = transaction.disputed
            # current_transaction.created_at = transaction.created_at
            current_transaction.updated_at = transaction.updated_at
            current_transaction.transaction_status = transaction.transaction_status
            current_transaction.processed_at = transaction.processed_at
            current_transaction.voided_at = transaction.voided_at

            self.session.add(current_transaction)
            self.session.commit()
            self.session.refresh(current_transaction)

            return current_transaction

        except Exception as e:
            print(e)
            self.session.rollback()
            raise e


    async def process_transaction(self, transaction_id: str, processed_at: float):
        try:
            transaction = self.get_transaction(transaction_id)
            transaction.processed_at = processed_at
            transaction.transaction_status = TransactionStatus.PROCESSED
            self.session.add(transaction)
            self.session.commit()

            return transaction.dict()

        except Exception as e:
            print(e)
            self.session.rollback()
            raise e


    async def void_transaction(self, transaction_id: str, voided_at: float):
        try:
            transaction = self.get_transaction(transaction_id)
            transaction.voided_at = voided_at
            transaction.transaction_status = TransactionStatus.VOID
            self.session.add(transaction)
            self.session.commit()

            return transaction.dict()

        except Exception as e:
            print(e)
            self.session.rollback()
            raise e

    
    async def get_transaction_by_processed(self, account_id: str) -> Optional[list[TransactionInDBModel]]:
        try:

            return self.session.exec(select(TransactionInDBModel).where(TransactionInDBModel.account_id == account_id and TransactionInDBModel.transaction_status == TransactionStatus.PROCESSED)).all()
                    
        except Exception as e:
            print(e)
            raise e


    async def get_transaction_by_pending(self, account_id: str) -> Optional[list[TransactionInDBModel]]:
        try:
            return self.session.exec(select(TransactionInDBModel).where(TransactionInDBModel.account_id == account_id and TransactionInDBModel.transaction_status == TransactionStatus.PENDING)).all()

        except Exception as e:
            print(e)
            raise e
    
    async def get_transaction_by_voided(self, account_id: str) -> Optional[list[TransactionInDBModel]]:
        try:
            return self.session.exec(select(TransactionInDBModel).where(TransactionInDBModel.account_id == account_id and TransactionInDBModel.transaction_status == TransactionStatus.VOID)).all()

        except Exception as e:
            print(e)
            raise e
        
    async def get_transaction_by_disputed(self, account_id: str) -> Optional[list[TransactionInDBModel]]:
        try:
            return self.session.exec(select(TransactionInDBModel).where(TransactionInDBModel.account_id == account_id and TransactionInDBModel.disputed == True)).all()

        except Exception as e:
            print(e)
            raise e


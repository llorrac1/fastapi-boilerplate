from fastapi import HTTPException, status, Depends
from typing import Optional
from time import time
from uuid import uuid4

# Import Models and Schemas 
from ...db.sqlite.transactions.db import TransactionInDBModel, TransactionMethod, TransactionStatus, TransactionType
from ...api.transactions.schema import UpdateTransactionRequestSchema, ProcessTransactionRequestSchema, VoidTransactionRequestSchema, NewTransactionRequestSchema, PublicTransactionSchema

from ...db.sqlite.transactions.db import TransactionsDB


class TransactionsService:
    def __init__(self):
        self.db = TransactionsDB()

    async def get_transactions(self, account_id: str) -> Optional[list[TransactionInDBModel]]:
        try: 
            return await self.db.get_transactions(account_id)

        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not get transactions")

    
    async def get_transaction(self, transaction_id: str) -> Optional[TransactionInDBModel]:
        try: 
            return await self.db.get_transaction(transaction_id)

        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not get transaction")

    
    async def create_transaction(self, transaction: NewTransactionRequestSchema) -> Optional[TransactionInDBModel]:
        try: 
            new_transaction = TransactionInDBModel(
                id= str(uuid4().hex),
                account_id=transaction.account_id,
                destination_account_id=transaction.destination_account_id,
                amount=transaction.amount,
                description=transaction.description,
                reference=transaction.reference,
                transaction_type=transaction.transaction_type,
                transaction_method=transaction.transaction_method,
                transaction_method_id=transaction.transaction_method_id,
                transaction_status=TransactionStatus.PENDING,
                created_at=time().__trunc__(),
                updated_at=time().__trunc__(),
                processed_at=None,
                voided_at=None,
                disputed=False

            )
            created = await self.db.create_transaction(new_transaction)
            if created:
                return PublicTransactionSchema(**created.dict())

        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not create transaction")

    
    async def update_transaction(self, transaction_id, transaction: UpdateTransactionRequestSchema) -> Optional[TransactionInDBModel]:
        try: 
            to_update = transaction.dict()
            updated_transaction = TransactionInDBModel(
                **to_update,
                id=transaction_id,
                updated_at=time().__trunc__()

            )
            print(updated_transaction)

            updated = await self.db.update_transaction(transaction_id, updated_transaction)
            if updated:
                return PublicTransactionSchema(**updated.dict())

        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not update transaction")

        
    async def process_transaction(self, transaction: ProcessTransactionRequestSchema) -> Optional[TransactionInDBModel]:
        try:
            current_transaction = await self.get_transaction(transaction.transaction_id) 

            processed_transaction = TransactionInDBModel(
                **current_transaction.dict(),
                processed_at=time().__trunc__,
                transaction_status=TransactionStatus.PROCESSED,
            )
        
            return await self.db.update_transaction(processed_transaction)

        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not process transaction")


    async def void_transaction(self, transaction: VoidTransactionRequestSchema) -> Optional[TransactionInDBModel]:
        try:
            current_transaction = await self.get_transaction(transaction.transaction_id)
        
            void_transaction = TransactionInDBModel(
                **current_transaction.dict(),
                voided_at=time().__trunc__,
                updated_at=time().__trunc__,
                transaction_status=TransactionStatus.VOID,
            )

            return await self.db.update_transaction(void_transaction)
        
        except Exception as e: 
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not void transaction")
        
    
    async def dispute_transaction(self, transaction: VoidTransactionRequestSchema) -> Optional[TransactionInDBModel]:
        try:
            current_transaction = await self.get_transaction(transaction.transaction_id)
        
            disputed_transaction = TransactionInDBModel(
                **current_transaction.dict(),
                disputed=True,
                updated_at=time().__trunc__
            )

            return await self.db.update_transaction(disputed_transaction)
        
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not dispute transaction")

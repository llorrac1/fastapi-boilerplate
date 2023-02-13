from fastapi import APIRouter, Depends, HTTPException, status
from .schema import PublicTransactionSchema, CreatedTransactionSchema, NewTransactionRequestSchema, UpdateTransactionRequestSchema

from ...core.transactions.services import TransactionsService

txn_svc = TransactionsService()


router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
    responses={404: {"description": "Not found"}},
)


@router.post("/",
# , response_model=CreatedTransactionSchema, 
status_code=status.HTTP_201_CREATED)
async def create_transaction(request: NewTransactionRequestSchema):
    return await txn_svc.create_transaction(request)


@router.get("/{transaction_id}", response_model=PublicTransactionSchema)
async def get_transaction(transaction_id: str):
    return await txn_svc.get_transaction(transaction_id)


@router.put("/{transaction_id}", response_model=PublicTransactionSchema)
async def update_transaction(transaction_id: str, request: UpdateTransactionRequestSchema):
    return await txn_svc.update_transaction(transaction_id, request)

# Path: slick-ledger/app/api/transactions/schema.py


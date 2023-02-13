from fastapi import APIRouter, Depends, HTTPException, status

from .schema import NewGeneralLedgerAccountRequestSchema, GeneralLedgerAccountSchema, NewSubLedgerAccountRequestSchema, SubLedgerAccountSchema, NewLinkedAccountRequestSchema, LinkedAccountSchema, PublicAccountSchema, AccountBalanceSchema

from ...core.accounts.services import AccountService

acc_svc = AccountService()

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=GeneralLedgerAccountSchema)
async def create_general_ledger_account(
    request: NewGeneralLedgerAccountRequestSchema,
    # user: User = Depends(get_current_active_user),
):
    """Create a new general ledger account."""
    # created_account = GeneralLedgerAccountSchema(**request.dict())
    created = await acc_svc.create_general_ledger_account(request)
    if not created:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account not created")
    return created


@router.post("/sub/", response_model=SubLedgerAccountSchema)
async def create_sub_ledger_account(
    request: NewSubLedgerAccountRequestSchema,
    # user: User = Depends(get_current_active_user),
):
    """Create a new sub ledger account."""


@router.post("/linked/", response_model=LinkedAccountSchema)
async def create_linked_account(
    request: NewLinkedAccountRequestSchema,
    # user: User = Depends(get_current_active_user),
):
    """Create a new linked account."""


@router.get("/{account_id}", response_model=PublicAccountSchema)
async def get_account(
    account_id: str,
    # user: User = Depends(get_current_active_user),
):
    response = await acc_svc.get_account(account_id)
    return response


@router.get("/{account_id}/balance/"
, response_model=AccountBalanceSchema
)
async def get_account_balance(
    account_id: str,
    # user: User = Depends(get_current_active_user),
):
    response = await acc_svc.get_account_balance(account_id)
    return response


@router.get("/", response_model=list[PublicAccountSchema])
async def get_accounts(
    # account_holder_id: str = None,
    # user: User = Depends(get_current_active_user),
):
    """Get all accounts."""


@router.get("/sub/", response_model=list[SubLedgerAccountSchema])
async def get_sub_ledger_accounts(
    account_holder_id: str = None,
    # user: User = Depends(get_current_active_user),
):
    """Get all sub ledger accounts."""


@router.get("/linked/", response_model=list[LinkedAccountSchema])
async def get_linked_accounts(
    account_holder_id: str = None,
    # user: User = Depends(get_current_active_user),
):
    """Get all linked accounts."""



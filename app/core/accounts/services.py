from fastapi import Depends, HTTPException, status
from ...api.accounts.schema import NewSubLedgerAccountRequestSchema, SubLedgerAccountSchema, PublicAccountSchema, NewGeneralLedgerAccountRequestSchema, GeneralLedgerAccountSchema, NewLinkedAccountRequestSchema, LinkedAccountSchema, AccountBalanceSchema

from time import time
from datetime import datetime
from uuid import uuid4

from ...db.sqlite.accounts.db import AccountsDBController as AccountRepository

class AccountService:
    def __init__(self, account_repo: AccountRepository = AccountRepository()):
        self.account_repo = account_repo

    async def get_account(self, account_id: str) -> PublicAccountSchema:
        try: 
            account = await self.account_repo.get_account_by_id(account_id)
            if not account:
                # print(e)
                return None

            # balance = await self.get_account_balance(account_id)

            account_response = PublicAccountSchema(**account)
            return account_response

        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")


    async def create_general_ledger_account(self, request: NewGeneralLedgerAccountRequestSchema) -> GeneralLedgerAccountSchema:
        try: 
            new_created_account = GeneralLedgerAccountSchema(**request.dict(),
            id=uuid4().hex,
            created_at=time().__trunc__(),
            updated_at=time().__trunc__(),
            )
            print(new_created_account.dict())

            new_account_balance = AccountBalanceSchema(**request.dict(),
            id=new_created_account.id,
            created_at=time().__trunc__(),
            updated_at=time().__trunc__(),
            )
            print(new_account_balance.dict())

            created = await self.account_repo.create_account(new_created_account.dict())
            balance = await self.account_repo.create_account_balance(new_account_balance.dict())

            print(created, balance)
            if not created or not balance:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account not created")
            
            return PublicAccountSchema(**new_created_account.dict())
        
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account not created")
        

    async def get_sub_ledger_account(self, account_id: str) -> SubLedgerAccountSchema:
        account = await self.account_repo.get_sub_ledger_account(account_id)
        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
        
        account_response = SubLedgerAccountSchema(**account)
        return account_response


    async def get_general_ledger_account(self, account_id: str) -> GeneralLedgerAccountSchema:
        account = await self.account_repo.get_general_ledger_account(account_id)
        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

        account_response = GeneralLedgerAccountSchema(**account)
        return account_response
        

    async def get_linked_account(self, account_id: str) -> LinkedAccountSchema:
        account = await self.account_repo.get_linked_account(account_id)
        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")

        account_response = LinkedAccountSchema(**account)
        return account_response


    async def create_sub_ledger_account(self, request: NewSubLedgerAccountRequestSchema) -> SubLedgerAccountSchema:
        created_account = SubLedgerAccountSchema(**request.dict(),
        id=uuid4().hex,
        created_at=time(),
        updated_at=time(),
        )

        created = await self.account_repo.create_sub_ledger_account(created_account)
        if not created:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account not created")

        return created_account


    async def create_linked_account(self, request: NewLinkedAccountRequestSchema) -> LinkedAccountSchema:
        created_account = LinkedAccountSchema(**request.dict(),
        id=uuid4().hex,
        created_at=time(),
        updated_at=time(),
        )

        created = await self.account_repo.create_linked_account(created_account)
        if not created:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Account not created")

        return created_account


    async def get_all_accounts(self, account_holder_id: str = None) -> list[PublicAccountSchema]:
        try: 
            accounts = await self.account_repo.get_all_accounts(account_holder_id=account_holder_id)
            if not accounts:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Accounts not found")

            accounts_response = [PublicAccountSchema(**account) for account in accounts]
            return accounts_response

        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unable to retrieve accounts")


    async def get_all_sub_ledger_accounts(self, account_holder_id: str = None) -> list[SubLedgerAccountSchema]:
        try:
            accounts = await self.account_repo.get_all_sub_ledger_accounts(account_holder_id=account_holder_id)

            if not accounts:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Accounts not found")
            
            accounts_response = [SubLedgerAccountSchema(**account) for account in accounts]
            return accounts_response
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unable to retrieve accounts")
        


    async def get_all_general_ledger_accounts(self) -> list[GeneralLedgerAccountSchema]:
        try: 
            accounts = await self.account_repo.get_all_general_ledger_accounts()
            if not accounts:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Accounts not found")

            accounts_response = [GeneralLedgerAccountSchema(**account) for account in accounts]
            return accounts_response
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unable to retrieve accounts")


    async def get_all_linked_accounts(self) -> list[LinkedAccountSchema]:
        try:
            accounts = await self.account_repo.get_all_linked_accounts()
            if not accounts:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Accounts not found")

            accounts_response = [LinkedAccountSchema(**account) for account in accounts]
            return accounts_response
        
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unable to retrieve accounts")


    async def get_account_balance(self, account_id: str) -> AccountBalanceSchema:
        try:
            account_balance = await self.account_repo.get_account_balance(account_id)
            if not account_balance:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
            
            return AccountBalanceSchema(**account_balance)
        
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Unable to retrieve account balance")


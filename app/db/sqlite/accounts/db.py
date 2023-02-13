from sqlmodel import SQLModel, Relationship, Field, create_engine, Session, select, JSON
from decimal import Decimal
from typing import Optional, Dict, List
from datetime import datetime
from uuid import uuid4


class AccountBase(SQLModel):
    id: str = Field(primary_key=True, index=True, description="Account ID")
    account_name: str = Field(description="The name of the account")
    account_type: str = Field(description="The type of account this is such as CHECK")
    balance: float = Field(0, description="The current balance of the account")
    available_balance: float = Field(0, description="The current available balance of the account")
    currency: str = Field(description="The currency of the account")
    account_holder_id: str = Field(index=True, description="The ID of the account holder")
    active: bool = Field(True, index=True, description="Whether the account is active or not")
    created_at: datetime = Field(description="The date and time the account was created")
    updated_at: datetime = Field(description="The date and time the account was last updated")

    class Config: 
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class AccountBalance(SQLModel, table=True): 
    id: str = Field(primary_key=True, index=True, description="The ID of the account")
    balance: float = Field(0, description="The current balance of the account")
    available_balance: float = Field(0, description="The current available balance of the account")
    created_at: float = Field(0, description="The date and time the account was created")
    updated_at: float = Field(0, description="The date and time the account was last updated")

    class Config: 
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class Account(AccountBase, table=True):
    pass


class SubLedgerAccount(Account, table=True):
    parent_account_id: str = Field(description="The ID of the parent account", foreign_key="account.id")


class GeneralLedgerAccount(Account):
    sub_ledger_accounts: List[SubLedgerAccount] | None = Relationship(
        back_populates="SubLedgerAccounts"
    )


class LinkedAccount(Account, table=True):
    linked_account_id: str = Field(description="The ID of the linked account", index=True)
    institution_id: str = Field(description="The ID of the institution")
    institution_name: str = Field(description="The name of the institution")
    linked_account_status: str = Field(description="The status of the linked account")
    link_authorized_at: datetime = Field(description="The date and time the account was authorized")


sqlite_file_name = "accounts.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url
# , echo=True
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def drop_db_and_tables():
    SQLModel.metadata.drop_all(engine)


class AccountDB:
    def __init__(self):
        self.session = Session(engine)
        create_db_and_tables()


    async def get_account_by_id(self, account_id: str) -> AccountBase:
        base_account = self.session.get(Account, account_id)
        if not base_account:
            sub_ledger_account = self.session.get(SubLedgerAccount,account_id)
            print(sub_ledger_account)
            return sub_ledger_account.dict()
        print(base_account)
        return base_account.dict()


    async def create_account(self, account: dict) -> Account:
        try:
            new_account = Account(**account)
            print(f"Creating account {new_account.id}")
            self.session.add(new_account)
            self.session.commit()
            self.session.refresh(new_account)
            return new_account.dict()
        except Exception as e:
            print(e)


    async def get_all_accounts(self) -> List[dict]:
        base_accounts = [account.dict() for account in self.session.query(AccountBase).all()]
        sub_ledger_accounts = [account.dict() for account in self.session.query(SubLedgerAccount).all()]
        general_ledger_accounts = [account.dict() for account in self.session.query(GeneralLedgerAccount).all()]
    
        return base_accounts + sub_ledger_accounts + general_ledger_accounts

    
    async def get_general_ledger_account(self, account_id: str) -> dict:
        try: 
            general_ledger_account = self.session.query(GeneralLedgerAccount).get(account_id)
            return general_ledger_account.dict()
        except Exception as e:
            print(e)
            return None


    async def get_sub_ledger_account(self, account_id: str) -> dict:
        try: 
            sub_ledger_account = SubLedgerAccount(**self.session.get(SubLedgerAccount, account_id))
            return sub_ledger_account
        except Exception as e:
            print(e)
            return None


    async def update_account(self, account: AccountBase) -> AccountBase:
        try:
            self.session.query(AccountBase).filter(AccountBase.id == account.id).update(account.dict())
            self.session.commit()
            self.session.refresh(account)
            return account
        except Exception as e:
            print(e)


    async def create_sub_ledger_account(self, sub_ledger_account: SubLedgerAccount) -> SubLedgerAccount:
        try:
            new_sub_ledger_account = SubLedgerAccount(**sub_ledger_account)
            self.session.add(new_sub_ledger_account)
            self.session.commit()
            self.session.refresh(new_sub_ledger_account)
            return new_sub_ledger_account.dict()
        except Exception as e:
            print(e)

    
    async def update_sub_ledger_account(self, sub_ledger_account: SubLedgerAccount) -> SubLedgerAccount:
        try:
            self.session.query(SubLedgerAccount).filter(SubLedgerAccount.id == sub_ledger_account.id).update(sub_ledger_account.dict())
            self.session.commit()
            self.session.refresh(sub_ledger_account)
            return sub_ledger_account.dict()
        except Exception as e:
            print(e)
    
    
    def balance_constructor(account_id, balance, available_balance):
        return {
            "account_id": account_id,
            "balance": balance,
            "available_balance": available_balance,
        }
    

    async def get_account_balance(self, account_id: str) -> dict:
        try:
            account = self.session.get(Account, account_id)
            
            if not account:
                sub_ledger_account = self.session.get(SubLedgerAccount, account_id)
                
                if not sub_ledger_account:
                    return None
    
                return self.balance_constructor(account_id, sub_ledger_account.balance, sub_ledger_account.available_balance)

            print(account)
            return {
            "account_id": account_id,
            "balance": account.balance,
            "available_balance": account.available_balance,
        }

        except Exception as e:
            print(e)
            return None


    async def update_account_balance(self, account_id: str, balance: float = None, available_balance: float = None) -> dict: 
        try:
            account = self.session.get(Account, account_id)
            
            if not account:
                sub_ledger_account = self.session.get(SubLedgerAccount, account_id)
                
                if not sub_ledger_account:
                    return None
                
                account = sub_ledger_account
            
            if balance:
                account.balance = balance
            
            if available_balance:
                account.available_balance = available_balance

            self.session.commit()
            self.session.refresh(account)
            return self.balance_constructor(account.balance, account.available_balance)
        
        except Exception as e:
            print(e)
            return None


class AccountBalanceDB:
    def __init__(self):
        self.session = Session(engine)
        create_db_and_tables()

    def __balance_constructor(account_id, balance, available_balance):
        return {
            "account_id": account_id,
            "balance": balance,
            "available_balance": available_balance,
        }


    async def get_account_balance(self, account_id: str) -> dict:
        try:
            account_balance = self.session.get(AccountBalance, account_id)
            
            if not account_balance:
                return None

            print(account_balance)
            return self.__balance_constructor(account_id, account_balance.balance, account_balance.available_balance)
        
        except Exception as e:
            print(e)
            return None
        
    
    async def update_account_balance(self, account_id: str, balance: float = None, available_balance: float = None) -> dict:
        try:
            account_balance = self.session.get(AccountBalance, account_id)
            
            if not account_balance:
                return None
            
            if balance:
                account_balance.balance = balance
            
            if available_balance:
                account_balance.available_balance = available_balance
            
            self.session.commit()
            self.session.refresh(account_balance)
            return self.__balance_constructor(account_id, account_balance.balance, account_balance.available_balance)

        except Exception as e:
            print(e)
            return None

    
    async def create_account_balance(self, account_balance: dict) -> dict:
        try:
            new_account_balance = AccountBalance(**account_balance)
            self.session.add(new_account_balance)
            self.session.commit()
            self.session.refresh(new_account_balance)
            return {
                "account_id": new_account_balance.id,
                "balance": new_account_balance.balance,
                "available_balance": new_account_balance.available_balance,
            }
        
        except Exception as e:
            print(e)
            return None


class AccountsDBController:
    def __init__(self):
        self.accounts_db = AccountDB()
        self.account_balance_db = AccountBalanceDB()

    async def get_all_accounts(self) -> List[dict]:
        return await self.accounts_db.get_all_accounts()
    
    async def get_account_balance(self, account_id: str) -> dict:
        return await self.account_balance_db.get_account_balance(account_id)

    async def update_account_balance(self, account_id: str, balance: float = None, available_balance: float = None) -> dict:
        return await self.account_balance_db.update_account_balance(account_id, balance, available_balance)
    
    async def create_account_balance(self, account_balance: dict) -> dict:
        return await self.account_balance_db.create_account_balance(account_balance)

    async def get_general_ledger_account(self, account_id: str) -> dict:
        return await self.accounts_db.get_general_ledger_account(account_id)

    async def get_sub_ledger_account(self, account_id: str) -> dict:
        return await self.accounts_db.get_sub_ledger_account(account_id)
    
    async def get_account_by_id(self, account_id: str) -> dict:
        return await self.accounts_db.get_account(account_id)

    async def update_account(self, account: Account) -> AccountBase:
        return await self.accounts_db.update_account(account)
    
    async def create_sub_ledger_account(self, sub_ledger_account: SubLedgerAccount) -> SubLedgerAccount:
        return await self.accounts_db.create_sub_ledger_account(sub_ledger_account)
    
    async def update_sub_ledger_account(self, sub_ledger_account: SubLedgerAccount) -> SubLedgerAccount:
        return await self.accounts_db.update_sub_ledger_account(sub_ledger_account)

    async def create_account(self, account: Account) -> AccountBase:
        return await self.accounts_db.create_account(account)
    
    async def update_account(self, account: Account) -> AccountBase:
        return await self.accounts_db.update_account(account)

    
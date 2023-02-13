from tinydb import TinyDB, Query

## Set up tinydb 
account_db = TinyDB("accounts.json")


class AccountDBService:
    def __init__(self):
        self.account_repo = account_db
        self.account_repo.default_table_name = "accounts"

    async def get_account_by_id(self, account_id: str) -> dict:
        account = await self.account_repo.get(account_id)
        if not account:
            return None
        return account


    async def create_account(self, account: dict) -> dict:
        created = await self.account_repo.insert(account)
        if not created:
            return None
        return created

    
    async def get_account_by_parent_id(self, parent_id: str) -> dict:
        Account_search = Query()
        account = await self.account_repo.search(Account_search.parent_id == parent_id)
        if not account:
            return None
        return account


    async def update_account_balance(self, account_id: str, balance: float = None, available_balance: float = None) -> dict:
        account = await self.account_repo.get(account_id)
        if not account:
            return None
        
        if balance:
            account.balance = balance
        
        if available_balance:
            account.available_balance = available_balance
        
        updated = await self.account_repo.update(account, account_id)
        if not updated:
            return None
        return account
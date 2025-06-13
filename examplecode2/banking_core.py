
class EnterpriseBankingSystem:
    def __init__(self):
        self.accounts = {}
        self.next_account_id = 1
        
    def create_account(self, customer_info: dict, currency: str) -> dict:
        account_id = f'acc_{self.next_account_id}'
        self.accounts[account_id] = {
            'customer_info': customer_info,
            'currency': currency,
            'balance': 0.0,
        }
        self.next_account_id += 1
        return {'account_id': account_id, **self.accounts[account_id]}

    def get_account_details(self, account_id: str) -> dict:
        return self.accounts.get(account_id, None)

    def deposit(self, account_id: str, amount: float) -> bool:
        if amount <= 0 or account_id not in self.accounts:
            return False
        self.accounts[account_id]['balance'] += amount
        return True

    def withdraw(self, account_id: str, amount: float) -> bool:
        if amount <= 0 or account_id not in self.accounts or self.accounts[account_id]['balance'] < amount:
            return False
        self.accounts[account_id]['balance'] -= amount
        return True

    def transfer(self, from_account_id: str, to_account_id: str, amount: float) -> bool:
        if self.withdraw(from_account_id, amount) and self.deposit(to_account_id, amount):
            return True
        return False


# Example usage
bank_system = EnterpriseBankingSystem()
account_info = bank_system.create_account({'name': 'John Doe', 'id': '123'}, 'USD')
print('New Account:', account_info)
account_details = bank_system.get_account_details(account_info['account_id'])
print('Account Details:', account_details)
transfer_result = bank_system.transfer(account_info['account_id'], 'acc_2', 50.0)  # This should fail due to non-existing account
print('Transfer Result:', transfer_result)

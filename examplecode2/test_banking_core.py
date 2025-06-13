import unittest
from banking_core import EnterpriseBankingSystem

class TestEnterpriseBankingSystem(unittest.TestCase):
    def setUp(self):
        self.bank = EnterpriseBankingSystem()
        self.customer_info = {'name': 'John Doe', 'id': '123'}
        self.account = self.bank.create_account(self.customer_info, 'USD')

    def test_create_account(self):
        # Test account creation
        self.assertEqual(self.account['customer_info'], self.customer_info)
        self.assertEqual(self.account['currency'], 'USD')
        self.assertEqual(self.account['balance'], 0.0)
        self.assertTrue(self.account['account_id'].startswith('acc_'))

    def test_get_account_details(self):
        # Test getting existing account
        details = self.bank.get_account_details(self.account['account_id'])
        self.assertEqual(details, self.account)
        
        # Test getting non-existing account
        self.assertIsNone(self.bank.get_account_details('nonexistent_account'))

    def test_deposit(self):
        # Test valid deposit
        initial_balance = self.account['balance']
        deposit_amount = 100.0
        self.assertTrue(self.bank.deposit(self.account['account_id'], deposit_amount))
        details = self.bank.get_account_details(self.account['account_id'])
        self.assertEqual(details['balance'], initial_balance + deposit_amount)
        
        # Test invalid deposit (negative amount)
        self.assertFalse(self.bank.deposit(self.account['account_id'], -50.0))
        
        # Test deposit to non-existing account
        self.assertFalse(self.bank.deposit('nonexistent_account', 100.0))

    def test_withdraw(self):
        # Setup - deposit some money first
        self.bank.deposit(self.account['account_id'], 200.0)
        
        # Test valid withdrawal
        initial_balance = self.bank.get_account_details(self.account['account_id'])['balance']
        withdraw_amount = 100.0
        self.assertTrue(self.bank.withdraw(self.account['account_id'], withdraw_amount))
        details = self.bank.get_account_details(self.account['account_id'])
        self.assertEqual(details['balance'], initial_balance - withdraw_amount)
        
        # Test invalid withdrawal (negative amount)
        self.assertFalse(self.bank.withdraw(self.account['account_id'], -50.0))
        
        # Test withdrawal exceeding balance
        self.assertFalse(self.bank.withdraw(self.account['account_id'], 1000.0))
        
        # Test withdrawal from non-existing account
        self.assertFalse(self.bank.withdraw('nonexistent_account', 100.0))

    def test_transfer(self):
        # Setup - create two accounts and deposit to first
        account2 = self.bank.create_account({'name': 'Jane Doe', 'id': '456'}, 'USD')
        self.bank.deposit(self.account['account_id'], 200.0)
        
        # Test valid transfer
        initial_balance1 = self.bank.get_account_details(self.account['account_id'])['balance']
        initial_balance2 = self.bank.get_account_details(account2['account_id'])['balance']
        transfer_amount = 100.0
        
        self.assertTrue(self.bank.transfer(
            self.account['account_id'], 
            account2['account_id'], 
            transfer_amount
        ))
        
        details1 = self.bank.get_account_details(self.account['account_id'])
        details2 = self.bank.get_account_details(account2['account_id'])
        
        self.assertEqual(details1['balance'], initial_balance1 - transfer_amount)
        self.assertEqual(details2['balance'], initial_balance2 + transfer_amount)
        
        # Test transfer with insufficient funds
        self.assertFalse(self.bank.transfer(
            self.account['account_id'], 
            account2['account_id'], 
            1000.0
        ))
        
        # Test transfer to non-existing account
        self.assertFalse(self.bank.transfer(
            self.account['account_id'], 
            'nonexistent_account', 
            50.0
        ))
        
        # Test transfer from non-existing account
        self.assertFalse(self.bank.transfer(
            'nonexistent_account', 
            account2['account_id'], 
            50.0
        ))

if __name__ == '__main__':
    unittest.main()
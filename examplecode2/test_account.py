import unittest
from datetime import datetime
from account import Account, get_share_price


class TestAccount(unittest.TestCase):
    def setUp(self):
        self.user_id = 'test_user'
        self.account = Account(self.user_id)
    
    def test_initial_state(self):
        self.assertEqual(self.account.user_id, self.user_id)
        self.assertEqual(self.account.balance, 0.0)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(self.account.transactions, [])
        self.assertEqual(self.account.total_deposits, 0.0)
        self.assertEqual(self.account.total_withdrawals, 0.0)
    
    def test_deposit_funds_positive(self):
        result = self.account.deposit_funds(100.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 100.0)
        self.assertEqual(self.account.total_deposits, 100.0)
        self.assertEqual(len(self.account.transactions), 1)
        self.assertEqual(self.account.transactions[0]['type'], 'DEPOSIT')
    
    def test_deposit_funds_negative(self):
        result = self.account.deposit_funds(-50.0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 0.0)
        self.assertEqual(self.account.total_deposits, 0.0)
        self.assertEqual(len(self.account.transactions), 0)
    
    def test_withdraw_funds_sufficient(self):
        self.account.deposit_funds(200.0)
        result = self.account.withdraw_funds(100.0)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 100.0)
        self.assertEqual(self.account.total_withdrawals, 100.0)
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1]['type'], 'WITHDRAWAL')
    
    def test_withdraw_funds_insufficient(self):
        self.account.deposit_funds(50.0)
        result = self.account.withdraw_funds(100.0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 50.0)
        self.assertEqual(self.account.total_withdrawals, 0.0)
        self.assertEqual(len(self.account.transactions), 1)
    
    def test_withdraw_funds_negative(self):
        result = self.account.withdraw_funds(-50.0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 0.0)
        self.assertEqual(self.account.total_withdrawals, 0.0)
        self.assertEqual(len(self.account.transactions), 0)
    
    def test_buy_shares_success(self):
        self.account.deposit_funds(1000.0)
        result = self.account.buy_shares('AAPL', 2)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, 1000.0 - (150.0 * 2))
        self.assertEqual(self.account.holdings, {'AAPL': 2})
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.transactions[1]['type'], 'BUY')
    
    def test_buy_shares_insufficient_funds(self):
        self.account.deposit_funds(100.0)
        result = self.account.buy_shares('GOOGL', 1)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 100.0)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(len(self.account.transactions), 1)
    
    def test_buy_shares_invalid_symbol(self):
        self.account.deposit_funds(1000.0)
        result = self.account.buy_shares('INVALID', 1)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(len(self.account.transactions), 1)
    
    def test_buy_shares_invalid_quantity(self):
        self.account.deposit_funds(1000.0)
        result = self.account.buy_shares('AAPL', 0)
        self.assertFalse(result)
        self.assertEqual(self.account.balance, 1000.0)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(len(self.account.transactions), 1)
    
    def test_sell_shares_success(self):
        self.account.deposit_funds(1000.0)
        self.account.buy_shares('AAPL', 3)
        initial_balance = self.account.balance
        result = self.account.sell_shares('AAPL', 2)
        self.assertTrue(result)
        self.assertEqual(self.account.balance, initial_balance + (150.0 * 2))
        self.assertEqual(self.account.holdings, {'AAPL': 1})
        self.assertEqual(len(self.account.transactions), 3)
        self.assertEqual(self.account.transactions[2]['type'], 'SELL')
    
    def test_sell_shares_insufficient_quantity(self):
        self.account.deposit_funds(1000.0)
        self.account.buy_shares('AAPL', 1)
        result = self.account.sell_shares('AAPL', 2)
        self.assertFalse(result)
        self.assertEqual(self.account.holdings, {'AAPL': 1})
        self.assertEqual(len(self.account.transactions), 2)
    
    def test_sell_shares_invalid_symbol(self):
        self.account.deposit_funds(1000.0)
        result = self.account.sell_shares('INVALID', 1)
        self.assertFalse(result)
        self.assertEqual(self.account.holdings, {})
        self.assertEqual(len(self.account.transactions), 1)
    
    def test_sell_shares_invalid_quantity(self):
        self.account.deposit_funds(1000.0)
        self.account.buy_shares('AAPL', 1)
        result = self.account.sell_shares('AAPL', 0)
        self.assertFalse(result)
        self.assertEqual(self.account.holdings, {'AAPL': 1})
        self.assertEqual(len(self.account.transactions), 2)
    
    def test_calculate_portfolio_value(self):
        self.account.deposit_funds(1000.0)
        self.account.buy_shares('AAPL', 2)
        self.account.buy_shares('TSLA', 1)
        expected_value = self.account.balance + (150.0 * 2) + (800.0 * 1)
        self.assertEqual(self.account.calculate_portfolio_value(), expected_value)
    
    def test_calculate_profit_loss(self):
        self.account.deposit_funds(1000.0)
        self.account.buy_shares('AAPL', 2)
        self.account.withdraw_funds(200.0)
        current_value = self.account.calculate_portfolio_value()
        expected_pl = current_value - 1000.0 + 200.0
        self.assertEqual(self.account.calculate_profit_loss(), expected_pl)
    
    def test_get_holdings(self):
        self.account.deposit_funds(1000.0)
        self.account.buy_shares('AAPL', 2)
        holdings = self.account.get_holdings()
        self.assertEqual(holdings, {'AAPL': 2})
        # Test that returned dict is a copy
        holdings['AAPL'] = 3
        self.assertEqual(self.account.holdings, {'AAPL': 2})
    
    def test_get_transaction_history(self):
        self.account.deposit_funds(1000.0)
        self.account.buy_shares('AAPL', 2)
        transactions = self.account.get_transaction_history()
        self.assertEqual(len(transactions), 2)
        # Test that returned list is a copy
        transactions.append({'test': 'data'})
        self.assertEqual(len(self.account.transactions), 2)


class TestGetSharePrice(unittest.TestCase):
    def test_get_share_price_valid(self):
        self.assertEqual(get_share_price('AAPL'), 150.0)
        self.assertEqual(get_share_price('TSLA'), 800.0)
        self.assertEqual(get_share_price('GOOGL'), 2500.0)
    
    def test_get_share_price_invalid(self):
        self.assertEqual(get_share_price('INVALID'), 0.0)


if __name__ == '__main__':
    unittest.main()
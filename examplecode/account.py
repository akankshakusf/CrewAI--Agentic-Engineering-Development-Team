from datetime import datetime
from typing import List, Dict, Any


def get_share_price(symbol: str) -> float:
    """Returns the current price of shares for the given stock symbol.
    This is a test implementation with fixed prices for specific symbols.
    
    Args:
        symbol (str): The stock symbol.
        
    Returns:
        float: Price of the share as a float.
    """
    prices = {
        'AAPL': 150.0,
        'TSLA': 800.0,
        'GOOGL': 2500.0
    }
    return prices.get(symbol, 0.0)


class Account:
    """Simulates a user's trading account for a trading simulation platform."""

    def __init__(self, user_id: str):
        """Initializes a new account for a user with a unique user ID.

        Args:
            user_id (str): Unique identifier for the user.
        """
        self.user_id = user_id
        self.balance = 0.0
        self.holdings = {}  # Format: {symbol: quantity}
        self.transactions = []  # List of transaction records
        self.total_deposits = 0.0
        self.total_withdrawals = 0.0

    def deposit_funds(self, amount: float) -> bool:
        """Deposits a specified amount of funds into the user's account.

        Args:
            amount (float): The amount to be deposited.

        Returns:
            bool: True if deposit is successful, False if the amount is negative or invalid.
        """
        if amount <= 0:
            return False
        
        self.balance += amount
        self.total_deposits += amount
        
        # Record the transaction
        self.transactions.append({
            'type': 'DEPOSIT',
            'amount': amount,
            'timestamp': datetime.now(),
            'balance_after': self.balance
        })
        
        return True

    def withdraw_funds(self, amount: float) -> bool:
        """Withdraws a specified amount from the user's account, ensuring the balance doesn't go negative.

        Args:
            amount (float): The amount to be withdrawn.

        Returns:
            bool: True if withdrawal is successful, False if insufficient funds or invalid amount.
        """
        if amount <= 0 or amount > self.balance:
            return False
        
        self.balance -= amount
        self.total_withdrawals += amount
        
        # Record the transaction
        self.transactions.append({
            'type': 'WITHDRAWAL',
            'amount': amount,
            'timestamp': datetime.now(),
            'balance_after': self.balance
        })
        
        return True

    def buy_shares(self, symbol: str, quantity: int) -> bool:
        """Buys a quantity of shares for a given stock symbol, if the funds in the account are sufficient.

        Args:
            symbol (str): The stock symbol to buy.
            quantity (int): The number of shares to buy.

        Returns:
            bool: True if purchase is successful, False if insufficient funds or invalid parameters.
        """
        if not symbol or quantity <= 0:
            return False
        
        share_price = get_share_price(symbol)
        if share_price <= 0:
            return False  # Invalid symbol or price
        
        total_cost = share_price * quantity
        
        if total_cost > self.balance:
            return False  # Insufficient funds
        
        # Update balance
        self.balance -= total_cost
        
        # Update holdings
        if symbol in self.holdings:
            self.holdings[symbol] += quantity
        else:
            self.holdings[symbol] = quantity
        
        # Record the transaction
        self.transactions.append({
            'type': 'BUY',
            'symbol': symbol,
            'quantity': quantity,
            'price_per_share': share_price,
            'total_amount': total_cost,
            'timestamp': datetime.now(),
            'balance_after': self.balance
        })
        
        return True

    def sell_shares(self, symbol: str, quantity: int) -> bool:
        """Sells a quantity of shares for a given stock symbol, assuming the user owns enough shares.

        Args:
            symbol (str): The stock symbol to sell.
            quantity (int): The number of shares to sell.

        Returns:
            bool: True if sale is successful, False if the user doesn't own enough shares or if invalid parameters.
        """
        if not symbol or quantity <= 0 or symbol not in self.holdings or self.holdings[symbol] < quantity:
            return False
        
        share_price = get_share_price(symbol)
        if share_price <= 0:
            return False  # Invalid symbol or price
        
        total_sale = share_price * quantity
        
        # Update balance
        self.balance += total_sale
        
        # Update holdings
        self.holdings[symbol] -= quantity
        if self.holdings[symbol] == 0:
            del self.holdings[symbol]  # Remove the symbol if no shares left
        
        # Record the transaction
        self.transactions.append({
            'type': 'SELL',
            'symbol': symbol,
            'quantity': quantity,
            'price_per_share': share_price,
            'total_amount': total_sale,
            'timestamp': datetime.now(),
            'balance_after': self.balance
        })
        
        return True

    def calculate_portfolio_value(self) -> float:
        """Calculates the total value of the user's portfolio based on current share prices.

        Returns:
            float: Total portfolio value.
        """
        total_value = self.balance  # Start with the cash balance
        
        for symbol, quantity in self.holdings.items():
            share_price = get_share_price(symbol)
            total_value += share_price * quantity
        
        return total_value

    def calculate_profit_loss(self) -> float:
        """Calculates the profit or loss from the user's initial deposit, taking into account
        the current portfolio value and withdrawn funds.

        Returns:
            float: Total profit or loss.
        """
        current_value = self.calculate_portfolio_value()
        return current_value - self.total_deposits + self.total_withdrawals

    def get_holdings(self) -> Dict[str, int]:
        """Provides a summary of the user's current share holdings.

        Returns:
            dict: A dictionary where keys are stock symbols and values are quantities owned.
        """
        return self.holdings.copy()

    def get_transaction_history(self) -> List[Dict[str, Any]]:
        """Lists all transactions the user has made over time.

        Returns:
            list: A list of transaction records, each containing details about the transaction.
        """
        return self.transactions.copy()
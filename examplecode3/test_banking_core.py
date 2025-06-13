import unittest
from banking_core import Customer, Account, Transaction, CreditCard, Loan, AccessControl, EnterpriseBankingSystem

class TestBankingCore(unittest.TestCase):
    def test_customer_creation(self):
        customer = Customer(customer_id="CUST1234", first_name="John", last_name="Doe", dob="1990-01-01", address="123 Main St", contact_info="john@example.com", id_documents={"passport": "ABC123"}, kyc_status="pending")
        self.assertEqual(customer.customer_id, "CUST1234")
        self.assertEqual(customer.first_name, "John")
        self.assertEqual(customer.last_name, "Doe")
        self.assertEqual(customer.dob, "1990-01-01")
        self.assertEqual(customer.address, "123 Main St")
        self.assertEqual(customer.contact_info, "john@example.com")
        self.assertEqual(customer.id_documents, {"passport": "ABC123"})
        self.assertEqual(customer.kyc_status, "pending")

    def test_account_creation(self):
        account = Account(account_id="ACC1234", customer_id="CUST1234", account_type="checking", currency="USD", balance=1000.0)
        self.assertEqual(account.account_id, "ACC1234")
        self.assertEqual(account.customer_id, "CUST1234")
        self.assertEqual(account.account_type, "checking")
        self.assertEqual(account.currency, "USD")
        self.assertEqual(account.balance, 1000.0)

    def test_transaction_creation(self):
        transaction = Transaction(transaction_id="TRANS1234", account_id="ACC1234", amount=100.0, currency="USD", transaction_type="deposit")
        self.assertEqual(transaction.transaction_id, "TRANS1234")
        self.assertEqual(transaction.account_id, "ACC1234")
        self.assertEqual(transaction.amount, 100.0)
        self.assertEqual(transaction.currency, "USD")
        self.assertEqual(transaction.transaction_type, "deposit")

    def test_credit_card_creation(self):
        credit_card = CreditCard(card_id="CARD1234", customer_id="CUST1234", card_type="visa", credit_limit=1000.0, balance=0.0)
        self.assertEqual(credit_card.card_id, "CARD1234")
        self.assertEqual(credit_card.customer_id, "CUST1234")
        self.assertEqual(credit_card.card_type, "visa")
        self.assertEqual(credit_card.credit_limit, 1000.0)
        self.assertEqual(credit_card.balance, 0.0)

    def test_loan_creation(self):
        loan = Loan(loan_id="LOAN1234", customer_id="CUST1234", loan_type="personal", amount=1000.0, currency="USD", term_months=12, status="pending")
        self.assertEqual(loan.loan_id, "LOAN1234")
        self.assertEqual(loan.customer_id, "CUST1234")
        self.assertEqual(loan.loan_type, "personal")
        self.assertEqual(loan.amount, 1000.0)
        self.assertEqual(loan.currency, "USD")
        self.assertEqual(loan.term_months, 12)
        self.assertEqual(loan.status, "pending")

    def test_access_control(self):
        access_control = AccessControl()
        access_control.add_role("user1", "admin", ["create_account", "process_deposit"])
        self.assertTrue(access_control.check_permission("user1", "create_account"))
        self.assertTrue(access_control.check_permission("user1", "process_deposit"))
        self.assertFalse(access_control.check_permission("user1", "withdraw"))

    def test_enterprise_banking_system(self):
        banking_system = EnterpriseBankingSystem("Bank of America", "BOA1234", "encryption_key")
        self.assertEqual(banking_system.institution_name, "Bank of America")
        self.assertEqual(banking_system.institution_id, "BOA1234")
        self.assertEqual(banking_system._encryption_key, "encryption_key")

    def test_register_customer(self):
        banking_system = EnterpriseBankingSystem("Bank of America", "BOA1234", "encryption_key")
        access_control = AccessControl()
        access_control.add_role("user1", "admin", ["register_customer"])
        banking_system._access_control = access_control
        customer_data = {"first_name": "John", "last_name": "Doe", "dob": "1990-01-01", "address": "123 Main St", "contact_info": "john@example.com", "id_documents": {"passport": "ABC123"}, "kyc_status": "pending"}
        self.assertIsNotNone(banking_system.register_customer(customer_data, "user1"))

    def test_create_account(self):
        banking_system = EnterpriseBankingSystem("Bank of America", "BOA1234", "encryption_key")
        access_control = AccessControl()
        access_control.add_role("user1", "admin", ["create_account"])
        banking_system._access_control = access_control
        customer_id = "CUST1234"
        account_type = "checking"
        currency = "USD"
        initial_deposit = 1000.0
        self.assertIsNotNone(banking_system.create_account(customer_id, account_type, currency, initial_deposit, "user1"))

    def test_process_deposit(self):
        banking_system = EnterpriseBankingSystem("Bank of America", "BOA1234", "encryption_key")
        access_control = AccessControl()
        access_control.add_role("user1", "admin", ["process_deposit"])
        banking_system._access_control = access_control
        account_id = "ACC1234"
        amount = 100.0
        currency = "USD"
        source = "Source"
        transaction_data = {}
        self.assertIsNotNone(banking_system.process_deposit(account_id, amount, currency, source, transaction_data, "user1"))

if __name__ == '__main__':
    unittest.main()
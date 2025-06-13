from datetime import datetime
import random

class Customer:
    def __init__(self, customer_id, first_name, last_name, dob, address, contact_info, 
                 id_documents, kyc_status="pending"):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        self.address = address
        self.contact_info = contact_info
        self.id_documents = id_documents
        self.kyc_status = kyc_status
        self.accounts = []
        self.credit_cards = []
        self.loans = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update_profile(self, field, value):
        if hasattr(self, field):
            setattr(self, field, value)
            self.updated_at = datetime.now()
            return True
        return False

    def verify_kyc(self):
        # Placeholder for real KYC verification logic
        self.kyc_status = "verified"
        return True

    def get_customer_summary(self):
        return {
            "customer_id": self.customer_id,
            "full_name": f"{self.first_name} {self.last_name}",
            "accounts": len(self.accounts),
            "credit_cards": len(self.credit_cards),
            "loans": len(self.loans),
            "kyc_status": self.kyc_status
        }


class Account:
    def __init__(self, account_id, customer_id, account_type, currency, balance=0.0):
        self.account_id = account_id
        self.customer_id = customer_id
        self.account_type = account_type
        self.currency = currency
        self.balance = balance
        self.created_at = datetime.now()


class Transaction:
    def __init__(self, transaction_id, account_id, amount, currency, transaction_type, timestamp=None):
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.amount = amount
        self.currency = currency
        self.transaction_type = transaction_type
        self.timestamp = timestamp or datetime.now()


class CreditCard:
    def __init__(self, card_id, customer_id, card_type, credit_limit, balance=0.0):
        self.card_id = card_id
        self.customer_id = customer_id
        self.card_type = card_type
        self.credit_limit = credit_limit
        self.balance = balance


class Loan:
    def __init__(self, loan_id, customer_id, loan_type, amount, currency, term_months, status="pending"):
        self.loan_id = loan_id
        self.customer_id = customer_id
        self.loan_type = loan_type
        self.amount = amount
        self.currency = currency
        self.term_months = term_months
        self.status = status


class AccessControl:
    def __init__(self):
        self.roles = {}

    def add_role(self, username, role, permissions):
        if username not in self.roles:
            self.roles[username] = {"role": role, "permissions": permissions}
            return True
        return False

    def check_permission(self, username, permission):
        user_role = self.roles.get(username)
        if user_role and permission in user_role.get("permissions", []):
            return True
        return False


class EnterpriseBankingSystem:
    def __init__(self, institution_name, institution_id, encryption_key):
        self.institution_name = institution_name
        self.institution_id = institution_id
        self._encryption_key = encryption_key
        self._customers = {}  # customer_id -> Customer
        self._accounts = {}   # account_id -> Account
        self._transactions = []
        self._credit_cards = {}  # card_id -> CreditCard
        self._loans = {}  # loan_id -> Loan
        self._audit_log = []
        self._access_control = AccessControl()

    def register_customer(self, customer_data, user_role):
        if not self._access_control.check_permission(user_role, "register_customer"):
            raise PermissionError("User does not have permission to register customers.")
        new_customer_id = f"CUST{random.randint(1000, 9999)}"
        new_customer = Customer(customer_id=new_customer_id, **customer_data)
        if new_customer.verify_kyc():
            self._customers[new_customer_id] = new_customer
            return new_customer_id
        else:
            raise Exception("KYC validation failed")

    def create_account(self, customer_id, account_type, currency, initial_deposit=0, user_role=None):
        if not self._access_control.check_permission(user_role, "create_account"):
            raise PermissionError("User does not have permission to create accounts.")
        if customer_id not in self._customers:
            raise Exception("Customer not found")
        new_account_id = f"ACC{random.randint(1000, 9999)}"
        new_account = Account(account_id=new_account_id, customer_id=customer_id, 
                             account_type=account_type, currency=currency, balance=initial_deposit)
        self._accounts[new_account_id] = new_account
        self._customers[customer_id].accounts.append(new_account_id)
        return new_account_id

    def process_deposit(self, account_id, amount, currency, source, transaction_data, user_role=None):
        if not self._access_control.check_permission(user_role, "process_deposit"):
            raise PermissionError("User does not have permission to process deposits.")
        account = self._accounts.get(account_id)
        if not account:
            raise Exception("Account not found")
        if account.currency != currency:
            raise Exception("Currency mismatch")
        account.balance += amount
        transaction_id = f"TRANS{random.randint(1000, 9999)}"
        transaction = Transaction(transaction_id=transaction_id, account_id=account_id, amount=amount, 
                                  currency=currency, transaction_type="deposit")
        self._transactions.append(transaction)
        return transaction

    # Placeholder methods for withdrawals, transfers, and other operations.

    def encrypt_sensitive_data(self, data):
        # Placeholder for real encryption logic
        return "encrypted_data"

    def decrypt_sensitive_data(self, encrypted_data, user_role=None):
        if not self._access_control.check_permission(user_role, "decrypt_data"):
            raise PermissionError("User does not have permission to decrypt data.")
        # Placeholder for real decryption logic
        return "decrypted_data"

    # Additional methods according to the design requirements.
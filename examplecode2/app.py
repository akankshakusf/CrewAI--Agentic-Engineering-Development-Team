
import gradio as gr
from banking_core import EnterpriseBankingSystem

bank_system = EnterpriseBankingSystem()

def create_account(name, customer_id, currency):
    return bank_system.create_account({'name': name, 'id': customer_id}, currency)

def get_account_details(account_id):
    return bank_system.get_account_details(account_id)

def perform_deposit(account_id, amount):
    success = bank_system.deposit(account_id, amount)
    return 'Deposit Successful' if success else 'Deposit Failed'

def perform_withdrawal(account_id, amount):
    success = bank_system.withdraw(account_id, amount)
    return 'Withdrawal Successful' if success else 'Withdrawal Failed'

def perform_transfer(from_account_id, to_account_id, amount):
    success = bank_system.transfer(from_account_id, to_account_id, amount)
    return 'Transfer Successful' if success else 'Transfer Failed'

demo = gr.Interface(
    fn=create_account,
    inputs=["text", "text", "text"],
    outputs="json",
    title="Create Account",
    description="Create a new bank account with KYC validation and multi-currency support."
)

account_detail_demo = gr.Interface(
    fn=get_account_details,
    inputs="text",
    outputs="json",
    title="Account Details",
    description="Retrieve the details of an existing bank account."
)

deposit_demo = gr.Interface(
    fn=perform_deposit,
    inputs=["text", "number"],
    outputs="text",
    title="Deposit",
    description="Deposit funds into an existing account."
)

withdraw_demo = gr.Interface(
    fn=perform_withdrawal,
    inputs=["text", "number"],
    outputs="text",
    title="Withdrawal",
    description="Withdraw funds from an existing account."
)

transfer_demo = gr.Interface(
    fn=perform_transfer,
    inputs=["text", "text", "number"],
    outputs="text",
    title="Transfer",
    description="Transfer funds between two accounts."
)

gr.TabbedInterface(
    [demo, account_detail_demo, deposit_demo, withdraw_demo, transfer_demo],
    ["Create Account", "Account Details", "Deposit", "Withdrawal", "Transfer"]
).launch()

import gradio as gr
import json
from banking_core import EnterpriseBankingSystem, Customer, Account, Transaction, CreditCard, Loan

def register_customer_interface(first_name, last_name, dob, address, contact_info, id_documents):
    try:
        id_documents = json.loads(id_documents)
        customer_data = {
            "first_name": first_name,
            "last_name": last_name,
            "dob": dob,
            "address": address,
            "contact_info": contact_info,
            "id_documents": id_documents
        }
        user_role = "bank_staff"  # Simplified for one user demo
        customer_id = bank_system.register_customer(customer_data, user_role)
        return f"Customer registered successfully with ID: {customer_id}"
    except Exception as e:
        return str(e)

def create_account_interface(customer_id, account_type, currency, initial_deposit):
    try:
        user_role = "bank_staff"  # Simplified for one user demo
        account_id = bank_system.create_account(customer_id, account_type, currency, initial_deposit, user_role)
        return f"Account created successfully with ID: {account_id} with deposit of: {initial_deposit}"
    except Exception as e:
        return str(e)

def process_deposit_interface(account_id, amount, currency):
    try:
        user_role = "bank_staff"  # Simplified for one user demo
        source = "ATM"  # Simplified source
        transaction_data = ""  # Placeholder for additional transaction data
        transaction = bank_system.process_deposit(account_id, amount, currency, source, transaction_data, user_role)
        return f"Deposit successful. Transaction ID: {transaction.transaction_id}"
    except Exception as e:
        return str(e)

# Initialize the banking system
bank_system = EnterpriseBankingSystem("Demo Bank", "DB001", "encryption_key")

# Grant permissions to the demo user role
bank_system._access_control.add_role(
    username="bank_staff",
    role="staff",
    permissions=["register_customer", "create_account", "process_deposit"]
)


# Setup Gradio interfaces
with gr.Blocks() as demo_app:
    gr.Markdown("# Banking System Prototype")

    with gr.Tab("Customer Registration"):
        first_name_input = gr.Textbox(label="First Name")
        last_name_input = gr.Textbox(label="Last Name")
        dob_input = gr.Textbox(label="Date of Birth")
        address_input = gr.Textbox(label="Address")
        contact_info_input = gr.Textbox(label="Contact Information")
        id_documents_input = gr.Textbox(label="ID Documents")

        register_output = gr.Textbox(label="Output")
        register_button = gr.Button("Register Customer")
        register_button.click(register_customer_interface, inputs=[first_name_input, last_name_input, dob_input, address_input, contact_info_input, id_documents_input], outputs=register_output)

    with gr.Tab("Create Account"):
        customer_id_input = gr.Textbox(label="Customer ID")
        account_type_input = gr.Dropdown(choices=["Savings", "Checking", "Investment"], label="Account Type")
        currency_input = gr.Textbox(label="Currency")
        initial_deposit_input = gr.Number(label="Initial Deposit")

        account_output = gr.Textbox(label="Output")
        create_account_button = gr.Button("Create Account")
        create_account_button.click(create_account_interface, inputs=[customer_id_input, account_type_input, currency_input, initial_deposit_input], outputs=account_output)

    with gr.Tab("Deposit"):
        account_id_input = gr.Textbox(label="Account ID")
        deposit_amount_input = gr.Number(label="Amount")
        deposit_currency_input = gr.Textbox(label="Currency")

        deposit_output = gr.Textbox(label="Output")
        deposit_button = gr.Button("Process Deposit")
        deposit_button.click(process_deposit_interface, inputs=[account_id_input, deposit_amount_input, deposit_currency_input], outputs=deposit_output)

demo_app.launch()
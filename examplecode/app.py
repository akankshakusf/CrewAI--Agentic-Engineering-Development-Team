import gradio as gr
from account import Account, get_share_price
import pandas as pd
import datetime

# Initialize a single account
account = Account("user123")

def create_account(user_id, initial_deposit):
    global account
    account = Account(user_id)
    success = account.deposit_funds(float(initial_deposit))
    if success:
        return f"Account created for {user_id} with initial deposit of ${initial_deposit:.2f}"
    else:
        return "Failed to create account. Initial deposit must be greater than 0."

def deposit(amount):
    amount = float(amount)
    success = account.deposit_funds(amount)
    if success:
        return f"Successfully deposited ${amount:.2f}. New balance: ${account.balance:.2f}"
    else:
        return "Deposit failed. Amount must be greater than 0."

def withdraw(amount):
    amount = float(amount)
    success = account.withdraw_funds(amount)
    if success:
        return f"Successfully withdrew ${amount:.2f}. New balance: ${account.balance:.2f}"
    else:
        return "Withdrawal failed. Amount must be greater than 0 and not exceed your balance."

def buy_shares(symbol, quantity):
    symbol = symbol.upper()
    try:
        quantity = int(quantity)
        current_price = get_share_price(symbol)
        
        if current_price == 0.0:
            return f"Invalid symbol '{symbol}'. Available symbols: AAPL, TSLA, GOOGL"
        
        success = account.buy_shares(symbol, quantity)
        if success:
            return f"Successfully bought {quantity} shares of {symbol} at ${current_price:.2f} each. Total cost: ${current_price * quantity:.2f}. New balance: ${account.balance:.2f}"
        else:
            return f"Purchase failed. Insufficient funds or invalid parameters. Current balance: ${account.balance:.2f}, Required: ${current_price * quantity:.2f}"
    except ValueError:
        return "Quantity must be an integer."

def sell_shares(symbol, quantity):
    symbol = symbol.upper()
    try:
        quantity = int(quantity)
        current_price = get_share_price(symbol)
        
        if current_price == 0.0:
            return f"Invalid symbol '{symbol}'. Available symbols: AAPL, TSLA, GOOGL"
        
        success = account.sell_shares(symbol, quantity)
        if success:
            return f"Successfully sold {quantity} shares of {symbol} at ${current_price:.2f} each. Total received: ${current_price * quantity:.2f}. New balance: ${account.balance:.2f}"
        else:
            return f"Sale failed. You don't own enough shares of {symbol} or invalid parameters."
    except ValueError:
        return "Quantity must be an integer."

def get_holdings():
    holdings = account.get_holdings()
    if not holdings:
        return "No holdings in portfolio."
    
    result = "Current Holdings:\n"
    total_value = 0
    
    for symbol, quantity in holdings.items():
        price = get_share_price(symbol)
        value = price * quantity
        total_value += value
        result += f"{symbol}: {quantity} shares at ${price:.2f} each = ${value:.2f}\n"
    
    result += f"\nTotal Holdings Value: ${total_value:.2f}"
    result += f"\nCash Balance: ${account.balance:.2f}"
    result += f"\nTotal Portfolio Value: ${account.calculate_portfolio_value():.2f}"
    
    return result

def get_profit_loss():
    profit_loss = account.calculate_profit_loss()
    portfolio_value = account.calculate_portfolio_value()
    
    result = f"Total Deposits: ${account.total_deposits:.2f}\n"
    result += f"Total Withdrawals: ${account.total_withdrawals:.2f}\n"
    result += f"Current Portfolio Value: ${portfolio_value:.2f}\n"
    
    if profit_loss >= 0:
        result += f"Total Profit: ${profit_loss:.2f}"
    else:
        result += f"Total Loss: ${-profit_loss:.2f}"
    
    return result

def get_transactions():
    transactions = account.get_transaction_history()
    if not transactions:
        return "No transactions recorded."
    
    # Convert to DataFrame for nicer display
    df = pd.DataFrame(transactions)
    
    # Format the dataframe
    formatted_rows = []
    
    for _, tx in df.iterrows():
        row = {
            "Time": tx['timestamp'].strftime("%Y-%m-%d %H:%M:%S"),
            "Type": tx['type'],
            "Details": ""
        }
        
        if tx['type'] == 'DEPOSIT':
            row["Details"] = f"Amount: ${tx['amount']:.2f}, Balance After: ${tx['balance_after']:.2f}"
        elif tx['type'] == 'WITHDRAWAL':
            row["Details"] = f"Amount: ${tx['amount']:.2f}, Balance After: ${tx['balance_after']:.2f}"
        elif tx['type'] in ['BUY', 'SELL']:
            row["Details"] = f"Symbol: {tx['symbol']}, Quantity: {tx['quantity']}, " \
                            f"Price: ${tx['price_per_share']:.2f}, " \
                            f"Total: ${tx['total_amount']:.2f}, " \
                            f"Balance After: ${tx['balance_after']:.2f}"
        
        formatted_rows.append(row)
    
    result_df = pd.DataFrame(formatted_rows)
    return result_df

def check_stock_price(symbol):
    symbol = symbol.upper()
    price = get_share_price(symbol)
    if price > 0:
        return f"Current price of {symbol}: ${price:.2f}"
    else:
        return f"Invalid symbol '{symbol}'. Available symbols: AAPL, TSLA, GOOGL"

with gr.Blocks(title="Trading Simulation Platform") as demo:
    gr.Markdown("# Trading Simulation Platform")
    
    with gr.Tab("Account Setup"):
        gr.Markdown("### Create Account")
        with gr.Row():
            user_id_input = gr.Textbox(label="User ID", value="user123")
            initial_deposit_input = gr.Number(label="Initial Deposit ($)", value=10000)
        create_btn = gr.Button("Create Account")
        create_output = gr.Textbox(label="Result")
        create_btn.click(create_account, inputs=[user_id_input, initial_deposit_input], outputs=create_output)
    
    with gr.Tab("Fund Management"):
        gr.Markdown("### Deposit & Withdraw Funds")
        with gr.Row():
            with gr.Column():
                deposit_amount = gr.Number(label="Deposit Amount ($)")
                deposit_btn = gr.Button("Deposit")
                deposit_output = gr.Textbox(label="Result")
            
            with gr.Column():
                withdraw_amount = gr.Number(label="Withdraw Amount ($)")
                withdraw_btn = gr.Button("Withdraw")
                withdraw_output = gr.Textbox(label="Result")
        
        deposit_btn.click(deposit, inputs=deposit_amount, outputs=deposit_output)
        withdraw_btn.click(withdraw, inputs=withdraw_amount, outputs=withdraw_output)
    
    with gr.Tab("Trading"):
        gr.Markdown("### Buy & Sell Shares")
        
        with gr.Row():
            stock_symbol = gr.Textbox(label="Stock Symbol (AAPL, TSLA, GOOGL)", value="AAPL")
            check_price_btn = gr.Button("Check Price")
        price_output = gr.Textbox(label="Current Price")
        check_price_btn.click(check_stock_price, inputs=stock_symbol, outputs=price_output)
        
        with gr.Row():
            with gr.Column():
                buy_symbol = gr.Textbox(label="Symbol to Buy", value="AAPL")
                buy_quantity = gr.Number(label="Quantity", value=10, precision=0)
                buy_btn = gr.Button("Buy Shares")
                buy_output = gr.Textbox(label="Result")
            
            with gr.Column():
                sell_symbol = gr.Textbox(label="Symbol to Sell", value="AAPL")
                sell_quantity = gr.Number(label="Quantity", value=5, precision=0)
                sell_btn = gr.Button("Sell Shares")
                sell_output = gr.Textbox(label="Result")
        
        buy_btn.click(buy_shares, inputs=[buy_symbol, buy_quantity], outputs=buy_output)
        sell_btn.click(sell_shares, inputs=[sell_symbol, sell_quantity], outputs=sell_output)
    
    with gr.Tab("Portfolio"):
        gr.Markdown("### Portfolio Status")
        with gr.Row():
            holdings_btn = gr.Button("View Holdings")
            profit_loss_btn = gr.Button("View Profit/Loss")
        
        portfolio_output = gr.Textbox(label="Portfolio Information", lines=10)
        
        holdings_btn.click(get_holdings, outputs=portfolio_output)
        profit_loss_btn.click(get_profit_loss, outputs=portfolio_output)
    
    with gr.Tab("Transaction History"):
        gr.Markdown("### Transaction History")
        transactions_btn = gr.Button("View All Transactions")
        transactions_output = gr.Dataframe(label="Transactions")
        
        transactions_btn.click(get_transactions, outputs=transactions_output)

if __name__ == "__main__":
    demo.launch()
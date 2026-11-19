
from bank_operations import (
    create_account,
    view_accounts,
    search_account,
    deposit_money,
    withdraw_money,
    check_balance,
    transaction_history
)

print("\n===== BANK MANAGEMENT TEST =====")

# 1. Create Account
result = create_account(
    "Rahul Kumar",
    "9876543210",
    "rahul@gmail.com",
    "Rewari",
    1000
)
print("\nCreate Account:", result)

# 2. View Accounts
accounts = view_accounts()
print("\nAll Accounts:", accounts)

# 3. Search Account
if accounts:
    account_no = accounts[-1]["account_no"]

    print("\nSearch Account:")
    print(search_account(account_no))

    # 4. Deposit
    print("\nDeposit:")
    print(deposit_money(account_no, 500))

    # 5. Withdraw
    print("\nWithdraw:")
    print(withdraw_money(account_no, 200))

    # 6. Check Balance
    print("\nBalance:")
    print(check_balance(account_no))

    # 7. Transaction History
    print("\nTransaction History:")
    print(transaction_history(account_no))

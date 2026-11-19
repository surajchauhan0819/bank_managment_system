from decimal import Decimal
from database import get_connection


def create_account(name, phone, email, address, balance):
    connection = get_connection()

    if connection is None:
        return "Database connection failed"

    cursor = connection.cursor()

    try:
        if not name.strip() or not phone.strip():
            return "Name and phone are required"

        if balance < 0:
            return "Initial balance cannot be negative"

        query = """
            INSERT INTO accounts
            (name, phone, email, address, balance)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(
            query, (name, phone, email, address, balance)
        )

        account_no = cursor.lastrowid

        connection.commit()

        return f"Account created! Account No: {account_no}"

    except Exception as e:
        connection.rollback()
        return f"Error: {e}"

    finally:
        cursor.close()
        connection.close()


def view_accounts():
    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM accounts")
        return cursor.fetchall()

    except Exception as e:
        print("Error:", e)
        return []

    finally:
        cursor.close()
        connection.close()


def search_account(account_no):
    connection = get_connection()

    if connection is None:
        return None

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM accounts WHERE account_no = %s",
            (account_no,)
        )

        return cursor.fetchone()

    except Exception as e:
        print("Error:", e)
        return None

    finally:
        cursor.close()
        connection.close()


def deposit_money(account_no, amount):
    if amount <= 0:
        return "Amount must be greater than zero"

    return update_balance(account_no, amount, "Deposit")


def withdraw_money(account_no, amount):
    if amount <= 0:
        return "Amount must be greater than zero"

    return update_balance(account_no, -amount, "Withdraw")


def update_balance(account_no, amount, transaction_type):
    connection = get_connection()

    if connection is None:
        return "Database connection failed"

    cursor = connection.cursor()

    try:
        amount = Decimal(str(amount))
        if amount == 0:
            return "Amount must be greater than zero"

        connection.start_transaction()

        cursor.execute(
            "SELECT balance FROM accounts WHERE account_no = %s FOR UPDATE",
            (account_no,)
        )

        result = cursor.fetchone()

        if result is None:
            connection.rollback()
            return "Account not found"

        current_balance = result[0]
        new_balance = current_balance + amount

        if amount == 0:
            connection.rollback()
            return "Insufficient balance"

        cursor.execute(
            "UPDATE accounts SET balance = %s WHERE account_no = %s",
            (new_balance, account_no)
        )

        cursor.execute(
            """
            INSERT INTO transactions
            (account_no, transaction_type, amount, balance_after)
            VALUES (%s, %s, %s, %s)
            """,
            (account_no, transaction_type, abs(amount), new_balance)
        )

        connection.commit()

        return f"{transaction_type} successful. Balance: {new_balance}"

    except Exception as e:
        connection.rollback()
        return f"Error: {e}"

    finally:
        cursor.close()
        connection.close()


def check_balance(account_no):
    account = search_account(account_no)

    if account is None:
        return "Account not found"

    return account["balance"]


def update_account(account_no, name, phone, email, address):
    connection = get_connection()

    if connection is None:
        return "Database connection failed"

    cursor = connection.cursor()

    try:
        query = """
            UPDATE accounts
            SET name=%s, phone=%s, email=%s, address=%s
            WHERE account_no=%s
        """

        cursor.execute(
            query, (name, phone, email, address, account_no)
        )

        connection.commit()

        if cursor.rowcount == 0:
            return "Account not found"

        return "Account updated successfully"

    except Exception as e:
        connection.rollback()
        return f"Error: {e}"

    finally:
        cursor.close()
        connection.close()


def delete_account(account_no):
    connection = get_connection()

    if connection is None:
        return "Database connection failed"

    cursor = connection.cursor()

    try:
        cursor.execute(
            "DELETE FROM accounts WHERE account_no=%s",
            (account_no,)
        )

        connection.commit()

        if cursor.rowcount == 0:
            return "Account not found"

        return "Account deleted successfully"

    except Exception as e:
        connection.rollback()
        return f"Error: {e}"

    finally:
        cursor.close()
        connection.close()


def transaction_history(account_no):
    connection = get_connection()

    if connection is None:
        return []

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT * FROM transactions
            WHERE account_no = %s
            ORDER BY transaction_date DESC
            """,
            (account_no,)
        )

        return cursor.fetchall()

    except Exception as e:
        print("Error:", e)
        return []

    finally:
        cursor.close()
        connection.close()

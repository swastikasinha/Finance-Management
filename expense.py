import mysql.connector
import streamlit as st

def create_connection():
    connection = mysql.connector.connect(
        host ="localhost",
        user = "root",
        password = "methmonk",
        database = "project",
        auth_plugin = 'mysql_native_password'
    )
    return connection

def create_expense_table():
    connection = create_connection()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS expenses (
        expenseID INT AUTO_INCREMENT PRIMARY KEY,
        userID INT,
        expenseCategory VARCHAR(255) NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (userID) REFERENCES users(id)
    )
    """

    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()

def insert_expense(user_id,category,amount):
    connection = create_connection()
    cursor = connection.cursor()

    query = "INSERT INTO expenses (userID, expenseCategory, amount) VALUES (%s, %s, %s)"
    cursor.execute(query,(user_id,category,amount))

    connection.commit()
    cursor.close()
    connection.close()
def check_budget_exceeded(user_id, category):
    connection = create_connection()
    cursor = connection.cursor()

    # Get the total expense for the specified category
    total_expense_query = "SELECT SUM(amount) FROM expenses WHERE userID = %s AND expenseCategory = %s"
    cursor.execute(total_expense_query, (user_id, category))
    total_expense = cursor.fetchone()[0] or 0  # If no expenses, default to 0

    # Get the budgeted amount for the specified category
    budget_query = "SELECT amount FROM budget WHERE user_id = %s AND category_name = %s"
    cursor.execute(budget_query, (user_id, category))
    budget_amount = cursor.fetchone()

    cursor.close()
    connection.close()

    if budget_amount is not None:
        budget_amount = budget_amount[0]
        if total_expense > budget_amount:
            return True, total_expense, budget_amount
    return False, total_expense, budget_amount

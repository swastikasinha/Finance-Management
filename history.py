import mysql.connector
import pandas as pd
import streamlit as st

def create_connection():
    connection = mysql.connector.connect(
        host ="localhost",
        user = "root",
        password = "swastika@2003",
        database = "project",
        auth_plugin = 'mysql_native_password'
    )
    return connection

def hist(user_id):
    connection = create_connection()
    cursor = connection.cursor()

    query = """
            SELECT 'Expense' AS transaction_type,expenseCategory as category_name,amount,created_at
            FROM expenses 
            WHERE userID = %s
            UNION ALL
            SELECT 'Income' AS transaction_type,incomeCategory as category_name,amount,created_at
            FROM income
            WHERE userID = %s
            ORDER BY created_at DESC
            """
    cursor.execute(query,(user_id,user_id))
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    if not result:
        st.warning("No transaction history found.")
    else:
        df_history = pd.DataFrame(result, columns=['Transaction Type', 'Category', 'Amount', 'Transaction Date'])
        st.dataframe(df_history)
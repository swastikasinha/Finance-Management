import datetime
import mysql.connector
import pandas as pd

def create_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="methmonk",
        database="project",
        auth_plugin = 'mysql_native_password'
    )
    return connection

def get_expenses_by_month(user_id, month, year):
    connection = create_connection()
    cursor = connection.cursor()

    start_date = datetime.datetime(year, month, 1)
    end_date = datetime.datetime(year, month + 1, 1) - datetime.timedelta(days=1)

    query = "SELECT expenseCategory, amount FROM expenses WHERE userID = %s AND created_at BETWEEN %s AND %s"

    cursor.execute(query, (user_id, start_date, end_date))
    expenses_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return expenses_data

def get_income_by_month(user_id,month,year):
    connection = create_connection()
    cursor = connection.cursor()

    start_date = datetime.datetime(year, month, 1)
    end_date = datetime.datetime(year, month + 1, 1) - datetime.timedelta(days=1)

    query = "SELECT incomeCategory, amount FROM income WHERE userID = %s AND created_at BETWEEN %s AND %s"

    cursor.execute(query, (user_id, start_date, end_date))
    expenses_data = cursor.fetchall()

    cursor.close()
    connection.close()

    return expenses_data
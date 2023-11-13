import mysql.connector
import streamlit as st

def create_connection():
    connection = mysql.connector.connect(
        host ="localhost",
        user = "root",
        password = "methmonk",
        database = "project"
    )
    return connection

def create_income_table():
    connection = create_connection()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS income (
        incomeID INT AUTO_INCREMENT PRIMARY KEY,
        userID INT,
        incomeCategory VARCHAR(255) NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (userID) REFERENCES users(id)
    )
    """

    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()

def insert_income(user_id,category,amount):
    connection = create_connection()
    cursor = connection.cursor()

    query = "INSERT INTO income (userID, incomeCategory, amount) VALUES (%s, %s, %s)"
    cursor.execute(query,(user_id,category,amount))

    connection.commit()
    cursor.close()
    connection.close()

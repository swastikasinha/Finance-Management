import mysql.connector
import streamlit as st
import bcrypt

def create_connection():
    connection = mysql.connector.connect(
        host ="localhost",
        user = "root",
        password = "methmonk",
        database = "project",
        auth_plugin = 'mysql_native_password'
    )
    return connection

def create_user_table():
    connection = create_connection()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        username VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        age INT NOT NULL,
        profession VARCHAR(255),
        income INT,
        mobile VARCHAR(15),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """

    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()

def if_user_exists(username,email):
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT * FROM USERS WHERE UserName= %s OR email= %s"
    cursor.execute(query,(username,email))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return result is not None

def insert_user(name, email, username, password, age, profession, income, mobile):
    connection = create_connection()
    cursor = connection.cursor()

    query = "INSERT INTO users (name, email, username, password, age, profession, income, mobile) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (name, email, username, password, age, profession, income, mobile))

    connection.commit()

    cursor.close()
    connection.close()

def authenticate_user(username,password):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT id,password FROM users WHERE username = %s"
    cursor.execute(query, (username,))

    user_data = cursor.fetchone()

    cursor.close()
    connection.close()

    if user_data:
        stored_password = user_data[1].encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return user_data[0],user_data
    return None
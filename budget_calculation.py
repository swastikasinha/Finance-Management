import streamlit as st 
import mysql.connector
import calendar as cd
from functions import *

def create_connection():
    connection = mysql.connector.connect(
        host ="localhost",
        user = "root",
        password = "methmonk",
        database = "project",
        auth_plugin = 'mysql_native_password'
    )
    return connection

def create_budget_table():
    connection = create_connection()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS budget (
        budget_id INT AUTO_INCREMENT PRIMARY KEY,
        user_id int not null,
        month varchar(50),
        year int,
        category_name varchar(100),
        amount decimal(10,2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        foreign key(user_id) references users(id)
    )
    """

    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()

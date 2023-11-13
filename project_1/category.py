import mysql.connector
import streamlit as st
from functions import *

def create_connection():
    connection = mysql.connector.connect(
        host ="localhost",
        user = "root",
        password = "swastika@2003",
        database = "project",
        auth_plugin = 'mysql_native_password'
    )
    return connection

def create_category_table():
    connection = create_connection()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS category (
        categoryID INT AUTO_INCREMENT PRIMARY KEY,
        userID INT,
        category_name VARCHAR(255) NOT NULL unique,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (userID) REFERENCES users(id)
    )
    """

    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()

def default_categories_insertion():

    connection = create_connection()
    cursor = connection.cursor() 

    trigger_definition = """
    CREATE TRIGGER if not exists after_user_insert
    AFTER INSERT
    ON users FOR EACH ROW
    BEGIN
        INSERT ignore INTO category (userID, category_name) VALUES (NEW.id, 'Home');
        INSERT ignore INTO category (userID, category_name) VALUES (NEW.id, 'Education');
        INSERT ignore INTO category (userID, category_name) VALUES (NEW.id, 'Shopping');
        INSERT ignore INTO category (userID, category_name) VALUES (NEW.id, 'Others');
    END;
    """

    cursor.execute(trigger_definition)
    connection.commit()

    cursor.close()
    connection.close()



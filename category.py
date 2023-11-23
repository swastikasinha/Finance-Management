import mysql.connector
import streamlit as st
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

def create_category_table():
    connection = create_connection()
    cursor = connection.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS income_category (
        categoryID INT AUTO_INCREMENT,
        userID INT,
        category_name VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        primary key(categoryID, userID)
    )
    """

    cursor.execute(query)
    connection.commit()

    query = """
    CREATE TABLE IF NOT EXISTS expense_category (
        categoryID INT AUTO_INCREMENT,
        userID INT,
        category_name VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        primary key(categoryID, userID)
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
    after INSERT
    ON users FOR EACH ROW
    BEGIN
        INSERT INTO expense_category (userID, category_name) VALUES (new.ID, 'Home');
        INSERT INTO expense_category (userID, category_name) VALUES (new.id, 'Education');
        INSERT INTO expense_category (userID, category_name) VALUES (NEW.id, 'Shopping');
        INSERT INTO expense_category (userID, category_name) VALUES (NEW.id, 'Others');
        INSERT INTO income_category (userID, category_name) VALUES (NEW.id, 'Salary');
        INSERT INTO income_category (userID, category_name) VALUES (NEW.id, 'Rental');
        INSERT INTO income_category (userID, category_name) VALUES (NEW.id, 'Coupons');
        INSERT INTO income_category (userID, category_name) VALUES (NEW.id, 'Refunds');
    END;
    """

    cursor.execute(trigger_definition)
    connection.commit()

    cursor.close()
    connection.close()



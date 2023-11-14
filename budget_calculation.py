import streamlit as st 
import mysql.connector
import calendar as cd
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
        foreign key(user_id) references users(id),
        foreign key(category_name) references expense_category(category_name)
    )
    """

    cursor.execute(query)
    connection.commit()

    cursor.close()
    connection.close()


def set_budget():
    user_id = get_user_id()
    category_names = get_category_names("expense")

    connection = create_connection()
    cursor = connection.cursor()

    months = list(cd.month_name)[1:]
    years = list(range(2018, 2025))
    year = st.selectbox('Select a year:', years)
    month = st.selectbox('Select a month:', months)
    amount = st.number_input("Enter the budget : ", min_value = 0)
    category = st.selectbox("Select a category:", category_names, index=0)


    st.write("Your budget for ", month,", ",str(year),"=  Rs.",str(amount), "for category : ", category)   

    confirm_button = st.button("Confirm the budget")

    if confirm_button:
        select_query = "select * from budget where user_id = %s and year = %s and month = %s and category_name = %s"
        cursor.execute(select_query, (user_id, year, month,category))
        existing = cursor.fetchall()

        if existing:
            st.write("The same budget name exists for this month of the selected year. Would you like to update the budget amount for the same?")
            
        else:
            query = "INSERT INTO budget(user_id, year, month, category_name, amount) VALUES(%s,%s, %s,%s, %s)"
            cursor.execute(query, (user_id, year, month, category, amount))
            st.write("Confirmed!!")

    update = st.button("Update")

    if update:
        select_query = "select * from budget where user_id = %s and year = %s and month = %s and category_name = %s"
        cursor.execute(select_query, (user_id, year, month, category))
        existing = cursor.fetchall()

        if not existing:
            st.write("The budget doesn't exist!!")
        else:
            cursor.execute("Update budget set amount = %s where user_id = %s and year = %s and month = %s and category_name = category", (amount, user_id, year, month, category))
            st.write("The entered Budget is Updated!!")
        

    connection.commit()

    cursor.close()
    connection.close()

def budget():
    if "shared" not in st.session_state:
        st.write("Not Signed Up yet")
    else:
        set_budget()
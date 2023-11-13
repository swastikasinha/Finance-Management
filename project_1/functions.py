import mysql.connector
import streamlit as st
import bcrypt
from expense import *
from user_authentication import *
from income import *
from category import *
import pandas as pd

user_id = None

def sign_up():
    st.title("Sign Up")
    st.write("Have an account! Head to the sign in page!! 🙋‍♂️")
    with st.form("signup_form"):
        name = st.text_input("Full Name:")
        email = st.text_input("Email:")
        username = st.text_input('Username:')
        password = st.text_input('Password:', type='password')
        age = st.number_input('Age:', min_value=1, max_value=150)
        profession = st.text_input('Profession:')
        income = st.number_input('Income:', min_value=0)
        mobile = st.text_input("Mobile Number:")
    
        submit_button = st.form_submit_button("Sign Up")

    if submit_button:
        if not all([name,username,email,password,age,profession,income,mobile]):
            st.warning("Please fill all the required details.")
        elif if_user_exists(username,email):
            st.error("Username or email already exists. Please choose a different username or email.")
        else:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            insert_user(name,email,username,hashed_password,age,profession,income,mobile)
            st.success(f"Account created for {username}. You can now sign in")


def sign_in():
    global user_id
    st.title('Sign In')

    with st.form("signin_form"):
        username = st.text_input("Username:")
        password = st.text_input("Password", type='password')
        submit_button = st.form_submit_button('Sign In')
    st.write("Don't have an account? Head to the sign up page!! 🙋‍♂️")
    if submit_button:
        if not username or not password:
            st.warning("Please enter both username and password")
        else:
            user_data = authenticate_user(username,password)
            if user_data:
                st.success(f"Welcome, {username}")
                user_id = user_data[0]
                st.session_state["shared"] = True 
            else:
                st.error("Invalid credentials! Try Again")


def expense():
    st.title("Expense Management")

    with st.form("expense_form"):
        expense_category = st.text_input("Expense Category:")
        expense_amount = st.number_input("Expense Amount:",min_value=0.0)
        expense_submit_button = st.form_submit_button("Add Expense")

    if expense_submit_button:
        if not expense_category or expense_amount <=0:
            st.warning("Please enter all the details")
        else:
            insert_expense(user_id,expense_category,expense_amount)
            st.success("Expense added successfully")

def income():
    st.title("Income Management")

    with st.form("income_form"):
        income_category = st.text_input("Income Category:")
        income_amount = st.number_input("Income Amount:",min_value=0.0)
        income_submit_button = st.form_submit_button("Add Income")

    if income_submit_button:
        if not income_category or income_amount<=0:
            st.warning("Please enter all the details")
        else:
            insert_income(user_id,income_category,income_amount)
            st.success("Income added successfully")

def get_user_id():
    return user_id

def display_current_categories():
    connection = create_connection()
    cursor = connection.cursor() 

    display_query = "SELECT category_name FROM category where userID = %s"

    cursor.execute(display_query, (user_id,))

    result = cursor.fetchall()

    df_categories = pd.DataFrame(result, columns = ['Category'])
    st.dataframe(df_categories)

    cursor.close()
    connection.close()

def insert_categories(category_name):
    if not category_name.strip():
        st.warning("Please enter a non-empty category name.")
        return

    connection = create_connection()
    cursor = connection.cursor() 

    insert_query = """
    INSERT INTO category (userID, category_name) VALUES (%s, %s)
    """

    if category_name in get_category_names():
        st.error(f"Category '{category_name}' already exists for this user.")
    else: 
        cursor.execute(insert_query, (user_id, category_name))
        st.success(f"Category '{category_name}' added successfully.")
        
    connection.commit()
    cursor.close()
    connection.close()

def add_categories():
    new_category = st.text_input("Enter new category name : ", placeholder = "category name")
    add_category = st.button("Add new category", on_click = insert_categories(new_category))

def get_category_names():
    connection = create_connection()
    cursor = connection.cursor()

    query = "SELECT category_name FROM category WHERE userID = %s"
    cursor.execute(query, (user_id,))

    result = cursor.fetchall()

    category_names = [row[0] for row in result]

    cursor.close()
    connection.close()

    return category_names
import mysql.connector
import streamlit as st
import bcrypt


def create_connection():
    connection = mysql.connector.connect(
        host ="localhost",
        user = "root",
        password = "methmonk",
        database = "project"
    )
    return connection

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

def sign_up():
    st.title("Sign Up")

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

def authenticate_user(username,password):
    connection = create_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))

    user_data = cursor.fetchone()

    cursor.close()
    connection.close()

    if user_data:
        stored_password = user_data[3]
        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return user_data
    return None

def sign_in():
    st.title('Sign In')

    with st.form("signin_form"):
        username = st.text_input("Username:")
        password = st.text_input("Password", type='password')
        submit_button = st.form_submit_button('Sign In')

    if submit_button:
        if not username or not password:
            st.warning("Please enter both username and password")
        else:
            user_data = authenticate_user(username,password)
            if user_data:
                st.success(f"Welcome, {username}")
            else:
                st.error("Invalid credentials! Try Again")
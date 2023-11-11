import streamlit as st
import xml.etree.ElementTree as ET 
import mysql.connector 
import pandas as pd

conn = mysql.connector.connect(user='root',  
                               password='swastika@2003',  
                               host='localhost',  
                               database='Project',
                               auth_plugin = 'mysql_native_password')

c = conn.cursor() 

if 'page' not in st.session_state:
    st.session_state.page = 'SignUp'

result = False

def check(name, email, password) :

    query = "select * from user where UserName = %s and email = %s and password = %s"

    c.execute(query, (name, email, password))

    user = c.fetchone()

    if user :
        st.write("Signed up!")
        return True
    else :
        st.write("Wrong User details! Please fill correctly!")
        return False
    
    conn.commit()

def check_validity(name, email, password, age, profession, income, mobile) :

    query = "select * from user where UserName = %s and email = %s and Password = %s"

    c.execute(query, (name, email, password))

    user = c.fetchone()

    if name and email and password and age and profession and income and mobile :
        return True
    else :
        return False
    
    conn.commit()

st.markdown(
    """
    <div>
        <h1 style = "font-size: 40px; margin-bottom: 10px; color: #52B2BF; display: flex; justify-content: center;">Sign Up</h1>
    </div>
    """,
    unsafe_allow_html=True
)

name = st.text_input("Name : ")

email = st.text_input("email ID : ")

password = st.text_input("password : ")

signup_button = st.button('Sign Up')

if signup_button:
    result = check(name, email, password)


st.markdown(
        """
        <div>
            <h1 style = "font-size: 20px; margin-bottom: 20px; color: #82EEFD; display: flex; justify-content: center;">Don't have an account? Sign In now!! 🙋‍♂️ </h1>
        </div>
        """,
        unsafe_allow_html=True
)

# signin_button_placeholder = st.empty()

# signin_button = signin_button_placeholder.button("Sign In", key = "Sign In")


# signin_button = st.form_submit_button("Sign In")

# option = st.selectbox(
#   'Select an option : ',
#     ('Sign In', 'None'),
#     index=None,
#     placeholder = "-- options --",
# )


# signin_button_placeholder.empty()
st.markdown(
    """
    <div>
        <h1 style = "font-size: 40px; margin-bottom: 10px; color: #52B2BF; display: flex; justify-content: center;">Sign In</h1>
    </div>
    """,
    unsafe_allow_html=True
)

name = st.text_input("Name : ", key = 1)

email = st.text_input("email ID : ", key = 2)

Password = st.text_input("password : ", key = 3)

Age = st.text_input("Age : ", key = 4)

Profession = st.text_input("Profession : ", key = 5)

Income = st.text_input("Income (per annum) : ", key = 6)

mobile = st.text_input("Mobile no. : ", key = 7)

check_result = check_validity(name, email, Password, Age, Profession, Income, mobile)

confirm_signin_button = st.button("Sign In", key = "Sign In confirm")

if check_result and confirm_signin_button:
    query = "INSERT INTO User(UserName, email, Password, Age, Profession, Income, mobile_no) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    c.execute(query, (name, email, Password, Age, Profession, Income, mobile))
    conn.commit()
    st.write("Congratulations you are now signed in to the Finance Management App!!")
    st.write("Please sign up now to avail all the facilities!!")

elif not check_result and confirm_signin_button:
    st.write("Wrong User details! Please enter correctly!!")

# else :
#     st.write("Enter the complete details!!")


if st.session_state.page=="SignUp" and result==True:
    st.session_state["shared"] = True 

c.close()

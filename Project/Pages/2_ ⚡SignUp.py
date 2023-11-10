import streamlit as st
import xml.etree.ElementTree as ET 
import mysql.connector 
import pandas as pd

conn = mysql.connector.connect(user='root',  
                               password='swastika@2003',  
                               host='localhost',  
                               database='signup',
                               auth_plugin = 'mysql_native_password')

if 'page' not in st.session_state:
    st.session_state.page = 'SignUp'

placeholder = st.empty()

result = False

st.markdown(
    """
    <div>
        <h1 style = "font-size: 40px; margin-bottom: 60px; color: #3c00a0; display: flex; justify-content: center;">Sign Up</h1>
    </div>
    """,
    unsafe_allow_html=True
)

def check(name, email, password) :
    c = conn.cursor()

    query = "select * from user where name = %s and email = %s and password = %s"

    c.execute(query, (name, email, password))

    user = c.fetchone()

    if user :
        st.write("Signed up!")
        return True
    else :
        st.write("Wrong User details! Please fill correctly!")
        return False
    
    conn.commit()
    
    c.close()

name = st.text_input("Name : ")

email = st.text_input("email ID : ")

password = st.text_input("password : ")

signup_button = st.button('Sign Up')

if signup_button:
    result = check(name, email, password)

if st.session_state.page=="SignUp" and result==True:
    st.session_state["shared"] = True



import streamlit as st
import calendar as cd
import mysql.connector 
import time

conn = mysql.connector.connect(user='root',  
                               password='swastika@2003',  
                               host='localhost',  
                               database='Project',
                               auth_plugin = 'mysql_native_password')

c = conn.cursor() 

# if "shared" not in st.session_state:
#     st.write("Not Signed Up yet")

# elif st.session_state["shared"]==False:
#     st.write("Signed Out")

# else :


# def confirm(name, year, month, budget):

#     select_query = "select * from budget where name = %s and year = %s and month = %s and budget = %s"
#     c.execute(select_query, (name, year, month, budget,))
#     existing = c.fetchone()

#     if existing and confirm_button:
#         st.write("The same budget amount and name exists for this month of the selected year. Would you like to update the budget amount for the same?")
#         update = st.toggle("Update")
#         if update:
#             c.execute("Update budget set budget = %s where name = %s and year = %s and month = %s", (budget, name, year, month))
#             st.write("The entered Budget is Updated!!")
#     else:
#         query = "INSERT INTO budget(name, year, month, budget) VALUES(%s, %s, %s, %s)"
#         c.execute(query, (name, year, month, budget))
#         st.write("Confirmed!!")

#     conn.commit()

months = list(cd.month_name)[1:]
years = list(range(2018, 2025))

# Use the selectbox widget to allow the user to choose a month

selected_year = st.selectbox('Select a year:', years)
year = selected_year

selected_month = st.selectbox('Select a month:', months)
month = selected_month

budget = st.number_input("Enter the budget : ", min_value = 0)

# Display the selected month
st.write("Your budget for ", selected_month,", ",str(selected_year),"=  Rs.",str(budget))   

name = st.text_input("\n\nPlease confirm your set budget by entering a budget name :",key = "budget_name")

confirm_button = st.button("Confirm the budget")

if confirm_button:
    select_query = "select * from budget where name = %s and year = %s and month = %s"
    c.execute(select_query, (name, year, month))
    existing = c.fetchall()

    if existing:
        st.write("The same budget name exists for this month of the selected year. Would you like to update the budget amount for the same?")
        
    else:
        query = "INSERT INTO budget(name, year, month, budget) VALUES(%s, %s, %s, %s)"
        c.execute(query, (name, year, month, budget))
        st.write("Confirmed!!")

update = st.button("Update")

if update:
    select_query = "select * from budget where name = %s and year = %s and month = %s"
    c.execute(select_query, (name, year, month))
    existing = c.fetchall()

    if not existing:
        st.write("The budget doesn't exist!!")
    else:
        c.execute("Update budget set budget = %s where name = %s and year = %s and month = %s", (budget, name, year, month))
        st.write("The entered Budget is Updated!!")
    

conn.commit()

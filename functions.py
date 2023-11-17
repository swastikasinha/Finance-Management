from expense import *
from user_authentication import *
from income import *
from analysis import *
import altair as alt
from category import *
from history import *
import pandas as pd
import streamlit as st
from budget_calculation import *
from datetime import datetime
import matplotlib.pyplot as plt

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

def set_sign_out():
    st.session_state["shared"] = False

def sign_out():
    if "shared" not in st.session_state:
        st.write("Not Signed In yet")


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
    signout_button = st.button("Sign Out", key = "Sign Out")
    if signout_button:
            set_sign_out()
            st.write("Please sign In again to continue using the app!!")

def expense():
    st.title("Expense Management")
    category_names = get_category_names("expense")

    with st.form("expense_form"):
        expense_category = st.selectbox("Select a category:", category_names, index=0)
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
    category_names = get_category_names("income")

    with st.form("income_form"):
        income_category = st.selectbox("Select a category:", category_names, index=0)
        income_amount = st.number_input("Income Amount:",min_value=0.0)
        income_submit_button = st.form_submit_button("Add Income")

    if income_submit_button:
        if not income_category or income_amount<=0:
            st.warning("Please enter all the details")
        else:
            insert_income(user_id,income_category,income_amount)
            st.success("Income added successfully")

def analysis():
    st.title("Expense Analysis")

    with st.form("expense_analysis"):
        expense_month = st.number_input("Expense Month:", min_value=1, max_value=12)
        expense_year = st.number_input("Expense Year", min_value=2000)
        expense_analysis_submit = st.form_submit_button("Generate Expense Pie Chart")

    if expense_analysis_submit and expense_month >= 1 and expense_year >= 2000:
        expense_data = get_expenses_by_month(user_id, expense_month, expense_year)

        if not expense_data:
            st.warning("No expenses found for the specified expense month and year.")
        else:
            df_expenses = pd.DataFrame(expense_data, columns=['Category', 'Amount'])
            grouped_data = df_expenses.groupby('Category')['Amount'].sum()

            fig, ax = plt.subplots()
            wedges, texts, autotexts = ax.pie(grouped_data, labels=None, autopct='%1.1f%%', startangle=90,
                                              wedgeprops=dict(width=0.4))
            ax.legend(wedges, grouped_data.index, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            for text, autotext in zip(texts, autotexts):
                text.set_size(8)
                autotext.set_size(6)

            ax.axis('equal')
            st.pyplot(fig)

    elif expense_analysis_submit:
        st.warning("Please enter valid expense month and year values.")

    st.title("Income Analysis")

    with st.form("income_analysis"):
        income_month = st.number_input("Income Month:", min_value=1, max_value=12)
        income_year = st.number_input("Income Year", min_value=2000)
        income_analysis_submit = st.form_submit_button("Generate Income Pie Chart")

    if income_analysis_submit and income_month >= 1 and income_year >= 2000:
        income_data = get_income_by_month(user_id, income_month, income_year)

        if not income_data:
            st.warning("No income found for the specified income month and year.")
        else:
            df_income = pd.DataFrame(income_data, columns=['Category', 'Amount'])
            grouped_data = df_income.groupby('Category')['Amount'].sum()

            fig, ax = plt.subplots()
            wedges, texts, autotexts = ax.pie(grouped_data, labels=None, autopct='%1.1f%%', startangle=90,
                                              wedgeprops=dict(width=0.4))
            ax.legend(wedges, grouped_data.index, title="Categories", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
            for text, autotext in zip(texts, autotexts):
                text.set_size(8)
                autotext.set_size(6)

            ax.axis('equal')
            st.pyplot(fig)

    elif income_analysis_submit:
        st.warning("Please enter valid income month and year values.")

def display_current_categories():
    connection = create_connection()
    cursor = connection.cursor()

    try:
        display_query = """
                SELECT ec.category_name,
                    SUM(IFNULL(e.amount, 0)) AS total_expense_amount
                FROM expense_category ec
                LEFT JOIN expenses e ON ec.userID = e.userID
                    AND ec.category_name = e.expenseCategory
                    AND MONTH(ec.created_at) = MONTH(NOW())  
                    AND YEAR(ec.created_at) = YEAR(NOW())    
                WHERE ec.userID = %s
                GROUP BY ec.category_name;
        """
        cursor.execute(display_query, (user_id,))
        result_expense = cursor.fetchall()

        display_query_budget = """
            SELECT ec.category_name,
                IFNULL(b.amount, 'NA') AS budget_amount
            FROM expense_category ec  
            LEFT JOIN budget b ON ec.userID = b.user_id
                AND ec.category_name = b.category_name
                AND b.month = %s
                AND b.year = YEAR(NOW())
            WHERE ec.userID = %s
        """

        # Format the current month
        current_month = datetime.now().strftime('%B')

        cursor.execute(display_query_budget, (current_month, user_id))
        result_budget = cursor.fetchall()

        df_expense = pd.DataFrame(result_expense, columns=['Category', 'Total Spent this month'])
        df_budget = pd.DataFrame(result_budget, columns=['Category', 'Total budget set for this month'])
        df_categories = pd.merge(df_expense, df_budget, on='Category', how='outer')
        st.dataframe(df_categories)

        display_query_income = """
            CREATE PROCEDURE IF NOT EXISTS GetIncomeForCurrentUser(IN userID_param INT)
            BEGIN
                SELECT ic.category_name,
                    SUM(IFNULL(i.amount, 0)) AS total_income_amount
                FROM income_category ic
                LEFT JOIN income i ON ic.userID = i.userID
                    AND ic.category_name = i.incomeCategory
                    AND MONTH(ic.created_at) = MONTH(NOW())  
                    AND YEAR(ic.created_at) = YEAR(NOW())    
                WHERE ic.userID = userID_param
                GROUP BY ic.category_name;
            END;
        """

        cursor.execute(display_query_income, multi = True)
        cursor.callproc('GetIncomeForCurrentUser', (user_id,))

        for result in cursor.stored_results():
            result_income = result.fetchall()

        df_income = pd.DataFrame(result_income, columns=['Category', 'Income for the current month'])
        st.dataframe(df_income)

    finally:
        cursor.close()
        connection.close()

def insert_categories(category_name, type):
    if not category_name.strip():
        st.warning("Please enter a non-empty category name.")
        return

    if not type.strip():
        st.warning("Please enter a non-empty type of the category.")
        return

    connection = create_connection()
    cursor = connection.cursor() 

    if type=="income":
        insert_query = """
        INSERT INTO income_category (userID, category_name) VALUES (%s, %s)
        """
    else:
        insert_query = """
        INSERT INTO expense_category (userID, category_name) VALUES (%s, %s)
        """

    if category_name in get_category_names(type):
        st.error(f"Category '{category_name}' already exists for this user.")
    else: 
        cursor.execute(insert_query, (user_id, category_name))
        st.success(f"Category '{category_name}' added successfully.")
        
    connection.commit()
    cursor.close()
    connection.close()

def add_categories():
    new_category = st.text_input("Enter new category name : ", placeholder = "category name")
    type_category = st.text_input("Enter type of the catgory (income/expense) :")
    add_category = st.button("Add new category")
    if add_category:
        insert_categories(new_category, type_category)

def get_category_names(type):
    connection = create_connection()
    cursor = connection.cursor()

    if type=="income":
        query = "SELECT category_name FROM income_category WHERE userID = %s"
        cursor.execute(query, (user_id,))
    elif type=="expense":
        query = "SELECT category_name FROM expense_category WHERE userID = %s"
        cursor.execute(query, (user_id,))

    result = cursor.fetchall()

    category_names = [row[0] for row in result]

    cursor.close()
    connection.close()

    return category_names

def set_budget():
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
            cursor.execute("Update budget set amount = %s where user_id = %s and year = %s and month = %s and category_name = %s", (amount, user_id, year, month, category))
            st.write("The entered Budget is Updated!!")
        

    connection.commit()

    cursor.close()
    connection.close()

def history():
    hist(user_id)



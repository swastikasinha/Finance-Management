from expense import *
from user_authentication import *
from income import *
from analysis import *
import altair as alt

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

def analysis():
    st.title("Expense Analysis")

    expense_month = st.number_input("Expense Month:", min_value=1, max_value=12)
    expense_year = st.number_input("Expense Year", min_value=2000)
    expense_analysis_submit = st.button("Generate Expense Pie Chart")

    st.title("Income Analysis")

    income_month = st.number_input("Income Month:", min_value=1, max_value=12)
    income_year = st.number_input("Income Year", min_value=2000)
    income_analysis_submit = st.button("Generate Income Pie Chart")

    if expense_analysis_submit and expense_month >= 1 and expense_year >= 2000:
        expense_data = get_expenses_by_month(user_id, expense_month, expense_year)

        if not expense_data:
            st.warning("No expenses found for the specified expense month and year.")
        else:
            df_expenses = pd.DataFrame(expense_data, columns=['Category', 'Amount'])
            chart = alt.Chart(df_expenses).mark_arc().encode(
                alt.Color('Category:N'),
                alt.Text('Amount:Q', format='.2f')
            ).properties(width=400, height=400)
            st.altair_chart(chart)

    if income_analysis_submit and income_month >= 1 and income_year >= 2000:
        income_data = get_income_by_month(user_id, income_month, income_year)

        if not income_data:
            st.warning("No income found for the specified income month and year.")
        else:
            df_income = pd.DataFrame(income_data, columns=['Category', 'Amount'])
            chart = alt.Chart(df_income).mark_arc().encode(
                alt.Color('Category:N'),
                alt.Text('Amount:Q', format='.2f')
            ).properties(width=400, height=400)
            st.altair_chart(chart)

    if (expense_analysis_submit and (expense_month < 1 or expense_year < 2000)) or \
            (income_analysis_submit and (income_month < 1 or income_year < 2000)):
        st.warning("Please enter valid expense or income month and year values.")

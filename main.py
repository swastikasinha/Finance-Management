from functions import *
from budget_calculation import *
from category import *

create_user_table()
create_expense_table()
create_income_table()
create_category_table()
default_categories_insertion()
create_budget_table()

menu = ['Home', 'Sign Up','Sign In','Budget', 'Expense','Income','Category','Analysis','History']


tab = st.tabs(menu)

with tab[0]:
    st.title("# Welcome to Finance Management App! 👋")
    st.markdown(
        """
        <div>
            <div>
                <h2>Keep track of your expenses!!</h1>
                <h2>All in one app!!<h2>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with tab[1]:
    sign_up()

with tab[2]:
    sign_in()

with tab[3]:
    budget()

with tab[4]:
    expense()

with tab[5]:
    income()

with tab[6]:
    display_current_categories()
    add_categories()

with tab[7]:
    analysis()

with tab[8]:
    history()
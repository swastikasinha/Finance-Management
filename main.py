from functions import *
from budget_calculation import *
from category import *

create_user_table()
create_expense_table()
create_income_table()
create_category_table()
default_categories_insertion()
create_budget_table()

menu = ['Home', 'Sign Up','Sign In','Budget', 'Expense','Income','Category','Analysis', 'History','Savings']

tab = st.tabs(menu)

with tab[0]:
    st.title("Welcome to Finance Management App! 👋")
    st.markdown(
        """
        <div>
            <ul>
                <li>Keep track of your expenses with this all-in-one app!</li>
                <li>Sign up and sign in to start managing your finances.</li>
                <li>Set your monthly budget and track your expenses and income.</li>
                <li>Analyze your spending with visual charts and graphs.</li>
                <li>View your transaction history and manage categories.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

with tab[1]:
    sign_up()

with tab[2]:
    sign_in()

with tab[3]:
    if "shared" not in st.session_state:
        st.write("Not Signed In yet")
    elif st.session_state["shared"]==False:
        st.write("Signed Out")
    else:
        set_budget()

with tab[4]:
    if "shared" not in st.session_state:
        st.write("Not Signed In yet")
    elif st.session_state["shared"]==False:
        st.write("Signed Out")
    else:
        expense()

with tab[5]:
    if "shared" not in st.session_state:
        st.write("Not Signed In yet")
    elif st.session_state["shared"]==False:
        st.write("Signed Out")
    else:
        income()

with tab[6]:
    if "shared" not in st.session_state:
        st.write("Not Signed In yet")
    elif st.session_state["shared"]==False:
        st.write("Signed Out")
    else:
        display_current_categories()
        add_categories()

with tab[7]:
    if "shared" not in st.session_state:
        st.write("Not Signed In yet")
    elif st.session_state["shared"]==False:
        st.write("Signed Out")
    else:
        analysis()

with tab[8]:
    if "shared" not in st.session_state:
        st.write("Not Signed In yet")
    elif st.session_state["shared"]==False:
        st.write("Signed Out")
    else:
        history()

with tab[9]:
    if "shared" not in st.session_state:
        st.write("Not Signed In yet")
    elif st.session_state["shared"]==False:
        st.write("Signed Out")
    else:
        show_saving()
from functions import *

create_user_table()
create_expense_table()

menu = ['Home', 'Sign Up','Sign In','Expense']


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
    expense()
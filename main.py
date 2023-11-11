from user_authentication import *

create_user_table()

menu = ['Home', 'Sign Up','Sign In']


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

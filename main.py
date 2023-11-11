from functions import *

create_user_table()

menu = ['Sign In','Sign Up']
choice = st.sidebar.selectbox('Sign Up',menu)

if choice=='Sign In':
    sign_in()
    st.write("Don't have an account? Head to the sign up page!! 🙋‍♂️")
if choice=='Sign Up':
    sign_up()
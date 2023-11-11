from functions import *

menu = ['Sign In','Sign Up']
choice = st.sidebar.selectbox('Sign Up',menu)

if choice=='Sign In':
    sign_in()
    if st.button("Don't have an account? Sign In now!! 🙋‍♂️"):
        choice='Sign Up'
if choice=='Sign Up':
    sign_up()
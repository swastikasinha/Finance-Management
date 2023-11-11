import streamlit as st 

if "shared" not in st.session_state:
    st.write("Not Signed Up yet")

else:
    signout_button = st.button("Sign Out", key = "Sign Out")

    if signout_button:
        st.session_state["shared"] = False
        st.write("Please sign up again to continue using the app!!")


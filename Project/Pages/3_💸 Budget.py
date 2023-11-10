import streamlit as st 

if "shared" not in st.session_state:
    st.write("Not Signed Up yet")

else :
    st.write("Welcome")
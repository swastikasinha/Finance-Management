import streamlit as st 

if "shared" not in st.session_state:
    st.write("Not Signed Up yet")

elif st.session_state["shared"]==False:
    st.write("Signed Out")

else :
    st.write("Welcome!")
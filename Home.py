import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Streamlit! 👋")

st.markdown(
    """
    <div>
        <div>
            <h1>Sign Up</h1>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.success("Select a demo above.")

 
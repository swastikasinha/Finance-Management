import streamlit as st

st.set_page_config(
    page_title="Ex-stream-ly Cool App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
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

 
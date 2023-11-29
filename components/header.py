import streamlit as st
from streamlit_extras.switch_page_button import switch_page

def header(current_page):
    header = st.header("")
    with header:
        col1, col2, col3 = st.columns((1.5, 3, 1))
        with col1:
            st.image('static/Invenics Logo White.png', width=200)
        if current_page == "Login":
            return

        if 'user' not in st.session_state or st.session_state.user is None:
            with col2:
                st.write("Guest")
            with col3:
                if st.button ("LOGIN"):
                    st.session_state.current_page = current_page
                    switch_page('login')
        else:
            with col2:
                st.write("Logged in as: " + st.session_state.user)
            with col3:
                if st.button ("LOGOUT"):
                    st.session_state.user = None
                    st.experimental_rerun()
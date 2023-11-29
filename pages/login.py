import streamlit as st
import time
import xml.etree.ElementTree as ET
from PIL import Image
import os
import complexity_calc as cc
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages
from components.header import header as headerComponent

# Setting Page Configuration
icon = Image.open('invenics_logo.png')
st.set_page_config(
    initial_sidebar_state="collapsed",
    page_title="Migration Platform",
    page_icon=icon,
    layout="wide"
)
show_pages([
    Page('_1_-_Home.py'),
    Page('pages/_2_-_Complexity_Report.py'),
    Page('pages/_3_-_Conversion_Results.py'),
    Page('pages/login.py')
])
hide_pages([
    '1 - Home',
    '2 - Complexity Report',
    '3 - Conversion Results',
    'Login'
])

with open('style/style.css') as f:
    with open('style/stylelogin.css') as f2:
        st.markdown(f'<style>{f.read()}{f2.read()}</style>', unsafe_allow_html=True)

def main():
    # Header
    headerComponent('Login')

    col1, col2, col3 = st.columns((1, 3, 1))
    with col2:
        with st.form(key='login_form'):
            st.markdown("""<h3 style='text-align: center; background-color:#ffffff; color:#000000;background: none;'>
                    Login</h3>""", unsafe_allow_html=True)
            username = st.text_input(label='Username')
            password = st.text_input(label='Password', type='password')
            col1, col2, col3 = st.columns((1, 1, 1))
            with col2:
                submit_button = st.form_submit_button(label='LOGIN')
            if submit_button:
                if username != '' and password != '':
                    st.session_state.user = username
                    switch_page('1 - Home' if ('current_page' not in st.session_state or st.session_state.current_page == None) else st.session_state.current_page)
                else:
                    st.error('Please enter a username and password')

if __name__ == "__main__":
    main()
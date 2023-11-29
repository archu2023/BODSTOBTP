import streamlit as st

def title(str):
    st.markdown("""<h1 style='text-align: center; font-size: 36px; padding: 0; background-color:#ffffff; color:#000000;background: none;'>
            SAP BODS to SAP DI Migration Platform</h1>""", unsafe_allow_html=True)
    st.markdown("""<h5 style='text-align: center; font-size: 16px; padding-top: 5px; color: #5A5A5A;font-weight:500;background: none'>
                Speed up your migration process from SAP BODS to SAP Data Intelligence.<br>
                Convert your SAP BODS XML Files into JSON Files for SAP Data Intelligence.</h5>""", unsafe_allow_html=True)


    st.markdown(f"""<h2 style='text-align: center; font-size: 32px; color: #2A2A2A; font-weight:500,background: none'>{str}</h2>""", unsafe_allow_html=True)
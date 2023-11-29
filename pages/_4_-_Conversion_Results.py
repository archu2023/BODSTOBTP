import streamlit as st
import time
import xml.etree.ElementTree as ET
from PIL import Image
import os
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages
import pandas as pd
from components.header import header as headerComponent
from components.title import title as titleComponent



# import DS2DI_UC1_PARSE as parse1
# import DS2DI_UC0_PARSE as parse0
# pages
# import streamlit 


# Setting Page Configuration
icon = Image.open('invenics_logo.png')
st.set_page_config(
    initial_sidebar_state="auto",
    page_title="Migration Platform",
    page_icon=icon,
    layout="wide")
show_pages([
    Page('_1_-Home.py'),
    Page('pages/_2_-_Complexity_Report.py'),
    Page('pages/_3_-_Conversion_Results.py'),
    Page('pages/login.py')
])
hide_pages([
    'Login'
])

with open('style/style.css') as f:
    with open('style/style3.css') as f2:
        st.markdown(f'<style>{f.read()}{f2.read()}</style>', unsafe_allow_html=True)


def get_result():
    result = []
    row = ()
    for file in st.session_state.complexity:
        file_name = file['file_name'].split(".")[0]
        json_file = ""
        if "Success" in st.session_state.result[file_name]:
            json_file = file_name+".json"
        row = (file_name+".xml", st.session_state.complexity[0]['Complexity'], st.session_state.result[file_name], json_file)
        result.append(row)
        row = ()
    return result

def generate_table(df):

    html = """<div class="htmlTableContainer"><table style="width: 100%;">
                <thead>
                    <tr>
                        <th style="text-align: center; width:40%;">BODS File Name</th>
                        <th style="text-align: center; width:10%;">Complexity</th>
                        <th style="text-align: center; width:10%;">Result</th>
                        <th style="text-align: center; width:40%;">DI File Name</th>
                    </tr>
                </thead>
                <tbody>"""
    for index, row in df.iterrows(): # do not remove index
        complexity_color = "#EC7B34"
        if row['Complexity'] == "Low":
            complexity_color = "#33B469"
        elif row['Complexity'] == "Medium":
            complexity_color = "#EBBC2E"
        result_color = "#33B469;"
        di_img = """<img style="height: 24px;" src="https://media.licdn.com/dms/image/C5612AQF9txh_Bp5L4w/article-cover_image-shrink_720_1280/0/1592076102280?e=2147483647&v=beta&t=dzKpuY9lXoskM1k9TGGG4XszbghJFvUsy_oj7JILJSo">"""
        if row['DI File Name'] == "":
            result_color = "#ED3A3A;"
            di_img = """"""
        html += f"""<tr>
                        <td style="text-align: left; word-break: break-all;">
                            <span>
                                <img style="width: 52px;" src="https://www.aespatech.com/wp-content/uploads/2018/01/r-sap-bods-900x288.png">
                                {row['File Name']}
                            </span>
                        </td>
                        <td style="text-align: center; color: {complexity_color};">{row['Complexity']}</td>
                        <td style="text-align: center; color: {result_color};">{row['Result']}</td>
                        <td style="text-align: left; word-break: break-all;">{di_img}{row['DI File Name']}</td>
                    </tr>
                    """
    html += """</tbody></table></div>"""
    return html

def main():


    headerComponent("3 - Conversion Results")
    titleComponent("Conversion Results")

    cols = ['File Name', 'Complexity', 'Result', 'DI File Name']
    df1 = pd.DataFrame(get_result(), columns=cols)

    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown(generate_table(df1), unsafe_allow_html=True)

    st.markdown(f"""<p style='text-align: center; background-color:#ffffff; font-weight:bold; font-size:20px; background: none;'>
        Successfully created files have been downloaded in the '{st.session_state.destination_path}' path.</p>""", unsafe_allow_html=True)
    
    view_files_button = st.button('VIEW FILES')
    if view_files_button:
        # opens file explorer
        os.startfile(st.session_state.destination_path)

                        


if __name__ == "__main__":
    if 'files' not in st.session_state:
        switch_page('1 - Home')
    main()
import streamlit as st
import pandas as pd
import time
import xml.etree.ElementTree as ET
from PIL import Image
import os
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
from driver import main_prog1
from components.header import header as headerComponent
from components.title import title as titleComponent

# Setting Page Configuration

icon = Image.open('invenics_logo.png')
st.set_page_config(
    initial_sidebar_state="auto",
    page_title="Migration Platform",
    page_icon=icon,
    layout="wide")
show_pages([
    Page('Home.py'),
    Page('pages\\_2_-_Complexity_Report.py'),
    Page('pages\\_3_-_Conversion_Results.py'),
    Page('pages\\login.py')
])
hide_pages([
    '3 - Conversion Results',
    'Login'
])

#CSS
with open('style/style.css') as f:
    with open('style/style2.css') as f2:
        st.markdown(f'<style>{f.read()}{f2.read()}</style>', unsafe_allow_html=True)


complexity_df = pd.DataFrame({
    "File Name": [],
    "Complexity": []
})

test_df = pd.DataFrame({
    "File Name": ["file1", "file2", "file3", "file4", "file5", "file6", "file7", "file8"],
    "Complexity": ["Low", "Medium", "High", "Low", "Medium", "High", "Low", "Medium"]
})

def generate_complexity_df():
    for key in st.session_state.complexity:
        complexity_df.loc[len(complexity_df.index)] = [key, st.session_state.complexity[key]]
    st.session_state.complexity_df = complexity_df

def generate_table(df):
    html = """<div class="htmlTableContainer"><table style="width: 100%;">
                <thead>
                    <tr>
                        <th style="text-align: left; width:85%;  word-break: break-all;">File Name</th>
                        <th style="text-align: center; width:15%;">Complexity</th>
                    </tr>
                </thead>
                <tbody style="background-color: #FFFFFF;">"""
    for index, row in df.iterrows():
        text_color = "#EC7B34"
        if row['Complexity'] == "Low":
            text_color = "#33B469"
        elif row['Complexity'] == "Medium":
            text_color = "#EBBC2E"
        html += f"""<tr>
                        <td style="text-align: left;">{row['File Name']}</td>
                        <td style="text-align: center; color:{text_color};">{row['Complexity']}</td>
                    </tr>
                    """
    html += """</tbody></table></div>"""
    return html

def download_complexity_report(df):
    csv = df.to_csv(index=False)
    st.download_button(
        label="DOWNLOAD REPORT",
        data=csv,
        file_name='complexity_report.csv',
        mime='text/csv',
    )

def convert(files:list, path)->list:
    result = {}
    percent_complete = 0
    progress_bar = st.progress(int(percent_complete))
    for file in files:
        progress_text = f"Converting {file.get().name}..."
        progress_bar.progress(int(percent_complete), text=progress_text)
        file_name = file.get().name.split(".")[0]
        file_content = file.getContent()
        try:    
            result[f"{file_name}"] = main_prog1(file_content, path, file_name)
        except Exception as e:
            print(e)
            result[f"{file_name}"] = "Failed"
        percent_complete += 100/len(files)
    print(result)
    st.session_state.result = result

    progress_bar.progress(100, text="Conversion complete.")
    time.sleep(1)

def main():

    headerComponent("2 - Complexity Report")
    titleComponent("Complexity Report")

    if ('complexity_df' not in st.session_state or st.session_state.complexity_df is None):
        generate_complexity_df()
    complexity_df = st.session_state.complexity_df


    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        st.markdown(generate_table(complexity_df), unsafe_allow_html=True)

    download_complexity_report(complexity_df)

    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        destination_path = st.text_input(placeholder="Enter the destination for your files", label = ' ', label_visibility = "collapsed")
    
    if destination_path != "":
        if os.path.exists(destination_path):
            convert_pressed = st.button("CONVERT", key="convert")
            col1, col2, col3 = st.columns([1, 4, 1])
            if convert_pressed:
                with col2:
                    st.session_state.destination_path = destination_path
                    convert(st.session_state.files, destination_path)
                    show_pages([
                        Page('pages\\_4_-_Conversion_Results.py')
                    ])
                    switch_page('4 - Conversion Results')
        else:
            col1, col2, col3 = st.columns([1, 4, 1])
            with col2:
                st.error(f"'{destination_path}' doesn't exist. Please enter a valid path.")

if __name__ == "__main__":
    if 'files' not in st.session_state:
        switch_page('1 - Home')
    main()

import streamlit as st

import time

from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages

from driver import main_prog1
from components.header import header as headerComponent

import pandas as pd

import base64


# icon = Image.open('invenics_logo.png')
st.set_page_config(
    initial_sidebar_state="auto", page_title="Migration Platform", layout="wide"
)
show_pages(
    [
        Page("_1_-_Home.py"),
        Page("pages/_2_-_Complexity_source.py"),
        Page("pages/_3_-_Summary.py"),
        Page("pages/_4_-_Conversion_Results.py"),
        Page("pages/login.py"),
    ]
)
hide_pages(["3 - Conversion Results", "Login"])
with open("style/style.css") as f:
    with open("style/style2.css") as f2:
        with open("style/complexity_styling.css") as f3:
            st.markdown(
                f"<style>{f.read()}{f2.read()}{f3.read()}</style>",
                unsafe_allow_html=True,
            )


def generate_boxs(tot, val, inval):
    html_for_the_box = (
        """
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Information Boxes</title>
        <style>
            .infoContainer {
                display: flex;
                justify-content: space-around;
            }
            .infoBox {
                border: 1px solid #ddd;
                padding: 20px;
                width: 30%;
                text-align: center;
                margin: 10px;
            }
        </style>
    </head>
    <body>
    <div class="infoContainer">
        <div id="firstbox" class="infoBox" >
            <h2>"""
        + str(tot)
        + """</h2>
            <img src="./app/static/files.png" alt="Image"style="float:right"><br>
            <h6>Total Data Services</h6>
        </div>
        <div id="middlebox" class="infoBox" >
            <h2>"""
        + str(val)
        + """</h2>
            <img src="./app/static/passed.png" alt="Image"style="float:right"><br>
            <h6>Valid Data Services</h6>
        </div>
        <div id="lastbox" class="infoBox" >
            <h2>"""
        + str(inval)
        + """</h2>
            <img src="./app/static/failed.png" alt="Image"style="float:right">
            <h6>Invalid Data Services</h6>
        </div>
    </body>"""
    )
    return html_for_the_box


def generate_table(df):
    if len(df.index) != 0:
        html_for_the_table = """<head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="styles.css">
            <title>Your Table</title>
        </head>
        <body>
        <div class="htmlTableContainer">
        <colgroup>
            <col style="max-width: 100px;">
            <col style="max-width: 200px;">
        </colgroup>
            <table width="100%">
                <thead>
                    <tr>
                        <th>Sl.No</th>
                        <th>File Name</th>
                        <th>Job Name</th>
                        <th>Operators Count</th>
                        <th>Job Count</th>
                        <th>Inbuilt Functions Count</th>
                        <th>Custom Function Count</th>
                        <th>Workflow</th>
                        <th>Datastores</th>
                        <th>SQL Functions Count</th>
                        <th>Code Quality %</th>
                        <th>Complexity</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style>"""
        sl_no = 0
        for row in df.to_dict("records"):
            sl_no += 1
            text_color = "#EC7B34"
            if row["Complexity"] == "Low":
                text_color = "#33B469"
            elif row["Complexity"] == "Medium":
                text_color = "#EBBC2E"
            html_for_the_table += f"""<tr>
                            <td style="text-align: center;">{sl_no}</td>
                            <td style="text-align: center;">{row['file_name']}</td>
                            <td style="text-align: center;">{row['Job_name']}</td>
                            <td style="text-align: center;">{row['Operators_Count']}</td>
                            <td style="text-align: center;">{row['Job_Count']}</td>
                            <td style="text-align: center;">{row['Inbuilt_Functions']}</td>
                            <td style="text-align: center;">{row['Custom_Functions']}</td>
                            <td style="text-align: center;">{row['workflow']}</td>
                            <td style="text-align: center;">{row['datastore']}</td>
                            <td style="text-align: center;">{row['Sqlfunction_count']}</td>
                            <td style="text-align: center;">{row['Score']}</td>
                            <td style="text-align: center;"><b>{row['Complexity']}</b></td>
                        </tr>"""

        html_for_the_table += """</tbody></table></div></body>"""

    else:
        html_for_the_table = st.write("No Valid Xmls")
    return html_for_the_table


def generate_complexity_df():
    st.session_state.complexity_df = pd.DataFrame(st.session_state.complexity)
    st.session_state.xml_counts = st.session_state.xml_c
    st.session_state.summary = pd.DataFrame(st.session_state.summary_D)

def download_complexity_report(df):
    csv = df.to_csv(index=False)
    st.download_button(
        label="DOWNLOAD REPORT",
        data=csv,
        file_name="complexity_report.csv",
        mime="text/csv",
    )


def create_download_link(
    df, filename="exported_report.csv", text="Export Report    ", font_size="18px"
):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # Encode the CSV data as base64
    href = (
    f'<div style="display: inline-flex; align-items: center;margin-bottom: -27px;">'
    f'<a href="data:file/csv;base64,{b64}" download="{filename}" style="font-size: {font_size};">{text}</a>'
    f'<img src="./app/static/export_icon.png" style="margin-left: 5px; width: {font_size}; height: {font_size};">'
    "</div>"
)


    return href


def convert(files: list, path) -> list:
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
            # print(e)
            result[f"{file_name}"] = "Failed"
        percent_complete += 100 / len(files)
    # print(result)
    st.session_state.result = result

    progress_bar.progress(100, text="Conversion complete.")
    time.sleep(1)


def main():
    headerComponent("2 - Complexity source")
    st.markdown(
        """<h3 style='text-align: center; font-family: 'Poppins', sans-serif;font-size: 36px; padding: 0; background-color:#ffffff; color:#000000;background: none;'>Data Services to Data Intelligence Migration Platform</h3>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """<h4 style='text-align: center; font-size: 20px; padding-top: 2px; color: #000000;background: none'>
                    Data Services Diagnosis Report</h4>""",
        unsafe_allow_html=True,
    )

    if (
        "complexity_df" not in st.session_state
        or st.session_state.complexity_df is None
    ):
        generate_complexity_df()
    total, valid, invalid = st.session_state.xml_counts
    complexity_df = st.session_state.complexity_df
    col1, col2, col3 = st.columns([1, 12, 1])
    with col2:
        st.markdown(generate_boxs(total, valid, invalid), unsafe_allow_html=True)
        link_html = f"""
    <div style="display: flex; justify-content: flex-end; margin-top: 10px;">
        {create_download_link(complexity_df)}
    </div></br>
"""
        st.markdown(link_html, unsafe_allow_html=True)

        # st.markdown(generate_table(complexity_df), unsafe_allow_html=True)
        st.markdown(generate_table(complexity_df), unsafe_allow_html=True)
    # col1, col2, col3 = st.columns([1, 4, 1])
    # with col2:
    #     destination_path = st.text_input(
    #         placeholder="Enter the destination for your files",
    #         label=" ",
    #         label_visibility="collapsed",
    #     )
    #
    #     if destination_path != "":
    #         if os.path.exists(destination_path):
    #             convert_pressed = st.button("CONVERT", key="convert")
    #             # col1, col2, col3 = st.columns([1, 4, 1])
    #             if convert_pressed:
    #                 st.session_state.destination_path = destination_path
    #                 convert(st.session_state.files, destination_path)
    #                 show_pages([Page("pages\\_3_-_Conversion_Results.py")])
    #                 switch_page("3 - Conversion Results")
    #         else:
    #             st.error(
    #                 f"'{destination_path}' doesn't exist. Please enter a valid path."
    #             )
        col1, col2, col3 = st.columns([1, 4, 1])
        with col2:
            next_pressed = st.button("NEXT")
            if next_pressed:
                show_pages([Page("pages/_3_-_Summary.py")])
                switch_page("3 - Summary")
if __name__ == "__main__":
    if "files" not in st.session_state:
        switch_page("1 - Home")
    main()

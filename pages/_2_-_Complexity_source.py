import streamlit as st
import streamlit.components.v1 as components
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
        # Page("pages\\_3_-_Summary.py"),
        # Page("pages\\_4_-_Conversion_Results.py"),
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

# sample_data = [
#     {
#         "sl.no": "1",
#         "File Name": "DS2DI_UC0_READFILE.xml",
#         "Datastores": "DB_TMV",
#         "Operators": "Query,Table_comparison,History_preservation,Key_generation,Date_generation",
#         "SQL Functions": "NIL",
#         "Inbuilt Functions": "NIL",
#         "Workflow": "New_WorkFlow155"
#     },
#     {
#         "sl.no": "2",
#         "File Name": "DS2DI_UC02_LOOKUP.xml",
#         "Datastores": "DB_TMV",
#         "Operators": "Query",
#         "SQL Functions": "NIL",
#         "Inbuilt Functions": "NIL",
#         "Workflow": "New_WorkFlow156"
#     },
#     {
#         "sl.no": "3",
#         "File Name": "DS2DI_UC07_SP_INNER_JOIN_STOCK.xml",
#         "Datastores": "DB_TMV",
#         "Operators": "Query,Table_comparison,Date_generation",
#         "SQL Functions": "NIL",
#         "Inbuilt Functions": "NIL",
#         "Workflow": "New_WorkFlow155"
#     },
#     {
#         "sl.no": "4",
#         "File Name": "DS2DI_UC21_DATA_TRANSFORM.xml",
#         "Datastores": "NIL",
#         "Operators": "NIL",
#         "SQL Functions": "NIL",
#         "Inbuilt Functions": "NIL",
#         "Workflow": "New_WorkFlow156"
#     }, {
#         "sl.no": "5",
#         "File Name": "DS2DI_UC22_EFFECTIVE_DATE.xml",
#         "Datastores": "DB_TMV",
#         "Operators": "Query,Table_comparison,Key_generation",
#         "SQL Functions": "NIL",
#         "Inbuilt Functions": "NIL",
#         "Workflow": "New_WorkFlow155"
#     },
#     {
#         "sl.no": "6",
#         "File Name": "DS2DI_UC23_HIERARCHY_FLATTENING.xml",
#         "Datastores": "DB_TMV",
#         "Operators": "Query",
#         "SQL Functions": "NIL",
#         "Inbuilt Functions": "NIL",
#         "Workflow": "NIL"
#     },
#     {
#         "sl.no": "7",
#         "File Name": "DS2DI_UC24_DATE_GENERATION.xml",
#         "Datastores": "DB_TMV",
#         "Operators": "Query,Date_generation",
#         "SQL Functions": "NIL",
#         "Inbuilt Functions": "NIL",
#         "Workflow": "New_WorkFlow155"
#     },
#     {
#         "sl.no": "8",
#         "File Name": "DS2DI_UC25_HISTORY_PRESERVATION.xml",
#         "Datastores": "DB_TMV",
#         "Operators": "Data_mask",
#         "SQL Functions": "NIL",
#         "Inbuilt Functions": "NIL",
#         "Workflow": "New_WorkFlow156"
#     },
#
# ]
# popup_df = pd.DataFrame(sample_data)
#
# js_dataframe = popup_df.to_json(orient='split')


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
            <h6>Total Data Service Objects</h6>
        </div>
        <div id="middlebox" class="infoBox" >
            <h2>"""
            + str(val)
            + """</h2>
            <img src="./app/static/passed.png" alt="Image"style="float:right"><br>
            <h6>Valid Data Service Objects</h6>
        </div>
        <div id="lastbox" class="infoBox" >
            <h2>"""
            + str(inval)
            + """</h2>
            <img src="./app/static/failed.png" alt="Image"style="float:right">
            <h6>Invalid Data Service Objects</h6>
        </div>
    </body>"""
    )
    return html_for_the_box


def generate_table(df,pop):
    if len(df.index) != 0:
        html_for_the_table = """<!DOCTYPE html>
        <html lang="en">
        <head>
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
                        <th>Custom Functions Count</th>
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
            html_for_the_table += f"""<tr onclick="openPopup(this)">
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

        html_for_the_table += """</tbody></table></div>"""
        html_for_the_table += f"""
            <div class="overlay" id="overlay">
                <div class="popup">
                    <span class="close-btn" onclick="closePopup()">&times;</span>
                    <div id="popup-content"></div>
                </div>
            </div>
        <style>
        @import url('https://fonts.googleapis.com/css?family=Poppins');
        @import url('https://fonts.googleapis.com/css?family=Inter');
        h4{{
          text-align: center !important;
          font-family: 'Poppins', sans-serif 
        }}
        li{{
            font-family: 'Poppins', sans-serif 
        }}
        td{{
            font-family: 'Poppins', sans-serif 
        }}
        .htmlTableContainer {{
            /* table-layout: fixed; */
            overflow-y: scroll;
            /* position: relative; */
            max-height: 70vh;
            border: solid 1px rgba(49, 51, 63, 0.2);
            /* border-radius: 5px; */
            overflow: auto;
            margin-bottom: 20px;
        }}
        .st-emotion-cache-1629p8f{{
            padding: 0%;
        }}
        .htmlTableContainer table {{
            padding-top: 20px;
            width: 100%;
            border-collapse: collapse;
            /* height: 200px; */
        }}
        .htmlTableContainer th {{
            background-color: #161F27;
            padding: 5px !important;
            text-align: center;
            border: 1px solid #686C71;
            font-weight: normal;
            font-family: 'Poppins', sans-serif;
        }}
        .htmlTableContainer td {{
            padding: 10px;
            text-align: center;
            border: 1px solid #ddd;
        }}
        .htmlTableContainer tbody tr:nth-child(odd) {{
            background-color: #C8E6C9 ;
        }}
        .htmlTableContainer thead tr {{
            background-color: #EEF8EE;
            color: white;
            font-size: medium;
        }}
        .overlay {{
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 75%;
            background-color: #80808000;
            align-items: center;
            justify-content: center;
        }}
        .popup {{
            font-family: 'Poppins', sans-serif 
            margin-top: -0%;
            background: #fff;
            border-radius: 5px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
            text-align: left;
            max-width: 600px;
            width: 80%;
            padding-left: 0px;
            padding-right: 20px;
            position: relative;
            word-wrap: break-word;
        }}
        .close-btn {{
            cursor: pointer;
            position: absolute;
            top: 10px;
            right: 10px;
            font-size: 20px;
            color: #333;
        }}
        </style>
        <script>
        function openPopup(row) {{
            sample_data = {pop}
            console.log(sample_data)
            var rowData = Array.from(row.cells).map(cell => cell.textContent);
            var slNo = rowData[0];
            var matchedData = sample_data.find(data => data['sl.no'] == slNo);
            if (matchedData) {{
                // Create popup title with File Name
                var popupTitle = `<h4>${{matchedData["File Name"]}}</h4>`;
                // Create popup content excluding the two rows
                var popupContent = "<ul>";
                Object.keys(matchedData).forEach((key) => {{
                    // Exclude rows with sl.no and File Name
                    if (key !== "sl.no" && key !== "File Name") {{
                        popupContent += `<li><b>${{key}}:</b> ${{matchedData[key]}}</li>`;
                    }}
                }});
                popupContent += "</ul>";
                // Set popup title and content
                document.getElementById('popup-content').innerHTML = popupTitle + popupContent;
                document.getElementById('overlay').style.display = 'flex';
            }}
        }}
        function closePopup() {{
            console.log("Closing popup");

            document.getElementById('overlay').style.display = 'none';
        }}
        </script>
        """
    else:
        html_for_the_table = st.write("No Valid Xmls")
    return html_for_the_table


def generate_complexity_df():
    st.session_state.complexity_df = pd.DataFrame(st.session_state.complexity)
    st.session_state.xml_counts = st.session_state.xml_c
    st.session_state.summary = pd.DataFrame(st.session_state.summary_D)
    st.session_state.popup = st.session_state.popup_D

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
    # st.markdown(
    #     """<h3 style='text-align: center; font-family: 'Poppins', sans-serif;font-size: 36px; padding: 0; background-color:#ffffff; color:#000000;background: none;'>Data Services to Data Intelligence Migration Platform</h3>""",
    #     unsafe_allow_html=True,
    # )
    st.markdown("""<h1 style='text-align: center; font-size: 36px; padding: 0; background-color:#ffffff; color:#000000;background: none;'>
                Data Services to Data Intelligence Migration Platform</h1>""", unsafe_allow_html=True)

    st.markdown(
        """<h3 style='text-align: center; font-size: 20px; padding-top: 2px; color: #000000;background: none'>
                    Data Services Diagnosis Report</h3>""",
        unsafe_allow_html=True,
    )

    if (
            "complexity_df" not in st.session_state
            or st.session_state.complexity_df is None
    ):
        generate_complexity_df()
    total, valid, invalid = st.session_state.xml_counts
    complexity_df = st.session_state.complexity_df
    popup = st.session_state.popup
    col1, col2, col3 = st.columns([1, 12, 1])
    with col2:
        st.markdown(generate_boxs(total, valid, invalid), unsafe_allow_html=True)
        if len(complexity_df.index) != 0:
            complexity_df_export = complexity_df[
                ['file_name', 'Job_name', 'Operators_Count', 'Job_Count', 'Inbuilt_Functions',
                 'Custom_Functions', 'workflow', 'datastore', 'Sqlfunction_count', 'Score', 'Complexity']]
            complexity_df_export.rename(columns={'file_name': 'File Name', 'Job_name': 'Job Name',
                                                 'Operators_Count': 'Operators Count',
                                                 'Job_Count': 'Job Count',
                                                 'Inbuilt_Functions': 'Inbuilt Functions Count',
                                                 'Custom_Functions': 'Custom Function Count',
                                                 'workflow': 'Workflow',
                                                 'datastore': 'Datastores', 'Sqlfunction_count': 'SQL Functions Count',
                                                 'Score': 'Code Quality %', 'Complexity': 'Complexity'}, inplace=True)

            complexity_df_export.insert(0, 'Sl.No', range(1, 1 + len(complexity_df_export)))
            link_html = f"""
        <div style="display: flex; justify-content: flex-end; margin-top: 10px;">
            {create_download_link(complexity_df_export)}
        </div></br>
    """
            st.markdown(link_html, unsafe_allow_html=True)

            # st.markdown(generate_table(complexity_df), unsafe_allow_html=True)
            components.html(generate_table(complexity_df,popup), height=450)
            col1, col2, col3 = st.columns([1, 4, 1])
            with col2:
                next_pressed = st.button("Next")
                if next_pressed:
                    show_pages([Page("pages/_3_-_Summary.py")])
                    switch_page("3 - Summary")
        else:
            # st.write("**No Valid Data Service Objects**")
            st.markdown("<h5 style='text-align: center; color: grey;'>No Valid Data Service Objects</h5>",
                        unsafe_allow_html=True)


if __name__ == "__main__":
    if "files" not in st.session_state:
        switch_page("1 - Home")
    main()

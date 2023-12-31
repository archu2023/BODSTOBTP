import streamlit as st
import time
import xml.etree.ElementTree as ET
from PIL import Image
import os
import complexity_calc as cc
from streamlit_extras.switch_page_button import switch_page
from st_pages import Page, show_pages, hide_pages
from components.header import header as headerComponent
from components.title import title as titleComponent


# Setting Page Configuration
icon = Image.open("invenics_logo.png")
st.set_page_config(
    initial_sidebar_state="auto",
    page_title="Migration Platform",
    page_icon=icon,
    layout="wide",
)
# show_pages([Page("_1_-_Home.py")])
show_pages(
    [
        Page("_1_-_Home.py"),
        Page("pages/_2_-_Complexity_source.py"),
        Page("pages/_3_-_Summary.py"),
        Page("pages/_4_-_Conversion_Results.py"),
        Page("pages/login.py"),
    ]
)
hide_pages(["2 - Complexity source","3 - Summary", "4 - Conversion Results", "Login"])


with open("style/style.css") as f:
    with open("style/style1.css") as f2:
        st.markdown(f"<style>{f.read()}{f2.read()}</style>", unsafe_allow_html=True)


class File:
    def __init__(self, object):
        self.object = object
        self.content = object.read()

    def get(self):
        return self.object

    def getContent(self):
        return self.content


def createFileList(files):
    file_list = []
    for file in files:
        file_list.append(File(file))
    return file_list


def calculateComplexity(files):
    complexity = []
    summary = []
    popup = []
    validxml = 0
    in_validxml = 0
    sl = 1
    for file in files:
        # inbuilt_function,sql_function,custom_function,project_flag,dataintegrator_flag,job_flag,source_complexity,score_naming = cc.calculate_complexity(file.getContent())
        # repo_ver, prd_ver, job,valid_bods,invalid_bods = cc.complexity_assessment_report(project_flag,dataintegrator_flag,job_flag)
        (
            inbuilt_function,
            sql_function,
            custom_function,
            project_flag,
            dataintegrator_flag,
            job_flag,
            source_complexity,
            score_naming,
            job_names,
            num_dist_operator,
            num_jobs,
            workflows,
            datastores,
            efforts,
            coverage,
            workflow_names,
            operator_names,
            inbuild_function_names
        ) = cc.calculate_complexity(file.getContent())
        (
            repo_ver,
            prd_ver,
            job,
            valid_bods,
            invalid_bods,
        ) = cc.complexity_assessment_report(project_flag, dataintegrator_flag, job_flag)
        # if invalid_bods == 1:
        #     repo_ver=prd_ver=job=inbuilt_function=sql_function=custom_function=source_complexity = 'Null'
        # complexity.append({'file_name':file.get().name,
        #                                'RepositoryVersion':repo_ver,
        #                                'ProductVersion':prd_ver,
        #                                'Job_name': job,
        #                                'Inbuilt Functions':inbuilt_function,
        #                                'SQL Functions':sql_function,
        #                                'Custom_Functions':custom_function,
        #                                'Valid XML' :valid_bods,
        #                                'Invalid XML':invalid_bods,
        #                                'Source Complexity':source_complexity,
        #                                'Score':score_naming})
        if valid_bods == 1:
            complexity.append(
                {
                    "file_name": file.get().name,
                    "Job_name": job_names,
                    "Operators_Count": num_dist_operator,
                    "Job_Count": num_jobs,
                    "Inbuilt_Functions": inbuilt_function,
                    "Custom_Functions": custom_function,
                    "workflow": workflows,
                    "datastore": datastores,
                    "Sqlfunction_count": sql_function,
                    "Score": score_naming,
                    "Complexity": source_complexity,
                }
            )
            summary.append({
                "file_name": file.get().name,
                "Job_name": job_names,
                "Complexity": source_complexity,
                "coverage" : coverage,
                "effort" : efforts
            })

            popup.append({
                "sl.no": sl,
                "File Name": file.get().name,
                "DataStores": datastores,
                "Operators": operator_names,
                "WorkFlows": workflow_names,
                "Inbuild Functions": inbuild_function_names
            })
            validxml += 1
            sl += 1
        else:
            in_validxml += 1

        # complexity[file.get().name]

        # complexity['RepositoryVersion'] = repo_ver
        # complexity['ProductVersion'] = prd_ver
        # complexity['Job_name'] = job
        # complexity['Inbuilt Functions'] = inbuilt_function
        # complexity['SQL Functions'] = sql_function
        # complexity['Custom Functions'] = custom_function
        xmls_couts = (validxml + in_validxml, validxml, in_validxml)
    return complexity, xmls_couts,summary,popup


def checkFileLimit(files):
    if files is None:
        return None
    ("files: " + len(files))
    if len(files) > 10:
        st.warning(
            "You are limited to process a maximum of 10 files at once. The initial 10 files will be processed by default."
        )
        return files[:10]
    else:
        return files


def main():
    headerComponent("1 - Home")
    titleComponent("Upload Files")

    # Uploader
    col1, col2, col3 = st.columns((1, 7, 1))
    uploaded_files = None
    with col2:
        uploaded_files = st.file_uploader(
            label=" ",
            label_visibility="collapsed",
            type=["xml"],
            accept_multiple_files=True,
        )
        if len(uploaded_files) > 10:
            st.warning(
                "You are limited to process a maximum of 10 files at once. The initial 10 files will be processed by default."
            )
            uploaded_files = uploaded_files[:10]

    if uploaded_files:
        col1, col2, col3 = st.columns((2, 1, 2))
        with col2:
            next_pressed = st.button("Next")
            if next_pressed:
                st.session_state.files = None
                st.session_state.complexity = None
                st.session_state.complexity_df = None
                st.session_state.xml_counts = None
                st.session_state.summary = None
                st.session_state.popup = None
                st.session_state.files = createFileList(uploaded_files)
                (
                    st.session_state.complexity,
                    st.session_state.xml_c,
                    st.session_state.summary_D,
                    st.session_state.popup_D
                ) = calculateComplexity(st.session_state.files)
                # st.session_state.xml_c = (10,5,5)
                show_pages([Page("pages/_2_-_Complexity_source.py")])
                switch_page("2 - Complexity source")


if __name__ == "__main__":
    main()

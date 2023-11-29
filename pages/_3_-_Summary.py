import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from st_pages import Page, show_pages, hide_pages
from components.header import header as headerComponent
from streamlit_extras.switch_page_button import switch_page
import pandas as pd
import base64



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
# with open("style/destination_complexity.css") as f3:
#     st.markdown(
#         f"<style>{f3.read()}</style>",
#         unsafe_allow_html=True,
#     )
hide_pages(["3 - Conversion Results", "Login"])
with open("style/style.css") as f:
    with open("style/style2.css") as f2:
        with open("style/destination_complexity.css") as f3:
            st.markdown(
                f"<style>{f.read()}{f2.read()}{f3.read()}</style>",
                unsafe_allow_html=True,
            )

# Create a DataFrame with valid and invalid columns
valid_invalid = pd.DataFrame({
    "validation": ["Valid Data Service Objects", "Invalid Data Service Objects"],
    "value": [
        "10",
        "8",
    ],
})

# pd_donut_chart = pd.DataFrame(data)
source = pd.DataFrame(
    {"Complexity": ["High", "Medium", "Low"], "Data Services": [3, 7, 4]}
)
target = pd.DataFrame(
    {"Indicative Effort": ["Completely Migratable", "Partially Migratable", "Needs to be redesigned"], "Data Services": [3, 7, 4]}
)

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
                        <th>No</th>
                        <th>File Name</th>
                        <th>Job Name</th>
                        <th>Source Complexity</th>
                        <th>Target Coverage</th>
                        <th>Indicative Effort</th>
                    </tr>
                </thead>"""
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
                    <td style="text-align: center;">{row['Complexity']}</td>
                    <td style="text-align: center;">{row['coverage']}</td>
                    <td style="text-align: center;">{row['effort']}</td>
                </tr>"""
    else:
        html_for_the_table = 'There is no Valid Data Services'
    return html_for_the_table
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

def main():
    headerComponent("2 - Complexity source")
    st.markdown(
        """<h1 style='text-align: center; font-size: 36px; padding: 0; background-color:#ffffff; color:#000000;background: none;'>Data Services to Data Intelligence Migration Platform</h1>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """<h3 style='text-align: center; padding-top: 5px; color: #000000;background: none'>Summary</h3>""",
        unsafe_allow_html=True,
    )
    summary = st.session_state.summary
    total_xmls,valid,in_valid = st.session_state.xml_counts
    # complexity_source = summary[['Complexity']]
    c_low = len(list(summary[summary['Complexity'] == 'Low'].values))
    c_medium = len(list(summary[summary['Complexity'] == 'Medium'].values))
    c_high = len(list(summary[summary['Complexity'] == 'High'].values))
    effort_low = len(list(summary[summary['effort'] == 'Small'].values))
    effort_med = len(list(summary[summary['effort'] == 'Medium'].values))
    effort_hig = len(list(summary[summary['effort'] == 'High'].values))

    source = pd.DataFrame(
        {"Complexity": ["High", "Medium", "Low"], "Data Services": [c_high, c_medium, c_low]}
    )

    target = pd.DataFrame(
        {"Indicative Effort": ["Completely Migratable", "Partially Migratable", "Needs to be redesigned"],
         "Data Services": [effort_low, effort_med, effort_hig]}
    )

    valid_invalid = pd.DataFrame({
        "validation": ["Valid Data Service Objects", "Invalid Data Service Objects"],
        "value": [
            valid,
            in_valid,
        ],
    })

    column1, column2, column3 = st.columns([1, 12, 1])
    with column2:
        st.subheader("Client Landscape", anchor=None)
        col1, col2, col3 = st.columns(3)
        st.subheader("Estimation", anchor=None)
        with col1:
            # data_canada = px.data.gapminder().query("country == 'Canada'")
            # fig = px.bar(data_canada, x='complexity', y='dataservices')
            fig = px.bar(
                source,
                x="Complexity",
                y="Data Services",
                title="Source",
                height=280,
                width=600,
                color="Complexity",
                color_discrete_map={
                    "High": "#002060",
                    "Medium": "#2E76B7",
                    "Low": "#00B5D9",
                },
            )
            layout = go.Layout(title='Transparent Chart Example', plot_bgcolor='rgba(255, 255, 255, 0.5)')

            fig.update_layout(showlegend=False, title_x=0.5,    plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)',)
            st.plotly_chart(fig, use_container_width=True, config= {'displayModeBar': False},)

        with col2:
            fig = px.pie(
                valid_invalid,
                # x='value',
                values="value", names="validation",
                height=280,
                width=600,
                hole=0.7,
                title="Validation",
                color_discrete_sequence=["#002060", "#2E76B7", "#00B5D9"],
            )
            fig.update_layout(
                legend=dict(
                    orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5
                ), title_x=0.43,plot_bgcolor='rgba(0, 0, 0, 0)',paper_bgcolor='rgba(0, 0, 0, 0)'
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False},paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',)
        with col3:
            fig = px.bar(
                target,
                x="Indicative Effort",
                y="Data Services",
                title="Target",
                height=280,
                width=600,
                color="Indicative Effort",
                color_discrete_map={
                    "Completely Migratable": "#002060",
                    "Partially Migratable": "#2E76B7",
                    "Needs to be redesigned": "#00B5D9",
                },
            )
            fig.update_layout(showlegend=False, title_x=0.5, plot_bgcolor='rgba(0, 0, 0, 0)',
    paper_bgcolor='rgba(0, 0, 0, 0)')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False},paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',)

        with column2:
            link_html = f"""
    <div style="display: flex; justify-content: flex-end; margin-top: 10px;">
        {create_download_link(valid_invalid)}
    </div></br>
"""
            st.markdown(link_html, unsafe_allow_html=True)
            st.markdown(generate_table(summary), unsafe_allow_html=True)
            # st.markdown(html_for_the_table, unsafe_allow_html=True)


if __name__ == "__main__":
    if "files" not in st.session_state:
        switch_page("1 - Home")
    main()
    # # with cols2:
    # labels = ['Valid Data Service Objects','Invalid Data Service Objects',]
    # values = [4500, 2500,]
    # fig2 = go.Figure(data=[go.Pie(values = values, hole=.7)],)
    # fig2.update_layout(
    # autosize=True,legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),)
    # st.plotly_chart(fig2, use_container_width=True)

    # # Add labels
    # fig.add_trace(go.Scatter(
    #     x=[None],
    #     y=[None],
    #     showlegend=False,
    #     textfont=dict(size=14, color="#002060"),
    # ))

    # fig.add_trace(go.Scatter(
    #     x=[None],
    #     y=[None],
    #     showlegend=False,
    #     textfont=dict(size=14, color="#2E76B7"),
    # ))

    # Update layout
    # fig.update_layout(
    #     autosize=True,
    #     legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5),
    # )

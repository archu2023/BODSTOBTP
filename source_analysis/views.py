from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import redirect, render
from Bods2btp.utils.driver import main_prog1
from Bods2btp.utils import complexity_calc as cc
# from ds2di.utils. import complexity_calc as cc
import json
import pandas as pd


context = ""
xml_file = ""
user_path = ""





def calculateComplexity(files):
    complexity = []
    summary = []
    popup = []
    validxml = 0
    in_validxml = 0
    sl = 1
    result = {}
    for file in files:
        xml_content = file.read().decode("utf-8")
        file_name = file
        try:    
            result[f"{file_name}"] = main_prog1(xml_content, user_path, file_name)
        except Exception as e:

            result[f"{file_name}"] = "Failed"
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
            inbuild_function_names,
        ) = cc.calculate_complexity(xml_content)
        (
            repo_ver,
            prd_ver,
            job,
            valid_bods,
            invalid_bods,
        ) = cc.complexity_assessment_report(project_flag, dataintegrator_flag, job_flag)
        if valid_bods == 1:
            complexity.append(
                {
                    "sl_no": sl,
                    "file_name": file.name,
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
            summary.append(
                {
                    "sl_no": sl,
                    "file_name": file.name,
                    "Job_name": job_names,
                    "Complexity": source_complexity,
                    "coverage": coverage,
                    "effort": efforts,
                }
            )

            popup.append(
                {
                    "sl_no": sl,
                    "File_Name": file.name,
                    "DataStores": datastores,
                    "Operators": operator_names,
                    "WorkFlows": workflow_names,
                    "Inbuild_Functions": inbuild_function_names,
                }
            )
            validxml += 1
            sl += 1
        else:
            in_validxml += 1
    xmls_couts = (validxml + in_validxml, validxml, in_validxml)
    return complexity, xmls_couts, summary, popup, result


def home(request):
    global context
    global xml_file
    if request.method == "POST":
        print('8*****************88')
        xml_file = request.FILES.getlist("featured_images")
        complexity, xmls_counts, summary, popup, result = calculateComplexity(xml_file)
        context = {
            "complexity": complexity,
            "xmls_counts": xmls_counts,
            "summary": summary,
            "popup": popup,
            "result": result,
        }
        total_objects = context['xmls_counts'][0]
        total_valid_objects = context['xmls_counts'][1]
        total_invalid_objects = context['xmls_counts'][2]
        print(context)
        # print(context['complexity'])
        return render(request, "complexity.html", {"data":context['complexity'], "total_objects":total_objects, "total_valid_objects":total_valid_objects,"total_invalid_objects":total_invalid_objects, "popup":popup})
    return render(request, "uploadUI.html")


def source(request):
    dummy_data = [
        {
            "sl_no": 1,
            "file_name": "file1.xml",
            "job_name": "JOB_INBUILT",
            "operators_count": 3,
            "job_count": 1,
            "inbuilt_functions_count": 3,
            "custom_function_count": 1,
            "workflow": "1",
            "datastores": "DB_TMV",
            "sql_functions_count": 0,
            "code_quality_percent": 33,
            "complexity": "Medium",
        }
        # Add more dictionaries for additional rows
    ]
    return render(request, "complexity.html", {"data": dummy_data})


def summary_fun(request):
    summary = context['summary']
    df = pd.DataFrame(summary)
    c_low = len(list(df[df['Complexity'] == 'Low'].values))
    c_medium = len(list((df[df['Complexity'] == 'Medium'].values)))
    c_high = len(list((df[df['Complexity'] == 'High'].values)))
    effort_low = len(list(df[df['effort'] == 'Small'].values))
    effort_med = len(list(df[df['effort'] == 'Medium'].values))
    effort_hig = len(list(df[df['effort'] == 'Large'].values))
    valid_bods = context['xmls_counts'][1]
    invalid_bods = context['xmls_counts'][2]
    data_set_1 = [c_low, c_medium, c_high]  # Replace with your data
    data_set_3 = [effort_low, effort_med, effort_hig]  # Replace with your data
    total_files = valid_bods+invalid_bods
    valid_files =valid_bods
    invalid_files = invalid_bods
    label1 = ["Low", "Medium", "High"]  # Labels for x-axis
    label3 = ["Completely Migratable", "partially Migratable", "Need to be redesigned"]
    label2 = ["Valid Data Service Objects", "Invalid Data Service Objects"]
    context1 = {
        "data_set_1": data_set_1,
        "data_set_3": data_set_3,
        "total_files": total_files,
        "valid_files": valid_files,
        "invalid_files": invalid_files,
        "label1": label1,
        "label3": label3,
        "label2": label2,
        "data": context['summary'],
    }
    
    complexity = context['complexity']
    result = context['result']
    zipped = zip(complexity, result.values())
    result_complexity = list(zipped)
    converted_results = []
    for i in result_complexity:
        result_for_conversion = {}
        result_for_conversion['file_name'] = i[0]["file_name"]
        result_for_conversion['complexity'] = i[0]["Complexity"]    
        result_for_conversion['result'] = i[1]
        if i[1] == "Failed":
            result_for_conversion['di_filename'] = ''
        else:
            result_for_conversion['di_filename'] =  i[0]["file_name"].replace(".xml", ".json")
        converted_results.append(result_for_conversion)
        print(context1)
    if request.method == 'POST':
        user_path = request.POST.get('user_path')  # Get the value from the form
        return render(request, "result.html", {"data": converted_results, 'user_path':user_path})
    return render(request, "summary.html", context1)


def result(request):
    return render(request, "result.html")

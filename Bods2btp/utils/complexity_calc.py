# Created by Harikrishnan at 18:33 20-09-2023 using PyCharm
# To define the complexity of a XML file extracted from BODS
# import logging
# logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)
import pandas as pd
from xml.etree import ElementTree
import xml.etree.ElementTree as ET
from Bods2btp.utils.driver import main_prog1
# import os
# import lxml
from io import BytesIO
import Bods2btp.utils.inbuild_function as IFD
import Bods2btp.utils.scoring_naming_std as sc
# from lxml import objectify

all_jobs = []
repo_ver = ''
system_ver = ''
Bods_obj = ['DIScript','DIQuery','DITransformCall']

project_flag = False
dataintegrator_flag = False
job_flag = False


def flush_data():
    global all_jobs,repo_ver,system_ver
    all_jobs = []
    repo_ver = ''
    system_ver = ''

# Parses an XML element object and returns a dictionary containing the information extracted from the XML.
#  Parameters:element_obj (Element): The XML element object to parse.
#  Returns:dict: A dictionary containing the extracted information from the XML,
#  with the XML tag as the key and a list of attribute dictionaries as the value.

def parse_xml(element_obj):
    xml_info = {}
    for element in element_obj.iter():
        tag = element.tag
        value = element.attrib
        if tag not in xml_info:
            xml_info[tag] = []
        if value:
            xml_info[tag].append(value)
    return xml_info

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
    return result

# Calculates the complexity of the xml file using the parameters extracted from XML File.
# parameters are:num_of_operators, num_of_dataflow, is_parallel_connection, is_functional_call,
#                          num_of_jobs, script_functions extracted from the xml file
# Returns the mode of complexity as per the calculations
# def complexity_calculation(num_of_operators, num_of_dataflow, is_parallel_connection, is_functional_call,
#                          num_of_jobs, script_functions):
#     global complexity


# Extracts data from an XML file and returns various statistics.
#    Parameters:        xml_file_path (str): The path to the XML file.
#    Returns:        tuple: A tuple containing the following statistics:
#         - num_of_operators (int): The number of operators in the XML file.
#           - num_of_dataflow (int): The number of dataflows in the XML file.
#      - is_parallel_connection (bool): True if there are parallel connections in the XML file, False otherwise.
#     - is_functional_call (bool): True if there are functional calls in the XML file, False otherwise.
#        - num_of_jobs (int): The number of jobs in the XML file.
#        - script_functions (bool): True if there are custom functions in the XML file, False otherwise.
#        - check_flag (bool): False if the xml file is invalid """
def calculate_complexity(content):
    try:
        global all_jobs, repo_ver,system_ver,Bods_obj
        source_complexity = 'No criteria'
        # xml_io = BytesIO(content)
        tree = ET.ElementTree(ET.fromstring(content))
        root = tree.getroot()
        gen_1,gen_2 = count_distinct_gen_1_2_equivalent_operators(root)
        cust_op_di_count = count_of_custom_opr_di(root)

        is_parallel_connection = False
        is_functional_call = False
        script_functions = False
        dataflow_count_dict = {}
        all_jobs =[]
        job_lst = []
        transformations_lst = []
        transform_lst = []
        workflow_lst = []
        transformations_lst = []
        workflow_dict = {}
        all_tags = {}
        workflow_flag = False
        dataflow_flag = False
        project_flag = False
        dataintegrator_flag = False
        job_flag = False
        #count of functions
        #inbuilt Functions
        tag_name = 'FUNCTION_CALL'
        data = [element.items() for element in root.iter(tag_name)]
        data = [dict(x)['name'] for x in data]
        data = set(data)
        inbuild_function_names_l = [val for val in data if val in IFD.lst]
        inbuilt_function = sum(1 for val in data if val in IFD.lst)
        #Sql Functions
        lst2=['sql']
        data = [element.items() for element in root.iter(tag_name)]
        data = [dict(x)['name'] for x in data]
        # data = set(data)
        sql_function = sum(1 for val in data if val in lst2)
        #Custom Functions
        data = [element.items() for element in root.iter(tag_name)]
        data = [dict(x)['name'] for x in data]
        data = set(data)
        custom_function = sum(1 for val in data if val not in IFD.lst and val not in lst2)
        # Iterate through XML elements
        for branch in root:

            tag = branch.tag
            val = branch.attrib
            for child1 in branch:
                for child2 in child1:
                    if child2.tag in Bods_obj:
                        tag_details = []
                        child3_details = []
                        for child3 in child2:
                            tag_details.append(child3.tag)
                            child3_details.append(child3)
                        key_dict = child2.tag

                        if 'DIUIOptions' in tag_details:
                            check_uiname = []
                            for child4 in child3_details:
                                for child5 in child4:
                                    if 'name' in child5.attrib.keys():
                                        check_uiname.append(child5.attrib['name'])
                                        if child5.attrib['name'] == 'ui_display_name':

                                            if key_dict == 'DITransformCall':
                                                key_dict = child2.attrib['name']
                                            if key_dict not in all_tags.keys():
                                                all_tags[key_dict] = [child5.attrib['value']]
                                            else:
                                                all_tags[key_dict].append(child5.attrib['value'])
                            if 'ui_display_name' not in check_uiname:
                                if key_dict == 'DITransformCall':
                                    key_dict = child2.attrib['name']
                                if key_dict not in all_tags.keys():
                                    all_tags[key_dict] = ['Default']
                                else:
                                    all_tags[key_dict].append('Default')
                        else:
                            if key_dict == 'DITransformCall':
                                key_dict = child2.attrib['name']
                            if key_dict not in all_tags.keys():
                                all_tags[key_dict] = ['Default']
                            else:
                                all_tags[key_dict].append('Default')

            if tag not in all_tags.keys():
                if 'name' in val:
                    all_tags[tag] = [val['name']]
                else:
                    all_tags[tag] = ['N/A']
            else:
                all_tags[tag].append(val['name'])
            if 'DataIntegratorExport' in root.tag:
                dataintegrator_flag = True

            if 'Project' in tag:
                project_flag = True

            if 'Job' in tag:
                job_flag = True
                if 'name' in val:
                    job_lst.append(val['name'])
                    all_jobs.append(val['name'])

                else:
                    job_lst.append('N/A')
                    all_jobs.append('N/A')
                repo_ver = root.attrib['repositoryVersion']
                system_ver = root.attrib['productVersion']
                # with open("test.txt", 'w') as f:
                #     f.write((str(root.attrib)))
                #     f.write(str(val))
                #     f.write(str(tag))
                #     f.write(str(job_lst))


            if 'Workflow' in tag:
                workflow_flag = True
                workflow_lst.append(val['name'])

                # Extract sub-elements under Workflow
                branch_obj = branch.find('./DISteps')
                if branch_obj is not None:
                    for obj in branch_obj:
                        workflow_dict[obj.tag] = parse_xml(obj)
                        if 'Script' in obj.tag:
                            transform_lst.append(obj.tag)
                            is_functional_call = any(value == 'FUNCTION_CALL' for value in parse_xml(obj).keys())

            # Extract Dataflow information
            if 'Dataflow' in tag:
                dataflow_flag = True
                script_functions = any(root.findall(".//DIScriptFunction"))
                transformations = branch.find('./DITransforms')
                if transformations is not None:

                    for tags in transformations:
                        transformations_lst.append(tags.tag)
                        transform_lst.append(tags.attrib)
                    dataflow_count_dict[branch.attrib['name']] = transformations_lst
                    # Extract information from sub-elements of Dataflow
                    for sub_branch in transformations:
                        transformation = transformations.find('./{}'.format(sub_branch.tag))

                        if transformation is not None:
                            xml_info = parse_xml(transformation)
                            # Check for parallel connections and functions in Queries and Scripts
                            if 'Query' in sub_branch.tag:
                                is_parallel_connection = sum(
                                    'ui_acta_from' in value['name'] for value in xml_info['DIAttribute']) > 1
                            if 'Query' in sub_branch.tag or 'Script' in sub_branch.tag:
                                is_functional_call = any(value == 'FUNCTION_CALL' for value in parse_xml(sub_branch).keys())
            # if 'Script' in tag:
            #     transform_lst.append("DIScript")
            for script_element in root.findall(".//DIScript"):

                attribute_element = script_element.find(".//DIAttribute[@name='ui_display_name']")
                if attribute_element is not None:
                    if "DIScript" not in all_tags.keys():
                        all_tags["DIScript"] = [attribute_element.attrib["value"]]
                        transform_lst.append("DIScript")
                    else:
                        if attribute_element.attrib["value"] not in all_tags["DIScript"]:
                            all_tags["DIScript"].append(attribute_element.attrib["value"])
                            transform_lst.append("DIScript")



        num_of_jobs = len(job_lst)
        # num_of_operators = len(transformations_lst)
        # num_of_dataflow = len(dataflow_count_dict)
        dist_operator_list = set(map(str, transform_lst))
        num_dist_operator = len(dist_operator_list)
        score,operators_list = return_score(all_tags)
        effort, coverage = cal_indicative_eff(gen_1, gen_2, cust_op_di_count,num_dist_operator)

        if 'DIDataflow' in all_tags.keys():
            data_flow_list = all_tags['DIDataflow']
        else:
            data_flow_list = []
        if 'DIDatabaseDatastore' in all_tags.keys():
            data_stores_l = all_tags['DIDatabaseDatastore']
        else:
            data_stores_l = []
        if 'DIWorkflow' in all_tags.keys():
            workflow_l = all_tags['DIWorkflow']
        else:
            workflow_l = []
        ### Source_complexity
        if num_of_jobs > 2:
            jb = 3
        elif num_of_jobs == 2:
            jb = 2
        else:
            jb = 1

        if num_dist_operator > 10:
            op = 3
        elif num_dist_operator > 5 and num_dist_operator <= 10:
            op = 2
        else:
            op = 1

        if custom_function > 1:
            cf = 3
        elif custom_function == 1:
            cf = 2
        else:
            cf = 1
        complexity_map = {1: 'Low', 2: 'Medium', 3: 'High'}
        source_complexity_num = max(jb, cf, op)
        source_complexity = complexity_map[source_complexity_num]
        all_jobs_with_na = ['N/A' if name == "" else name for name in all_jobs]
        workflow_name = ','.join(workflow_l)
        if len(inbuild_function_names_l) != 0:
            inbuild_function_names = ','.join(inbuild_function_names_l)
        else:
            inbuild_function_names = 'Nill'
        if len(operators_list) != 0:
            operators_names = ','.join(operators_list)
        else:
            operators_names = 'N/A'
        job_names = ', '.join(all_jobs_with_na)
        workflows = len(workflow_l)
        dataflows = len(data_flow_list)
        if len(data_stores_l) != 0:
            data_stores = ', '.join(data_stores_l)
        else:
            data_stores = 'N/A'
        ### Source complexity ####
        # if not any([job_flag, workflow_flag, dataflow_flag]):
        #     raise Exception('Invalid File')
        # if not all([job_flag, workflow_flag, dataflow_flag]):
        #     raise Exception('Invalid XML File')
        # else:
        # return complexity
        # return num_of_operators, num_of_dataflow, is_parallel_connection, is_functional_call, num_of_jobs, script_functions
        # if num_of_operators >= 10 or num_of_jobs > 1 or is_functional_call or script_functions:
        #     complexity = 'High'
        # elif 5 <= num_of_operators < 10 and num_of_dataflow > 1 or is_parallel_connection:
        #     complexity = 'Medium'
        # elif num_of_operators < 5 and num_of_dataflow == 1:
        #     complexity = 'Low'
        # else:
        #     complexity = 'No criteria matches'
        return inbuilt_function,sql_function,custom_function,dataintegrator_flag,project_flag,job_flag,\
               source_complexity,score,job_names,num_dist_operator,num_of_jobs,workflows,data_stores,effort,coverage,workflow_name,operators_names,inbuild_function_names

    except ET.ParseError:
        repo_ver = 'Null'
        system_ver = 'Null'
        all_jobs=['Null']
        return 'Null','Null','Null','Null','Null','Null','Null','Null','Null','Null','Null','Null','Null','Null','Null','Null','Null','Null'


def complexity_assessment_report(project_flag,dataintegrator_flag,job_flag):

    global all_jobs,system_ver,repo_ver
    valid_bods = 0
    invalid_bods = 0
    job_names = ",".join(all_jobs)
    if project_flag != 'Null':
        if project_flag and dataintegrator_flag and job_flag:
            valid_bods = 1
        else:
            invalid_bods = 1
    else:
        invalid_bods = 1
    return repo_ver, system_ver, job_names, valid_bods, invalid_bods

def return_score(tags):
    operators = []
    naming_std = sc.naming_conventions
    total_no_obj = 0
    total_obj_score = 0
    for obj_key in tags.keys():
        if obj_key in naming_std.keys():
            # print(obj_key)
            opera = ['DIProject','DIJob','DIWorkflow','DIDataflow']
            if obj_key not in opera:
                operators.append(obj_key)
            num_s_obj = len(tags[obj_key])
            no_s_corrent_obj = 0
            total_no_obj += 1
            for objs in tags[obj_key]:
                if bool(naming_std[obj_key].match(objs)):
                    no_s_corrent_obj += 1
            obj_score = no_s_corrent_obj / num_s_obj
            total_obj_score = total_obj_score + obj_score
    if total_no_obj != 0:
        score_naming = str(int((total_obj_score/total_no_obj)*100))
    else:
        score_naming = '0'
    return score_naming,operators

def cal_indicative_eff(eq_gen1,eq_gen2,eq_custo,tot_oprt):
    no_of_gen1_operators = eq_gen1
    no_of_gen2_operators = eq_gen2
    count_of_custom_functions = eq_custo
    count_of_total_operators_in_xml = tot_oprt
    if count_of_total_operators_in_xml != 0:
        target_coverage = int(((max(no_of_gen1_operators,
                               no_of_gen2_operators) + count_of_custom_functions) / count_of_total_operators_in_xml)*100)
    else:
        target_coverage = 0
    # target_coverage
    indicative_effort = ''
    if target_coverage < 70:
        indicative_effort = 'Large'
    elif 70 <= target_coverage <= 80:
        indicative_effort = 'Medium'
    else:
        indicative_effort = 'Small'

    return indicative_effort,target_coverage

def count_distinct_gen_1_2_equivalent_operators(root):
    # xml_io = BytesIO(content)
    # tree = ET.parse(xml_io)
    # root = tree.getroot()
    """
    The function `count_distinct_gen1_equivalent_operators` counts the number of distinct operators in a
    given XML tree and returns a list of those operators along with the count.

    :param root: The `root` parameter is expected to be an XML element or tree that represents the root
    of an XML document
    :return: The function `count_distinct_gen1_equivalent_operators` returns a tuple containing two
    values. The first value is a list of distinct equivalent operators found in the XML tree represented
    by the `root` parameter. The second value is an integer representing the count of distinct gen1
    operators.
    """

    equivalent_gen1_operators = {
        "DIDatabaseTableSource": "com.sap.database.table.consumer.v2",
        "DIDatabaseTableTarget": "com.sap.database.table.producer.v2",
        "DIFileSource": "com.sap.storage.consumer.v2",
    }
    equivalent_gen2_operators = {
        "DIDatabaseTableSource": "com.sap.database.table.consumer.v3",
        "DIDatabaseTableTarget": "com.sap.database.table.producer.v4",
        "DIFileSource": "com.sap.storage.consumer.v3",
    }
    distinct_operators1 = set()
    distinct_operators2 = set()
    for element in root.iter():
        tag = element.tag
        name = element.get("name")
        if tag in equivalent_gen1_operators:
            distinct_operators1.add(equivalent_gen1_operators[tag])
        if name in equivalent_gen1_operators:
            distinct_operators1.add(equivalent_gen1_operators[name])
        if tag in equivalent_gen2_operators:
            distinct_operators2.add(equivalent_gen2_operators[tag])
        if name in equivalent_gen2_operators:
            distinct_operators2.add(equivalent_gen2_operators[name])
    count_of_distinct_gen1_operators = len(distinct_operators1)
    count_of_distinct_gen2_operators = len(distinct_operators2)
    return count_of_distinct_gen1_operators,count_of_distinct_gen2_operators

def count_of_custom_opr_di(root):
    di_gen1_opr={"com.sap.merge":"Merge","com.sap.basedatamask":"SDKTransform","com.sap.keygeneration":"Key_Generation"}
    custom_count=0
    opr_name=[]

    # To extract data from an XML file
    transformations_lst = []

    # Iterate through XML elements
    for branch in root:
        tag = branch.tag
        # Extract Dataflow information
        if 'Dataflow' in tag:
            transformations = branch.find('./DITransforms')
            if transformations is not None:
                # transformations_lst = []
                for tags in transformations:
                    transformations_lst.append(tags.attrib)

    ds_opr = [item['name'] for item in transformations_lst if 'name' in item]

    for value in di_gen1_opr.values():
        if value in ds_opr:
            key_list = list(di_gen1_opr.keys())
            val_list = list(di_gen1_opr.values())
            pos = val_list.index(value)
            opr_name.append(key_list[pos])
            custom_count += 1

    return custom_count
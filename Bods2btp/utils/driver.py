# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 19:21:14 2023

@author: MelvinM
"""

import pandas  as pd
from xml.etree import ElementTree
import xml.etree.ElementTree as ET
import os
import lxml
from lxml import objectify
from collections import OrderedDict
from Bods2btp.utils.OperatorLookup import operator_lookup_df,lookup_information
from Bods2btp.utils.parse import parse_data_from_xml
from Bods2btp.utils.migration import graph_creation
from io import BytesIO

def parse_xml(element_obj):
    xml_info = {}
    for i in element_obj.iter():
        tag = i.tag
        value = i.attrib
        
        if not value:
            continue
        if tag in xml_info.keys():
            prev_val = xml_info[tag]
            if isinstance(prev_val,list):
                prev_val.append(value)
                xml_info[tag] = prev_val
            else:
                prev_val = [xml_info[tag]]
                prev_val.append(value)
                xml_info[tag] = prev_val
                
        else:
            xml_info[tag] = value
    
    return xml_info

def check_data(root):
    transformations = root.find('./DIDataflow/DITransforms')
    
    is_lookup_used = False
    
    for tags in transformations:
        if 'DIQuery' in tags.tag:
            query_info = parse_xml(tags)
            
            if 'DIExpression' in query_info:
                for expression in query_info["DIExpression"]:
                    if expression['expr'].startswith('lookup_ext'):
                        is_lookup_used = True
    
    lookup_obj = {'is_lookup_used':is_lookup_used}
    return lookup_obj


def make_the_lookup(transformations_lst,lookup_obj,operator_lookup_df):
    transformation_mapping = {}
    is_lookup_used = lookup_obj['is_lookup_used']
    transformation_mapping = OrderedDict()
    for transformation in transformations_lst:
        if transformation=='DIQuery':
            continue
        else:
            lobj = operator_lookup_df[operator_lookup_df["BODS_OPERATOR"]==transformation]
            if len(lobj)>1:
                target_operator = lobj[lobj['LOOKUP'] == is_lookup_used]['DI_OPERATOR'].to_list()[0]
            else:
                target_operator = operator_lookup_df[operator_lookup_df["BODS_OPERATOR"]==transformation]['DI_OPERATOR'].to_list()[0]
            
            transformation_mapping[transformation] = target_operator
    
    return transformation_mapping


def main_prog1(content, file_path, file_name):
    
    xml_data = BytesIO(content)
    tree = ET.parse(xml_data)
    
    
    # tree = ET.parse('csv_to_table_xml.xml')
    
    # tree = ET.parse(xml_file_name)
    root = tree.getroot()
    
    dataflow_transforms = root.find('./DIDataflow/DITransforms')
    
    
    transformations_lst = []
    
    for i in dataflow_transforms:
        transformations_lst.append(i.tag)
    
    lookup_obj = check_data(root)
    
    transformation_mapping = make_the_lookup(transformations_lst,lookup_obj,operator_lookup_df)
    
    bods_obj  = parse_data_from_xml(root)
    
    message = graph_creation(transformation_mapping,bods_obj, FILE_PATH=file_path, File_name=file_name)
    return message



if __name__ == "__main__":
    transformation_mapping,bods_ob = main_prog1("csv_to_table_xml.xml")
    # for bods in bods_ob:
    #     open("data.txt","a").write(f"{bods.name}\n{bods.connections}\n{bods.value}\n{'*******'*10}\n")
    print(transformation_mapping.values())
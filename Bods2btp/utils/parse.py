# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 18:10:27 2023
@author: MelvinM
"""

import pandas  as pd
from xml.etree import ElementTree
import xml.etree.ElementTree as ET
import os
import lxml
from lxml import objectify


import os



class BODSObj():
    def __init__(self,name,transform_type,connections,value):
        self.name = name
        self.transform_type = transform_type
        self.connections = connections
        self.value = value
        
# class DataBaseObject():
#     def __init__(self,name,dbtype,subtype,server_database,server_version):
#         self.name = name
#         self.dbtype = dbtype
#         self.subtype = subtype
#         self.server_database = server_database
#         self.server_version = server_version



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


def extract_file_info(file_info):
    connectionID,file_location = None,None
    attr = file_info['DIAttribute']
    input_ID,output_ID = None,None

    
    
    if 'DIOutputView' in file_info.keys():
        output_ID = file_info['DIOutputView']['name']
       
    
    if 'DIInputView' in file_info.keys():
        input_ID = file_info['DIInputView']['name']
        
    
    for atr in attr:
        if atr['name'] == 'file_location':
            connectionID = atr['value']
        
        if atr['name'] == 'root_dir':
            file_location = atr['value']
            
    file_name = file_info['DIFileSource']['filename']
            
    file_location = file_location.split(':')[1].replace('\\','/')
        
    return connectionID,file_location,file_name,input_ID,output_ID


def extract_table_info(table_info):
    table_meta = parse_xml(table_info) 

    column_info = table_meta['DIColumn']
    table = table_meta['DITable']


    if 'name' in table.keys() or 'owner' in table.keys():
        tname = table['name'].replace('"','')
        tschema = table['owner']
        table_name = "\"{}\".\"{}\"".format(tschema,tname)
        qualified_name = "/{}/{}".format(tschema,tname)
        nativeQualifiedName= None
        
        
    new_column_info = []
    for i in column_info:
        if i['datatype'].lower().find("char") !=-1:
            new_column_info.append({'name':i['name'],'type':i['datatype'],'size':i['size']})
        else:
            new_column_info.append({'name':i['name'],'type':i['datatype']})
    
    
    
    return table_name,qualified_name,nativeQualifiedName,new_column_info,tname


    
def extract_query_info(query_info):
    
    is_lookup_used  = False
    
    connection_dict = {}
    transformation_mapping = []
    
    if 'DIAttribute' in query_info.keys():
        dat = query_info['DIAttribute']
        connection_tmp = {i['name']:i['value'] for i in dat if 'ui_acta_from_schema' in i['name'] }
        for i,j in enumerate(connection_tmp):
            connection_dict['input_{}'.format(i+1)] = connection_tmp[j]
    
    if 'DISchema' in query_info.keys():
        # Needs to be changed
        connection_dict['output_1'] = query_info['DISchema']['name']
        
    
    if 'DIElement' in query_info and 'DIExpression' in query_info:
        for element,expression in zip(query_info['DIElement'],query_info["DIExpression"]):
            if expression['expr'].startswith('lookup_ext'):
                is_lookup_used = True
            
            else:
                element['expression'] = expression['expr']
                transformation_mapping.append(element)
    
    if 'DIExpression' in query_info:
        for expression in query_info['DIExpression']:
            if expression['expr'].find('=')!=-1:
                is_lookup_used = True
    
    return connection_dict,is_lookup_used,transformation_mapping
        
def extract_db_info(table_info):
    tname,input_ID,output_ID = None,None,None
    for key,val in table_info.items():
        if 'DIDatabaseTable' in key:
            tname = table_info[key]['tableName']
            datastore_name = table_info[key]['datastoreName']
            ownerName = table_info[key]['ownerName']
        
        if 'DIInputView' in key:
            input_ID = table_info[key]['name']
            
        if 'DIOutputView' in key:
            output_ID = table_info[key]['name']
            
    return tname,datastore_name,ownerName,input_ID,output_ID
   

            
            
def parse_data_from_xml(root):
    
    data_flow = root.find('./DIDataflow')

    dataflow_transforms = data_flow.find('./DITransforms')

    # ********************************************************************
    # Extract Table Column Info
    table_metadata = {}

    bods_objs = []

    for table in root.iter('DITable'):
        table_name,qualified_name,nativeQualifiedName,new_column_info,tname= extract_table_info(table)
        table_metadata[tname] = {'table_name':table_name,
                                 'columns':new_column_info,
                                 'qualified_name':qualified_name,
                                 'nativeQualifiedName':nativeQualifiedName}
        
    # ********************************************************************




    # ********************************************************************
    # Extract DB Data
    # Need to check if many db is added
    databasedatastore_root = root.find('./DIDatabaseDatastore')
    db_store_name = databasedatastore_root.attrib['name']

    database_tmp_dict = {}

    for db_obj  in databasedatastore_root.find('DIAttributes'):
        obj_val =  db_obj.attrib
        if 'hasNestedXMLTree' in obj_val.keys():
            if obj_val['hasNestedXMLTree'] == 'true':
                for config_obj in db_obj.iter():
                    # All db info is already stored in a dictionary (For future ref)
                    database_tmp_dict[config_obj.tag] = config_obj.text


    extracted_db_tmp = {key:val for key,val in database_tmp_dict.items() if key in ['database_type','database_subtype','sql_server_database','sql_server_version']}
    extracted_db = {db_store_name : extracted_db_tmp}              
    # ********************************************************************


    # ********************************************************************
    # Extract FileInformation Data
    # Need to check if many db is added
    file_tmp_dict = {}
    filedatastore_root = root.find('./DIFlatFileDatastore')
    if filedatastore_root:
        
        file_store_name = filedatastore_root.attrib['name']
        file_look_dict  = []
        for obj in filedatastore_root.find('./DISchema'):
            element = obj.attrib
            element['type'] = element['datatype']
            del element['datatype']
            file_look_dict.append(element)
        file_tmp_dict[file_store_name] = {'columns':file_look_dict}
        
    # ********************************************************************    



    for tags in dataflow_transforms:
        
        if 'DIQuery' in tags.tag:
            transformation_mapping = []
            query_info = parse_xml(tags)
            query_connection,is_lookup_used,transformation_mapping  = extract_query_info(query_info)
            data_values = {'is_lookup_used':is_lookup_used,'transformation_mapping':transformation_mapping}
            bods = BODSObj('Query','Query',query_connection,data_values)       

            bods_objs.append(bods)       
            
            
        
        if 'DIFile' in tags.tag:
            columns_info = None
            file_info = parse_xml(tags)
            connectionID,file_location,file_name,input_ID,output_ID = extract_file_info(file_info)
            connection_values = {'input_ID':input_ID,'output_ID':output_ID}
            if output_ID in file_tmp_dict.keys():
                columns_info = file_tmp_dict[output_ID]['columns']
                
                
            data_values = {'connectionID':connectionID,'file_location':file_location,
                           'file_name':file_name,'operator_name':output_ID,'columns':columns_info}
            
            
            bods = BODSObj('DIFile',output_ID,connection_values,data_values)
            bods_objs.append(bods)
            
        
         
        
        if 'DatabaseTableTarget' in tags.tag:
            table_info = parse_xml(tags)
            dsstore_name = table_info['DIDatabaseTableTarget']['datastoreName']
            tname,datastore_name,ownerName,input_ID,output_ID = extract_db_info(table_info)  
            connection_values = {'input_ID':input_ID,'output_ID':output_ID}
            data_values = table_metadata[tname]
            data_values.update(extracted_db[dsstore_name])
            bods = BODSObj('DIDatabaseTableTarget',output_ID,connection_values,data_values)
            bods_objs.append(bods)



        if 'DatabaseTableSource' in tags.tag:           
            table_info = parse_xml(tags)
            dsstore_name = table_info['DIDatabaseTableSource']['datastoreName']
            tname,datastore_name,ownerName,input_ID,output_ID = extract_db_info(table_info)  
            connection_values = {'input_ID':input_ID,'output_ID':output_ID}
            data_values = table_metadata[tname]
            data_values.update(extracted_db[dsstore_name])
            bods = BODSObj('DatabaseTableSource',output_ID,connection_values,data_values)
            bods_objs.append(bods)
    
    return bods_objs
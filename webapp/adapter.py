# graph description is required # default is BODS2DI
table_consumer = {
			"component": "com.sap.database.table.consumer.v2",
			"metadata": {
				"label": "Table Consumer",
				"config": {
					"service": "", # HANA_DB
					"serviceConnection": {
						"configurationType": "Configuration Manager",
						"connectionID": "" #HANADB_02
					},
					"source": {
						"remoteObjectReference": {
							"name": "", #CUSTOMER$
							"remoteObjectType": "TABLE",
							"qualifiedName": "", #/DBADMIN/CUSTOMER%24
							"nativeQualifiedName": "",#\"DBADMIN\".\"CUSTOMER$\"
							"owner": "" # DBADMIN (schema name)
						},
						"filter": {
							"selectOptions": []
						}
					}
				},
				"outports": [
					{
						"name": "outTable",
						"type": "table",
						"vtype-ID": "$GRAPH.generated.process_name_outTable"
					}
				]
			}
		}


table_producer = {
			"component": "com.sap.database.table.producer.v2",
			"metadata": {
				"label": "Table Producer",
				"config": {
					"service": "", #HANA_DB
					"serviceConnection": {
						"configurationType": "Configuration Manager",
						"connectionID": "" # HANADB_02
					},
					"source": {
						"remoteObjectReference": {
							"name": "", #TRGTTESTTBL
							"remoteObjectType": "TABLE",
							"qualifiedName": "", # /DBADMIN/CUSTOMER%24 (table name and schema name )
							"nativeQualifiedName": "", #\"DBADMIN\".\"TRGTTESTTBL\"
							"owner": "" # DBADMIN (schema name )
						},
						"schema": {
							"genericType": "TABLE",
							"tableBasedRepresentation": {
								"attributes": [] # required the columns of the tgt table Ignore incrementing column
							}
						}
					},
					"attributeMappings": [], # required the mapping columns data
					"mode": "" # append , overwrite, truncate
				},
				"inports": [
					{
						"name": "inTable",
						"type": "table",
						"vtype-ID": "$GRAPH.generated.process_name_outTable"
					}
				]
			}
		}

file_consumer = {
			"component": "com.sap.storage.consumer.v2",
			"metadata": {
				"label": "Structured File Consumer",
				"config": {
					"service": "", # SDL
					"serviceConnection": {
						"configurationType": "Configuration Manager",
						"connectionID": "" # DI_DATA_LAKE
					},
					"source": {
						"remoteObjectReference": {
							"name": "", #uc2_src_2.csv ( File name)
							"qualifiedName": "", #/shared/SAP_DI_Training2/SAP_DEMO/bods_di/uc2_src_2.csv (path)
							"nativeQualifiedName": "" #/shared/SAP_DI_Training2/SAP_DEMO/bods_di/uc2_src_2.csv (path)
						},
						"schema": {
							"genericType": "TABLE",
							"tableBasedRepresentation": {
								"attributes": []
							}
						}
					}
				},
				"outports": [
					{
						"name": "outTable",
						"type": "table",
						"vtype-ID": "$GRAPH.generated.process_name_outTable"
					}
				]
			}
		}

graph_terminator = {
			"component": "com.sap.util.graphTerminator",
			"metadata": {
				"label": "Graph Terminator"
			}
		}

operators_jsons = {"table_consumer" : table_consumer, "table_producer":table_producer, "file_consumer":file_consumer, "graph_terminator":graph_terminator}

s_cat_ports = {
    "read_file": {
        "input": [{"name": "ref", "dtype": "message.file"}],
        "output": [
            {"name": "file", "dtype": "message.file"},
            {"name": "error", "dytpe": "message.error"}
        ]
    },
    "read_hana_table": {
        "input": [{"name": "input", "dtype": "message.table"}],
        "output": [
            {"name": "success", "dtype": "message.table"},
            {"name": "error", "dtype": "message.error"}
        ]
    },
    "write_hana_table": {
        "input": [{"name": "input", "dtype": "message.table"}],
        "output": [
            {"name": "success", "dtype": "message.table"},
            {"name": "error", "dtype": "message.error"}
        ]
    },
    "run_hana_sql": {
        "input": [{"name": "input", "dtype": "message.*"}],
        "output": [{"name": "success", "dtype": "message.table"},
                   {"name": "error", "dtype": "message.error"}]
    },
    "initialize_hana_table": {"input": [{"name":"input", "dtype":"message.table"}],
                              "output": [{"name": "success", "dtype": "message.table"},
                                         {"name": "error", "dtype": "message.error"}]},

    "list_files": {"input": [{"name": "dirRef", "dtype": "message.file"}],
                   "output": [
                            {"name": "ref", "dtype": "message.file"},
                            {"name": "error", "dytpe": "message.error"}
        ]},
    "write_file": {
            "input": [{"name": "file", "dtype": "message.file"}],
            "output": [
                {"name": "file", "dtype": "message.file"},
                {"name": "error", "dytpe": "message.error"}
        ]
    },
    "file_to_message_converter": {
            "input": [{"name": "file", "dtype": "message.file"}],
            "output": [
                {"name": "path", "dtype": "message"},
                {"name": "message", "dytpe": "message"}
        ]     
    },
    "decode_table": {
        "input": [{"name": "input", "dtype": "message"}],
        "output": [
                {"name": "output", "dtype": "message.table"}
        ]
    },
    "generate_table": {
        "input": [{"name": "trigger", "dtype": "any.*"}],
        "output": [
                {"name": "output", "dtype": "message.table"}
        ]
    },
    "sap_hana_client": {
        "input": [{"name": "sql", "dtype": "message"},
                  {"name": "data", "dtype": "message"}],
        "output": [
                {"name": "result", "dtype": "message"}
        ]
    },
    "file_consumer" : {
        "input" : [{"name":"inTrigger", "dtype": "message"}],
        "output": [{"name" : "outTable", "dtype": "Table"}]
    },
    "table_consumer" : {
        "input" : [{"name":"inTrigger", "dtype": "message"}],
        "output" : [{"name" : "outTable", "dtype": "Table"}]
    },
    "table_producer" :{
        "input": [{"name":"inTable", "dtype": "Table"}],
        "output":[{"name":"outMessage", "dtype": "message"}]
    },
    "graph_terminator":{
        "input":[{"name":"stop", "dtype":"any.*"}]
    }
}
#____________________________________Coding-part________________________________
# operators_required_parameters = {"table_consumer": "", "table_producer":"", "file_consumer":"", "graph_terminator":""}






file_consumer_setup_code = """graph["processes"][process_name]["metadata"]["config"]["service"] = "SDL"
            graph["processes"][process_name]["metadata"]["config"]["serviceConnection"]["connectionID"] = obj.value["connectionID"]
            graph["processes"][process_name]["metadata"]["config"]["source"]["remoteObjectReference"]["name"] = obj.value["file_name"]
            graph["processes"][process_name]["metadata"]["config"]["source"]["remoteObjectReference"]["qualifiedName"] = obj.value["file_location"]
            graph["processes"][process_name]["metadata"]["config"]["source"]["remoteObjectReference"]["nativeQualifiedName"] = obj.value["file_location"]"""
file_consumer_setup_code = """graph["processes"][process_name]["metadata"]["config"]["service"] = "SDL"
            graph["processes"][process_name]["metadata"]["config"]["serviceConnection"]["connectionID"] = value["connectionID"]
            graph["processes"][process_name]["metadata"]["config"]["source"]["remoteObjectReference"]["name"] = value["file_name"]
            graph["processes"][process_name]["metadata"]["config"]["source"]["remoteObjectReference"]["qualifiedName"] = value["file_location"]
            graph["processes"][process_name]["metadata"]["config"]["source"]["remoteObjectReference"]["nativeQualifiedName"] = value["file_location"]"""

table_producer_setup_code = """if not list_of_obj[index].value["is_lookup_used"]:
                graph["processes"][process_name]["metadata"]["config"]["service"] = obj.value["database_type"]
                graph["processes"][process_name]["metadata"]["config"]["source"]["remoteObjectReference"]["owner"] = obj.value["sql_server_database"]
                graph["processes"][process_name]["metadata"]["config"]["source"]["remoteObjectReference"]["name"] = obj.value["table_name"].split(".")[1].replace('"',"")
                graph["processes"][process_name]["metadata"]["config"]["source"]["remoteObjectReference"]["qualifiedName"] = obj.value["qualified_name"]
                graph["processes"][process_name]["metadata"]["config"]["source"]["remoteObjectReference"]["nativeQualifiedName"] = obj.value["nativeQualifiedName"]
                total_cols = list()
                for col in obj.value["columns"]:
                    temp_col = {}
                    temp_col["name"] = col["name"]
                    temp_col["nativeDatatype"] = col["type"]
                    nativeDatatype = col["type"]
                    if nativeDatatype.lower().find("char") != -1:
                        temp_col["datatype"] = "STRING"
                        temp_col["templateType"] = "string"
                        temp_col["Length"] = col["size"]
                        temp_col["nativeLength"] = col["size"]
                    elif nativeDatatype.lower().find("int") != -1:
                        temp_col["datatype"] = "INTEGER"
                        temp_col["templateType"] = "int32"
                        temp_col["Length"] = 8
                        temp_col["nativeLength"] = 10
                    # elif nativeDatatype.find("false") != -1 or nativeDatatype.find("true") != -1 or nativeDatatype.find("True")!= -1 or nativeDatatype.find("False")!= -1 or nativeDatatype.find(True)!= -1 or nativeDatatype.find(False)!= -1:
                    #     dtype = "boolean"
                    # elif nativeDatatype
                    total_cols += [temp_col]
                graph["processes"][process_name]["metadata"]["config"]["source"]["schema"]["tableBasedRepresentation"]["attribures"] = total_cols
                attr_mapping = []
                for data in list_of_obj[index].value["transformation_mapping"]:
                    mapp = dict()
                    mapp["expression"] = '\"'+f"{data['expression'].split('.')[1]}"+'\"'
                    mapp["target"] = data["name"]
                    attr_mapping += [mapp]
                graph["processes"][process_name]["metadata"]["config"]["attributeMappings"] = attr_mapping"""
table_producer_setup_code = """if not list_of_obj[index].value["is_lookup_used"]:
                graph["processes"][process_name]["metadata"]["config"]["service"] = value["database_type"]
                graph["processes"][process_name]["metadata"]["config"]["source"]["remoteObjectReference"]["name"] = value["table_name"].split(".")[1].replace('"',"")
                graph["processes"][process_name]["metadata"]["config"]["source"]["remoteObjectReference"]["qualifiedName"] = value["qualified_name"]
                graph["processes"][process_name]["metadata"]["config"]["source"]["remoteObjectReference"]["nativeQualifiedName"] = value["nativeQualifiedName"]
                graph["processes"][process_name]["metadata"]["config"]["source"]["remoteObjectReference"]["owner"] = value["sql_server_database"]
                total_cols = list()
                for col in value["columns"]:
                    temp_col = {}
                    temp_col["name"] = col["name"]
                    temp_col["nativeDatatype"] = col["type"]
                    nativeDatatype = col["type"]
                    if nativeDatatype.lower().find("char") != -1:
                        temp_col["datatype"] = "STRING"
                        temp_col["templateType"] = "string"
                        temp_col["Length"] = col["size"]
                        temp_col["nativeLength"] = col["size"]
                    elif nativeDatatype.lower().find("int") != -1:
                        temp_col["datatype"] = "INTEGER"
                        temp_col["templateType"] = "int32"
                        temp_col["Length"] = 8
                        temp_col["nativeLength"] = 10
                    elif nativeDatatype.lower().find("double") != -1:
                        temp_col["datatype"] = "FLOATING"
                        temp_col["templateType"] = "float64"
                        temp_col["Length"] = 8
                        temp_col["nativeLength"] = 15
                    # elif nativeDatatype.find("false") != -1 or nativeDatatype.find("true") != -1 or nativeDatatype.find("True")!= -1 or nativeDatatype.find("False")!= -1 or nativeDatatype.find(True)!= -1 or nativeDatatype.find(False)!= -1:
                    #     dtype = "boolean"
                    # elif nativeDatatype
                    total_cols += [temp_col]
                graph["processes"][process_name]["metadata"]["config"]["source"]["schema"]["tableBasedRepresentation"]["attribures"] = total_cols
                attr_mapping = []
                for data in list_of_obj[index].value["transformation_mapping"]:
                    mapp = dict()
                    mapp["expression"] = '\"'+f"{data['expression'].split('.')[1]}"+'\"'
                    mapp["target"] = data["name"]
                    attr_mapping += [mapp]
                graph["processes"][process_name]["metadata"]["config"]["attributeMappings"] = attr_mapping"""
table_consumer_setup_code = """
			graph["processes"][process_name]["metadata"]["config"]["service"] = value["database_type"]
            # graph["processes"][process_name]["metadata"]["config"]["serviceConnection"]["connectionID"] = value["connectionID"]
            graph["processes"][process_name]["metadata"]["config"]["source"]["remoteObjectReference"]["name"] = value["table_name"].split(".")[1].replace('"',"")
            graph["processes"][process_name]["metadata"]["config"]["source"]["remoteObjectReference"]["qualifiedName"] = value["qualified_name"]
            graph["processes"][process_name]["metadata"]["config"]["source"]["remoteObjectReference"]["nativeQualifiedName"] = value["nativeQualifiedName"]
            graph["processes"][process_name]["metadata"]["config"]["source"]["remoteObjectReference"]["owner"] = value["sql_server_database"]"""
operator_setup_code = {"table_consumer":"", "table_producer":table_producer_setup_code, "file_consumer":file_consumer_setup_code, "graph_terminator":""}
# if you are using the di query (currently assuming merging and join and mapping)
# The send the which function you are going to use and if join which type of join and which table is left and which table is right
# If mapping I'll use table producer so i'll utilize its functionality there.
# if merging and join then i'll use the data transform operator


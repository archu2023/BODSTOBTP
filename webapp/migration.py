from adapter import operators_jsons
from OperatorLookup import lookup_information
from json import dumps
from os import getcwd, makedirs, umask, chmod, rmdir
import stat
import tarfile
from os.path import basename, split as spl
import sys


# The below s_cat_ports are containing static category ports (The operators which having static category ports are consider under this category)
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


def name_generator(sop:list)->list:
    """
    name_generator :
    =============
    This function is used to generate the unique process name with alphanumerical symbols
    Parameters
    ----------
    sop : list
        Sequence of operations in order/inorder. It should be a list of strings 
        representing process names.

            For example:

               + ["table_producer", "table_consumer"],

               
               + ["read_table", "write_table"]
 
    Returns
    -------
    unique_process_names : list
        The unique process name generated based on the provided sequence of operations.
    
    Example
    -------
    >>> name_generator(sop=["read_hana_table", "write_hana_table"])
    ["readhanatable1", "writehanatable1"]
    """

    unique_process_names = []
    explicit_counter = 0
    process_counter = {}
    conter = 0
    # if is_graph_terminator_needed:
    #     sop += ["graph_terminator"]
    for process in sop:
        if process in process_counter.keys():
            process_counter[f"{process}".replace("_","")] += 1
        else:
            process_counter[f"{process}".replace("_","")] = 1
        process_name = f"{process.replace('_','')}{process_counter[process.replace('_','')]}"
        if process_name in unique_process_names:
            process_name = f"{process_name}{explicit_counter}"
            explicit_counter += 1
        unique_process_names += [process_name]
    return unique_process_names

def link_creator(source:str, target:str, src_process_name:str, tgt_process_name:str)->dict:
    """
    link_creator :
    =============
    This function creates links with source process name and target process name and ports will be taken
    from the static category ports dictionary (`s_cat_ports`)
    ...

    Parmeters :
    -----------
    source : str
        Name of the source operator to retrive the output port. 
        .. currently accepting few operators which having single output port
        .. ports are retriving from the s_cat_ports dictionry
        
    target : str
        Name of the target operator to retrive the input port.
        .. currently accepting few operators which having single input port
        .. ports are retriving from the s_cat_ports dictionary

    src_process_name : str
        Name of the source process name to create link

    tgt_process_name : str
        Name of the target process name to create link

    returns
    -------
    dict
        A dictionary which is supported by sap di graph, which containing details of process which are need to connect together.
        It'll also contains port names of the source operator and target operator which need to connect together.
        .. For every link there'll be a source and target they are building based on previous links, each link'll be independent by it's process name and port names 
    ...
    Example
    -------
    >>> link_creator(source="read_table", target="write_table", src_process_name="readhanatable1", tgt_process_name="writehanatable1")
    {"src":{"port" : "success", "process" : "readhanatable1"}, 
    "tgt": {"port" : "input", "process" : "writehanatable1"}}
    """

    # if source == "read_file" and target == "sap_hana_client":
    multi_port_targets = ["sap_hana_client", "file_to_message_converter"]
    # if target not in multi_port_targets:
    source_ports = (s_cat_ports[source]["output"])
    if len(list(source_ports[0].keys())) <= 2:
        for port in source_ports:
            if port["name"] != "error":
                src = port["name"]
                break
        else:
            raise "Port Error"
        if target not in multi_port_targets:
            target_ports = (s_cat_ports[target]["input"])
            for port in target_ports:
                tgt = port["name"]
                break
            else:
                raise "Port Error"
    return ({"src":{"port" : src, "process" : src_process_name},
           "tgt" : {"port" : tgt, "process" : tgt_process_name}})

def make_tarfile(output_filename, source_dir):
    """
    make_tarfile
    ===========
    Create a tar file from the contents of the source directory.

    Parameters
    ----------
    output_filename : str
        The name of the output tar file, including the ".tgz" extension.

    source_dir : str
        The path to the source directory containing the files to be included in the tar file.

    Returns
    -------
    bool
        True if the tar file creation is successful, otherwise False.

    Notes
    -----
    This function takes a source directory and creates a tar file in gzip compressed format (.tgz) 
    with the contents of the specified source directory.

    The `output_filename` should include the ".tgz" extension to indicate the tar file format.

    The `source_dir` parameter should be the full path to the directory containing the files 
    that need to be included in the tar file.

    Example
    -------
    >>> make_tarfile(output_filename="example.tgz", source_dir="/path/to/source_directory")
    True
    """
    chmod(source_dir, stat.S_IRWXO)
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=basename(source_dir))
        return True

def v_type_creation(operator, process_name, obj):
    """
    v_type_creation(operator, process_name, obj)
    ============================================

    Generate V-Types for table consumer and file consumer operators.

    This function generates V-Types for the table consumer and file consumer operators based on the
    provided operator, process_name, and configuration parameters in the `obj` dictionary.

    Parameters
    ----------
    operator : str
        The type of operator for which V-Types are being generated. It must be either "table_consumer"
        or "file_consumer".

    process_name : str
        The name of the current process, used for creating V-Type names.

    obj : dict
        A dictionary containing the configuration parameters for the table consumer or file consumer
        operator. It includes information about the columns and their data types.

    Returns
    -------
    list
        A list of dictionaries, each representing a V-Type for the table consumer or file consumer
        operator.

    list
        A list of strings, each representing the folder name for scalar data types created during V-Type generation.

    list
        A list of dictionaries, each representing a scalar data type used in the V-Types.

    Notes
    -----
    The function generates V-Types for table consumer and file consumer operators based on the configuration
    parameters in the `obj` dictionary. Each V-Type represents a row in the table with components corresponding
    to the columns and their data types.

    For columns with specific data types (e.g., char, int, double, float, decimal, bool, date, time, timestamp),
    scalar data types are created and added to the `scalar_dtypes` list. The `scalar_dtypes_folder_names` list
    stores the folder names for the scalar data types to avoid duplicates.

    The V-Types are generated as dictionaries containing information such as name, description, vflow type,
    and component details. The generated V-Types are appended to the `table_vtype` list.

    The function returns the list of generated V-Types (`table_vtype`), the list of folder names for scalar data types
    (`scalar_dtypes_folder_names`), and the list of scalar data types (`scalar_dtypes`) used in the V-Types.

    Example
    -------
    >>> config_params = {
    ...     "columns": [
    ...         {"name": "ID", "type": "int"},
    ...         {"name": "Name", "type": "char(50)"},
    ...         {"name": "Amount", "type": "double"},
    ...     ]
    ... }
    >>> operator_type = "table_consumer"
    >>> current_process = "tableconsumer1"
    >>> vtypes, folder_names, scalars = v_type_creation(operator_type, current_process, config_params)
    >>> print(vtypes)
    [{'name': 'generated.Process_A_outTable', 'description': 'auto-generated generated.tableconsumer1_outTable', ...}]
    >>> print(folder_names)
    ['string_50']
    >>> print(scalars)
    [{'name': 'generated.string_50', 'description': 'String(50)', 'vflow.type': 'scalar', ...}]

    """
    scalar_dtypes_folder_names = []
    table_vtype = []
    scalar_dtypes = []
    if operator == "table_consumer" or operator == "file_consumer" :
        process_table_vtype = {}
        process_table_vtype["name"] = "generated.%s_outTable" %process_name
        process_table_vtype["description"] = "auto-generated %s" %process_table_vtype["name"]
        process_table_vtype["vflow.type"] = "table"
        process_table_vtype["rows"] = {"components":[]}

        for col in obj.value["columns"]:
            nativeDatatype = col["type"]
            
            if nativeDatatype.lower().find("char") != -1:
                scalar_dtypes_tracing = [f"string_{col['size']}"]
            # checking the scalar created already or not to avoid duplicates
                if scalar_dtypes_tracing not in scalar_dtypes_folder_names:
                    scalar_dtypes_folder_names += scalar_dtypes_tracing
                    scalar = {}
                    scalar["name"] = f"generated.string_{col['size']}"
                    scalar["description"] = f"String({col['size']})"
                    scalar["vflow.type"] = "scalar"
                    scalar["template"] = "string"
                    scalar["value.length"] = int(col['size'])
                    scalar_dtypes += [scalar]
                component = {}
                component[f"{col['name']}"] = {
                    "vflow.type": "scalar",
                    "vtype-ID": f"$GRAPH.generated.string_{col['size']}"
                }
                process_table_vtype["rows"]["components"] += [component]
            elif nativeDatatype.lower().find("int") != -1:
                component = {}
                component[f"{col['name']}"] = {
                    "vflow.type": "scalar",
                    "vtype-ID": "com.sap.core.int64"
                }
                process_table_vtype["rows"]["components"] += [component]
            elif nativeDatatype.lower().find("double") != -1 or nativeDatatype.lower().find("float") != -1 or nativeDatatype.lower().find("decimal") != -1:
                component = {}
                component[f"{col['name']}"] = {
                    "vflow.type": "scalar",
                    "vtype-ID": "com.sap.core.float64"
                }
                process_table_vtype["rows"]["components"] += [component]
            elif nativeDatatype.lower().find("bool") != -1:
                component = {}
                component[f"{col['name']}"] = {
                    "vflow.type": "scalar",
                    "vtype-ID": "com.sap.core.bool"
                }
                process_table_vtype["rows"]["components"] += [component]
            elif nativeDatatype.lower().find("date") != -1:
                component = {}
                component[f"{col['name']}"] = {
                    "vflow.type": "scalar",
                    "vtype-ID": "com.sap.core.date"
                }
                process_table_vtype["rows"]["components"] += [component]
            elif nativeDatatype.lower().find("time") != -1:
                component = {}
                component[f"{col['name']}"] = {
                    "vflow.type": "scalar",
                    "vtype-ID": "com.sap.core.time"
                }
                process_table_vtype["rows"]["components"] += [component]
            elif nativeDatatype.lower().find("timestamp") != -1:
                component = {}
                component[f"{col['name']}"] = {
                    "vflow.type": "scalar",
                    "vtype-ID": "com.sap.core.timestamp"
                }
                process_table_vtype["rows"]["components"] += [component]
        else:
            table_vtype += [process_table_vtype]
        return table_vtype, scalar_dtypes_folder_names, scalar_dtypes

def nativeQualifiedName_owner_qualifiedName(obj):
    """
    nativeQualifiedName_owner_qualifiedName
    =======================================

    Extract owner, nativeQualifiedName, and qualifiedName from the provided object.

    This function takes an object containing a qualified name and extracts the owner, nativeQualifiedName,
    and qualifiedName from it.

    Parameters
    ----------
    obj : dict
        A dictionary containing the qualified name information.

    Returns
    -------
    owner : str
        The owner of the qualified name.

    nativeQualifiedName : str
        The native qualified name, with the owner enclosed in double quotes.

    qualifiedName : str
        The qualified name with URL-encoded characters.

    Example
    -------
    >>> qualified_name_info = {"qualified_name": "/owner_name/table_name"}
    >>> owner, native_qualified_name, qualified_name = nativeQualifiedName_owner_qualifiedName(qualified_name_info)
    >>> print(owner)
    "OWNER_NAME"
    >>> print(native_qualified_name)
    "\"OWNER_NAME\".\"table_name\""
    >>> print(qualified_name)
    "/OWNER_NAME/table_name"

    Notes
    -----
    The function extracts the owner from the provided qualified name by splitting the qualified name string.
    It then constructs the native qualified name by enclosing the owner in double quotes and concatenating it with the
    table name. The function also encodes special characters in the qualified name with the url encoders, if any, using the `url_encoders`
    dictionary. (Currently only few url encoders are added)

    Warning
    -------
    The function assumes a specific format for the qualified name (/schemaName/tableName) which is sent by the program 1,
     where the owner and table name are separated by slashes.
    If the provided object does not follow this format, the function may raise an exception or return incorrect results.
    """
    owner = obj.value["qualified_name"].split("/")[1].upper()
    nativeQualifiedName = "\"" + owner + "\"." + "\"" + obj.value["qualified_name"].split("/")[2] + "\""
    url_encoders = {"$":"%24", "!":"%21", "#":"%23","%":"%25", "\"":"%22", "&": "%26"}
    qualifiedName = obj.value["qualified_name"]
    qualifiedName = "/" + owner + "/" + qualifiedName.split("/")[2]
    for char in obj.value["qualified_name"]:
        if char in url_encoders.keys():
            qualifiedName = qualifiedName.replace(char, url_encoders[char])
    return owner, nativeQualifiedName, qualifiedName

def table_producer_code_exec(lookup_used, obj,index, list_of_obj, src_inports):
    """
    table_producer_code_exec(lookup_used, obj, index, list_of_obj, src_inports)
    ==============================================================================

    Generate operator JSON for the table producer based on the provided configuration.

    This function generates the operator JSON for the table producer based on the provided
    configuration parameters. The table producer is used to produce a table based on the
    transformation mapping and configuration details specified in the `obj` dictionary.

    Parameters
    ----------
    lookup_used : bool
        A flag indicating whether lookup logic is used. If True, the function raises a NotImplementedError.

    obj : dict
        A dictionary containing the configuration parameters for the table producer operator.
        It includes information about the database type, table name, and columns.

    index : int
        The index of the current table producer in the list_of_obj.

    list_of_obj : list
        A list of objects containing transformation mapping details for each operator.

    src_inports : list
        A list of source inport vtype-IDs to be mapped to the table producer.

    Returns
    -------
    dict
        The operator JSON for the table producer containing the configuration details.

    Raises
    ------
    NotImplementedError
        If the lookup logic is used, the function raises a NotImplementedError as it is not implemented yet.

    Example
    -------
    >>> config_params = {
    ...     "database_type": "HANA_DB",
    ...     "table_name": "SCHEMA_NAME.TABLE_NAME",
    ...     "columns": [
    ...         {"name": "ID", "type": "int"},
    ...         {"name": "Name", "type": "char(50)"},
    ...         {"name": "Amount", "type": "double"},
    ...     ]
    ... }
    >>> lookup_used_flag = False
    >>> index_of_producer = 0
    >>> transformations_list = [...]
    >>> source_inports_list = [...]
    >>> operator_json = table_producer_code_exec(lookup_used_flag, config_params, index_of_producer, transformations_list, source_inports_list)
    >>> print(operator_json)
    { ... }  # The generated operator JSON for the table producer.

    Notes
    -----
    The function generates the operator JSON for the table producer based on the provided configuration
    parameters. It sets the appropriate service, table name, attributes, and attribute mappings in the
    operator JSON. The function also sets the mode to "append" for table producers.

    If the lookup logic is used (i.e., lookup_used is True), the function raises a NotImplementedError,
    indicating that the lookup logic is not implemented yet.
    """

    operator_json = operators_jsons["table_producer"]
    if not lookup_used:
        operator_json["metadata"]["config"]["service"] = obj.value["database_type"]
        operator_json["metadata"]["config"]["source"]["remoteObjectReference"]["name"] = obj.value["table_name"].split(".")[1].replace("\"","")

        total_cols = list()
        # creating table attributes for table producer
        attr_mapping = []
        autogenkey_cols = []
        for data in list_of_obj[index].value["transformation_mapping"]:
            mapp = dict()
            if data["expression"].find("key_generation") ==-1:
                mapp["expression"] = '\"'+f"{data['expression'].split('.')[1]}"+'\"'
                mapp["target"] = data["name"]
                attr_mapping += [mapp]
            else:
                autogenkey_cols += [data["name"]]
        for col in obj.value["columns"]:
            if col["name"] in autogenkey_cols:
                continue
            temp_col = {}
            temp_col["name"] = col["name"]
            temp_col["nativeDatatype"] = col["type"]
            nativeDatatype = col["type"]
            if nativeDatatype.lower().find("char") != -1:
                temp_col["datatype"] = "STRING"
                temp_col["templateType"] = "string"
                temp_col["length"] = col["size"]
                temp_col["nativeLength"] = col["size"]
            elif nativeDatatype.lower().find("int") != -1:
                temp_col["datatype"] = "INTEGER"
                temp_col["templateType"] = "int32"
                temp_col["length"] = 8
                temp_col["nativeLength"] = 10
            elif nativeDatatype.lower().find("double") != -1 or nativeDatatype.lower().find("float") != -1 or nativeDatatype.lower().find("decimal") != -1:
                temp_col["datatype"] = "FLOATING"
                temp_col["templateType"] = "float64"
                temp_col["length"] = 8
                temp_col["nativeLength"] = 15
            total_cols += [temp_col]
        operator_json["metadata"]["config"]["source"]["schema"]["tableBasedRepresentation"]["attributes"] = total_cols
        # mapping inports of table consumer to table producer
        for port in operator_json["metadata"]["inports"]:
            port["vtype-ID"] = src_inports[0]#port["vtype-ID"].replace("process_name", process_names[index-1])
        operator_json["metadata"]["config"]["attributeMappings"] = attr_mapping
        operator_json["metadata"]["config"]["mode"] = "append"
        owner, nativeQualifiedName, qualifiedName = nativeQualifiedName_owner_qualifiedName(obj)
        operator_json["metadata"]["config"]["source"]["remoteObjectReference"]["qualifiedName"] = qualifiedName
        operator_json["metadata"]["config"]["source"]["remoteObjectReference"]["nativeQualifiedName"] = nativeQualifiedName
        operator_json["metadata"]["config"]["source"]["remoteObjectReference"]["owner"] = owner

        ## this code is added as per the discussion of the lingesh to make sure the graph running properly
        operator_json["metadata"]["config"]["service"] = "HANA_DB"
        operator_json["metadata"]["config"]["serviceConnection"]["connectionID"] = "HANADB_02"
        operator_json["metadata"]["config"]["source"]["remoteObjectReference"]["connection"] = {"id":"HANADB_02", "type":"HANA_DB"}
        return operator_json

    else:
        # raise  Exception("Lookup logic is not implemented yet")
        raise NotImplementedError("Lookup logic is not implemented yet")

def file_consumer_code_exec(obj, process_name):
    """
    file_consumer_code_exec
    =======================
    This function will retrive the default operator json from the adapter module and modify the configuration 
    of the file consumer operator and collect outport vtype-IDs for table producer operator

    This function takes an object containing the configuration parameters for the file consumer operator
    and the name of the current process. It modifies the provided operator JSON to set the appropriate
    values for the operator's configuration based on the object's attributes.

    Parameters
    ----------
    obj : dict
        A dictionary containing the configuration parameters for the file consumer operator.

    process_name : str
        The name of the current process, used for modifying the port vtype-IDs.

    Returns
    -------
    dict
        The modified operator JSON containing the updated configuration values.

    list
        A list of source inport vtype-IDs after the modifications.

    Notes
    -----
    The function modifies the provided operator JSON by updating the metadata configuration for the file
    consumer operator. It sets the service connection ID, file name, qualified name, native qualified name,
    and remote object type based on the values in the provided `obj["values"]` dictionary.

    The function also modifies the vtype-IDs of the outports in the operator JSON by replacing "process_name"
    with the actual `process_name` provided as an argument.

    Additionally, the function sets the `remoteObjectType` based on the file extension (csv or json) in the
    provided `obj` dictionary.

    .. HardCoded Details ::
        Temporary code is added as per the discussion with Lingesh to ensure proper graph execution in SAP DI.
        The function sets the service to "SDL" and the connectionID to "DI_DATA_LAKE" in the operator JSON.

    Example
    -------
    >>> config_params = {"connectionID": "FILE_CONN_01", "file_name": "data.csv", "file_location": "/files"}
    >>> current_process = "Process_A"
    >>> operator_json, src_inports = file_consumer_code_exec(config_params, current_process)
    >>> print(operator_json)
    { ... }  # The modified operator JSON with updated configuration values
    >>> print(src_inports)
    ['Process_A-outport1', 'Process_A-outport2']
    """
    src_inports = []
    operator_json = operators_jsons["file_consumer"] 
    operator_json["metadata"]["config"]["serviceConnection"]["connectionID"] = obj.value["connectionID"]
    operator_json["metadata"]["config"]["source"]["remoteObjectReference"]["name"] = obj.value["file_name"]
    operator_json["metadata"]["config"]["source"]["remoteObjectReference"]["qualifiedName"] = "/shared/SAP_DEMO" + f"{obj.value['file_location']}/" + obj.value["file_name"]
    operator_json["metadata"]["config"]["source"]["remoteObjectReference"]["nativeQualifiedName"] = "/shared/SAP_DEMO" + f"{obj.value['file_location']}/" + obj.value["file_name"]
    for port in operator_json["metadata"]["outports"]:
        port["vtype-ID"] = port["vtype-ID"].replace("process_name", process_name)
        src_inports += [port["vtype-ID"]]
    if obj.value["file_name"].split(".")[1].lower()=="csv":
        operator_json["metadata"]["config"]["source"]["remoteObjectReference"]["remoteObjectType"] = "FILE.CSV"
    elif obj.value["file_name"].split(".")[1].lower()=="json":
        operator_json["metadata"]["config"]["source"]["remoteObjectReference"]["remoteObjectType"] = "FILE.JSON"
    # This block of code is adding for temporary purpose as discussed with lingesh to run graph successfully
    operator_json["metadata"]["config"]["service"] = "SDL"
    operator_json["metadata"]["config"]["serviceConnection"]["connectionID"] = "DI_DATA_LAKE"
    operator_json["metadata"]["config"]["source"]["remoteObjectReference"]["connection"] = {"id":"DI_DATA_LAKE", "type":"SDL"}

    return operator_json, src_inports



def table_consumer_code_exec(obj, process_name):
    """
    table_consumer_code_exec
    ========================
    Fill the values for the table consumer operator to configure its behavior.

    This function takes an object containing the configuration parameters for the table consumer operator
    and the name of the current process. It modifies the provided operator JSON to set the appropriate
    values for the operator's configuration.

    Parameters
    ----------
    obj : dict
        A dictionary containing the configuration parameters for the table consumer operator.

    process_name : str
        The name of the current process, used for modifying the port vtype-IDs.

    Returns
    -------
    list
        A list of source inport vtype-IDs after the modifications.

    dict
        The modified operator JSON containing the updated configuration values.

    Notes
    -----
    The function modifies the provided operator JSON by updating the metadata configuration for the table
    consumer operator. It sets the service type, remote object reference name, qualified name, native qualified name,
    and owner based on the values in the provided `obj` dictionary.

    The function also modifies the vtype-IDs of the outports in the operator JSON by replacing "process_name"
    with the actual `process_name` provided as an argument.

    Additionally, the function adds extra code as per the discussion with Lingesh to ensure proper graph execution.
    It sets the service to "HANA_DB" and sets the connectionID to "HANADB_02" in the operator JSON.

    Example
    -------
    >>> config_params = {"database_type": "Mysql", "table_name": "\"schema_name\".\"table_name\""}
    >>> current_process = "tableconsumer1"
    >>> src_inports, operator_json = table_consumer_code_exec(config_params, current_process)
    >>> print(src_inports)
    ['tableconsumer1_out', 'Process_A-outport2']
    >>> print(operator_json)
    { ... }  # The modified operator JSON with updated configuration values
    """
    src_inports = []
    operator_json = operators_jsons["table_consumer"]
    operator_json["metadata"]["config"]["service"] = obj.value["database_type"]
    operator_json["metadata"]["config"]["source"]["remoteObjectReference"]["name"] = obj.value["table_name"].split(".")[1].replace("\"","")
    owner, nativeQualifiedName, qualifiedName = nativeQualifiedName_owner_qualifiedName(obj)
    operator_json["metadata"]["config"]["source"]["remoteObjectReference"]["qualifiedName"] = qualifiedName
    operator_json["metadata"]["config"]["source"]["remoteObjectReference"]["nativeQualifiedName"] = nativeQualifiedName
    operator_json["metadata"]["config"]["source"]["remoteObjectReference"]["owner"] = owner

    for port in operator_json["metadata"]["outports"]:
        port["vtype-ID"] = port["vtype-ID"].replace("process_name", process_name)
        src_inports += [port["vtype-ID"]]

    ## this code is added as per the discussion of the lingesh to make sure the graph running properly
    operator_json["metadata"]["config"]["service"] = "HANA_DB"
    operator_json["metadata"]["config"]["serviceConnection"]["connectionID"] = "HANADB_02"
    operator_json["metadata"]["config"]["source"]["remoteObjectReference"]["connection"] = {"id":"HANADB_02", "type":"HANA_DB"}
    return src_inports, operator_json

def write_graph(FILE_PATH, File_name, graph):
    """
    write_graph
    ===========

    Write the graph data (dictonary) to a JSON file.

    This function takes the graph data in JSON format and writes it to a JSON file in the specified
    FILE_PATH with the given File_name.

    Parameters
    ----------
    FILE_PATH : str
        The path where the JSON file will be saved.

    File_name : str
        The name of the JSON file (without the '.json' extension) to be created.

    graph : str
        The graph data in JSON format to be written to the file.

    Returns
    -------
    bool
        Returns True if the graph data is successfully written to the file.

    Example
    -------
    >>> graph_data = {"description":"bods2di", "processes":{"tableconsumer1":{"key1":value1}}, {"tableproducer1":{"key2":"value2"}}}
    >>> file_path = '/path/to/folder'
    >>> file_name = 'my_graph'
    >>> write_graph(file_path, file_name, graph_data)
    True

    Notes
    -----
    - The function writes the graph data provided as a string in JSON format to a file.
    - The JSON file will be created in the specified FILE_PATH with the provided File_name.
    - If a file with the same name already exists, it will be overwritten.
    - The function returns True if the writing process is successful; otherwise, it may raise an exception.

    Warning
    -------
    - Please ensure that the FILE_PATH is a valid directory where the script has write permissions.
    - The function will overwrite any existing file with the same File_name in the specified FILE_PATH.
    - The graph data should be a valid JSON string; otherwise, the resulting file may be corrupted.
    """
    graph_writer = open(f"{FILE_PATH}/{File_name+'.json'}" , "w")
    graph_writer.write(dumps(graph, indent=4))
    return True

def folderWithJsonAndVtypes(FILE_PATH:str, File_name:str, scalar_dtypes_folder_names, src_process_names, scalar_dtypes,
                            table_vtype, graph)->bool:
    """
    .. function:: folderWithJsonAndVtypes(FILE_PATH, File_name, scalar_dtypes_folder_names, src_process_names, scalar_dtypes, table_vtype, graph)

   folderWithJsonAndVtypes :
   =======================
   Creates a folder structure with JSON and VTypes files based on the provided parameters.

   This function generates a folder structure and writes JSON and VTypes files into it
   based on the given parameters. It is designed to organize and store data for
   scalar data types and table VTypes, as well as a graph in JSON format.

   Parameters :
   -----------
   :param FILE_PATH: The path where the folder structure will be created.
   :type FILE_PATH: str
   :param File_name: The name of the top-level folder to be created within FILE_PATH.
   :type File_name: str
   :param scalar_dtypes_folder_names: A list of subfolder names for scalar data types.
   :type scalar_dtypes_folder_names: list of str
   :param src_process_names: A list of subfolder names for table VTypes.
   :type src_process_names: list of str
   :param scalar_dtypes: A list of dictionaries, each containing scalar data type information.
   :type scalar_dtypes: list of dict
   :param table_vtype: A list of dictionaries, each containing table VType information.
   :type table_vtype: list of dict
   :param graph: A dictionary containing graph data in JSON format.
   :type graph: dict
   :returns: True if the folder structure and files are created successfully, otherwise False.
   :rtype: bool


   .. From given Path::
        The function creates a folder structure with the following hierarchy:

        FILE_PATH /
            └── File_name /
                    ├── vtypes /
                    │       └── scalars /
                    │              └── generated /
                    │                     └── [scalar_dtypes_folder_names]
                    │                             └── scalar.vtype
                    │       └── tables /
                    │              └── generated /
                    │                     └── [src_process_names]
                    │                             └── table.vtype
                    ├── graph.json

   Each scalar data type folder (scalar_dtypes_folder_names) contains a "scalar.vtype" file,
   and each table VType folder (src_process_names) contains a "table.vtype" file. The graph data
   is stored in a "graph.json" file at the top-level folder.

   Returns
   -------
   Bool
        If the Folder created successfully then it'll returns True else False
    """
    try:
        scalars_subfolder = "vtypes/scalars/generated"
        tables_subfolder = "vtypes/tables/generated"
        access = 0o777
        umask(7)
        makedirs(name=f"{FILE_PATH}/{File_name}", exist_ok=True, mode=access)
        makedirs(name=f"{FILE_PATH}/{File_name}/{scalars_subfolder}", exist_ok=True, mode=access)
        for index, folder in enumerate(scalar_dtypes_folder_names):
            # creating folder for every string data type with respect to their size
            makedirs(name=f"{FILE_PATH}/{File_name}/{scalars_subfolder}/{folder}", exist_ok=True,mode=access)
            open(f"{FILE_PATH}/{File_name}/{scalars_subfolder}/{folder}/scalar.vtype","w").write(dumps(scalar_dtypes[index], indent=4))
        makedirs(name=f"{FILE_PATH}/{File_name}/{tables_subfolder}", exist_ok=True, mode=access)
        for index, folder in enumerate(src_process_names):
            makedirs(name=f"{FILE_PATH}/{File_name}/{tables_subfolder}/{folder}", exist_ok=True, mode=access)
            open(f"{FILE_PATH}/{File_name}/{tables_subfolder}/{folder}/table.vtype","w").write(dumps(table_vtype[index], indent=4))
        write_graph(f"{FILE_PATH}/{File_name}", "graph", graph)
        return True
    except:
        return False


def graph_creation(transformation_mapping:dict, list_of_obj:list, description="BODS2DI", is_graph_terminator_needed=True, FILE_PATH=getcwd(), File_name=None):
    """
    graph_creation
    =============
    Create a graph (dictionary) with transformation mapping, v-types, and scalars.This function also create a `tar file` and a Folder with the `graph.json` and required
    scalars, vtypes in the given location which is needed to run the graph in SAP DI.


    Parameters
    ----------
    transformation_mapping : dict
        A dictionary containing operators in order for creating the graph.

    list_of_obj : list
        A list containing values of each operator for creating the graph.

    description : str, optional
        Description of the graph. Default is "BODS2DI".

    is_graph_terminator_needed : bool, optional
        Indicates whether a graph terminator is needed. Default is True.

    FILE_PATH : str, optional
        The path where the graph files will be stored. Default is the current working directory.

    File_name : str
        The name of the graph file and the folder.

    Returns
    -------
    str
        A message indicating the result of the graph creation. If successful, returns "Success";
        otherwise, it raises an exception with details.

    Raises
    ------
    AssertionError
        If FILE_name argument is not received the assertion error will be raised
        
    InterruptedError
        Raised when there is an error in creating the tar file.

    NotImplementedError
        Raised when the lookup logic is not implemented yet.

    Notes
    -----
    This function generates a graph with details of processes and their connections based on the provided transformation mapping.
    It creates v-types and scalars required for the graph to run.

    The folder and .tgz file containing the graph, scalars, and v-types will be saved to the specified FILE_PATH.

    Example
    -------
    >>> graph_creation(transformation_mapping=transformation_mapping_data, list_of_obj=operators_data)
    'Success'

    Warning
    -------
    The function assumes that the transformation_mapping and list_of_obj are provided correctly and
    in the correct order. Incorrect inputs may lead to unexpected graph generation or errors.

    See Also (Sub functions in sequential execution order)
    --------
    name_generator : Function that generates unique process names for each operator.
    v_type_creation : Function that creates scalar data types and table v-types for the graph.
    file_consumer_code_exec : Function that generates operator JSON for the file consumer.
    table_consumer_code_exec : Function that generates operator JSON for the table consumer.
    table_producer_code_exec : Function that generates operator JSON for the table producer.
    link_creator : Function that creates connections (links) between two operators.
    """
    if File_name==None:
        raise AssertionError("File name is not received") 
    try:
        graph = dict()
        graph["description"] = description
        graph["processes"] = dict()
        graph["connections"] = list()
        operators = list(transformation_mapping.values())
        if is_graph_terminator_needed:
            operators += ["graph_terminator"]
        process_names = name_generator(operators)
        # If structured operators used then output need to be .tgz file else .json file
        structured_operators_used = False
        structured_operators = ["table_consumer", "file_consumer", "file_producer", "table_producer", "data_transform"]
        for operator in operators:
            if operator in structured_operators:
                structured_operators_used = True
                break
                
        scalar_dtypes_folder_names = []
        scalar_dtypes = []
        src_process_names = []
        table_vtype = []
        src_inports = []
        # the below are the path in the tarfile, which holding data types
        for index,operator in enumerate(operators):
            if operator == "table_producer":
                obj = list_of_obj[index+1]
            else:
                obj = list_of_obj[index]
            process_name = process_names[index]
            graph["processes"][process_name] = operators_jsons[operator]

            # creating scalar data types for string dtypes for vtype folder
            

            if operator == "file_consumer":
                vtype_data = v_type_creation(operator, process_name, obj)
                table_vtype += vtype_data[0]
                scalar_dtypes_folder_names += vtype_data[1]
                scalar_dtypes += vtype_data[2]
                # graph["processes"][process_name]["metadata"]["config"]["service"] = "SDL"
                src_process_names += [process_name+"_outTable"]
                operator_updated_json = file_consumer_code_exec(obj, process_name)
                src_inports += operator_updated_json[0]
                graph["processes"][process_name] = operator_updated_json[1]
                
                
            elif operator == "table_producer":
                operator_updated_json = table_producer_code_exec(list_of_obj[index].value["is_lookup_used"], obj,index, list_of_obj, src_inports)
                graph["processes"][process_name] = operator_updated_json



            elif operator == "table_consumer":
                # src_process_names = []
                vtype_data = v_type_creation(operator, process_name, obj)
                table_vtype += vtype_data[0]
                scalar_dtypes_folder_names += vtype_data[1]
                scalar_dtypes += vtype_data[2]
                src_process_names += [process_name+"_outTable"]
                operator_updated_json = table_consumer_code_exec(obj, process_name)
                src_inports += operator_updated_json[0]
                graph["processes"][process_name] = operator_updated_json[1]

            elif operator == "read_file":
                graph["processes"][process_name]["metadata"]["config"]["mode"] = "Once"
                graph["processes"][process_name]["metadata"]["config"]["path"] = obj.value["path"]
                
                # hardcoded values as per discussion with lingesh
                graph["processes"][process_name]["metadata"]["config"]["connection"]["connectionID"] = "DiDataLake"

            elif operator == "sap_hana_client":
                nativeQualifiedName =  nativeQualifiedName_owner_qualifiedName(obj)
                graph["processes"][process_name]["metadata"]["config"]["tableName"] = nativeQualifiedName[1]
                graph["processes"][process_name]["metadata"]["config"]["tableColumns"] = obj.value["columns"]
                graph["processes"][process_name]["metadata"]["config"]["tableColumns"] = "Ignore"

                # hardcoded values as per discussion with lingesh
                graph["processes"][process_name]["metadata"]["config"]["connection"]["connectionID"] = "HANADB_02"

            elif operator == "write_hana_table":
                nativeQualifiedName =  nativeQualifiedName_owner_qualifiedName(obj)
                graph["processes"][process_name]["metadata"]["config"]["tableName"] = nativeQualifiedName[1]
            
                # hardcoded values as per discussion with lingesh
                graph["processes"][process_name]["metadata"]["config"]["connection"]["connectionID"] = "HANADB_02"

            elif operator == "read_hana_table":
                nativeQualifiedName =  nativeQualifiedName_owner_qualifiedName(obj)
                graph["processes"][process_name]["metadata"]["config"]["tableName"] = nativeQualifiedName[1]

                # hardcoded values as per discussion with lingesh
                graph["processes"][process_name]["metadata"]["config"]["connection"]["connectionID"] = "HANADB_02"

            # Between Two operators creating a link by considering first operator as source and second operator as target
            if index==0:
                continue
            else:
                link = link_creator(target=operator, source=operators[index-1],tgt_process_name=process_names[index], src_process_name=process_names[index-1])
                graph["connections"] += [link]
            # hardcoded_values = {"table_consumer":{"service":"HANA_DB", "connectionID":"HANADB_02"},
            # ["read_file", "structured_file_consumer"]:{"connection management"}}

        # creating the tgz file with graph.json and vtypes folder with all previlages to users (read, write and execute)
        if structured_operators_used:
            folder_creation_result = folderWithJsonAndVtypes(FILE_PATH, File_name, scalar_dtypes_folder_names, src_process_names, scalar_dtypes, table_vtype, graph)
            if folder_creation_result:
                final_result = make_tarfile("{}/{}.tgz".format(FILE_PATH,File_name), "{}/{}".format(FILE_PATH,File_name))
            else:
                raise ChildProcessError("Failed While Creating The Folder")
        else:
            final_result = write_graph(FILE_PATH, File_name, graph)

        if final_result:
            return "Success"
        else:
            raise ChildProcessError("Failed To Create Json")
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = spl(exc_tb.tb_frame.f_code.co_filename)[1]
        open(f"{FILE_PATH}/{File_name}.TXT", "w").write(f"Failed to Generate the json\nError occured in {fname}\nError : {e}\nError Type : {exc_type}, \nError reason : {exc_obj}, \nLine Number : {exc_tb.tb_lineno}")
        return "Failed"
    
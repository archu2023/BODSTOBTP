import pandas as pd

lookup_information = {
    'table_consumer':["service","connectionID","name","qualifiedName",
    "nativeQualifiedName","owner"],
    'table_producer':["service","connectionID","name","qualifiedName",
    "nativeQualifiedName","owner","attributes","attributeMappings","mode"],
    "file_consumer":["service","connectionID","_____name","qualifiedName",
    "nativeQualifiedName"],
    "graph_terminator":[]
}


operator_lookup = [
    {
        'BODS_OPERATOR':'DIFileSource',
        'DI_OPERATOR':'file_consumer',
        'LOOKUP':False
    },
    {
        'BODS_OPERATOR':'DIDatabaseTableTarget',
        'DI_OPERATOR':'table_producer',
        'LOOKUP':False
    },
    {
        'BODS_OPERATOR':'DIDatabaseTableSource',
        'DI_OPERATOR':'table_consumer',
        'LOOKUP':False
    },
    {
        'BODS_OPERATOR':'DIDatabaseTableTarget',
        'DI_OPERATOR':['table_producer','data_transform'],
        'LOOKUP':True
    }    
]

operator_lookup_df = pd.DataFrame(operator_lookup)
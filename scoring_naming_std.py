import re

# Defining naming conventions for different elements      Needs to be checked
naming_conventions = {
    "DIProject": re.compile(r'^PJ_[A-Za-z0-9_]+$'),
    "DIJob": re.compile(r'^JB_[a-zA-Z0-9_]+$'),
    "DIWorkflow": re.compile(r'^WF_[a-zA-Z0-9_]+$'),
    "DIDataflow": re.compile(r'^DF_[a-zA-Z0-9_]+$'),
    "Annotation": re.compile(r'^ANN_[a-zA-Z0-9_]+$'),
    "Catch": re.compile(r'^CATCH_[a-zA-Z0-9_]+$'),
    "Conditional": re.compile(r'^COND_[a-zA-Z0-9_]+$'),
    "DIDatabaseDatastore": re.compile(r'^DS_[a-zA-Z0-9_]+$'),
    "Document": re.compile(r'^DOC_[a-zA-Z0-9_]+$'),
    "DTD (Document Type Definition)": re.compile(r'^DTD_[a-zA-Z0-9_]+$'),
    "File Format": re.compile(r'^FF_[a-zA-Z0-9_]+$'),
    "Function": re.compile(r'^FUNC_[a-zA-Z0-9_]+$'),
    "DIScript": re.compile(r'^SC_[a-zA-Z0-9_]+$'),
    "Template Table": re.compile(r'^TT_[a-zA-Z0-9_]+$'),
    "Try": re.compile(r'^TRY_[a-zA-Z0-9_]+$'),
    "While Loop": re.compile(r'^While_[a-zA-Z0-9_]+$'),
    "XML Message": re.compile(r'^XMLMSG_[a-zA-Z0-9_]+$'),
    "XML Schema": re.compile(r'^XMLSCH_[a-zA-Z0-9_]+$'),
    "XML Template": re.compile(r'^XMLTMPL_[a-zA-Z0-9_]+$'),
    "Address_Enhancement": re.compile(r'^AE_[a-zA-Z0-9_]+$'),
    "Case_Operation": re.compile(r'^Case_[a-zA-Z0-9_]+$'),
    "Date_Generation": re.compile(r'^DG_[a-zA-Z0-9_]+$'),
    "Effective_Date": re.compile(r'^ED_[a-zA-Z0-9_]+$'),
    "Hierarchy_Flattening": re.compile(r'^HF_[a-zA-Z0-9_]+$'),
    "History_Preserving": re.compile(r'^HP_[a-zA-Z0-9_]+$'),
    "Key_Generation": re.compile(r'^KG_[a-zA-Z0-9_]+$'),
    "Map_CDC_Operation": re.compile(r'^MC_[a-zA-Z0-9_]+$'),
    "Map_Operation": re.compile(r'^MO_[a-zA-Z0-9_]+$'),
    "Match_Merge": re.compile(r'^MM_[a-zA-Z0-9_]+$'),
    "Merge": re.compile(r'^MER_[a-zA-Z0-9_]+$'),
    "Name_Parsing": re.compile(r'^NP_[a-zA-Z0-9_]+$'),
    "Pivot": re.compile(r'^PIV_[a-zA-Z0-9_]+$'),
    "Reverse_Pivot": re.compile(r'^RPIV_[a-zA-Z0-9_]+$'),
    "DIQuery": re.compile(r'^QRY_[a-zA-Z0-9_]+$'),
    "Row_Generation": re.compile(r'^RG_[a-zA-Z0-9_]+$'),
    "SQL": re.compile(r'^SQL_[a-zA-Z0-9_]+$'),
    "Table_Comparison": re.compile(r'^TC_[a-zA-Z0-9_]+$')
}

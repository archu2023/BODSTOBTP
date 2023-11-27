from driver import main_prog1
import os

data = open("csv_to_table_xml.xml","rb").read()

main_prog1(data, os.getcwd(),"csv_to_table_xml")
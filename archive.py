import lxml.etree
import zeep
import json
import os
import lxml

import utils.functions as helper_functions

wsdl = "https://api.ibb.gov.tr/iett/ibb/ibb360.asmx?wsdl"

translate_dict = {"ID": "Id", "NARSIVGOREVID": "Archive task ID", "NKAYITGUNU": "Action date", "SHATKODU": "Line code",
                  "SGUZERGAHKODU": "Route code", "SKAPINUMARA": "Door number", "DTBASLAMAZAMANI": "Mission start date", "DTBITISZAMANI": "Mission end date",
                  "SGOREVDURUM": "Mission status", "NGOREVID": "Mission ID", "DTPLANLANANBASLANGICZAMANI": "Planned mission start date", 
                  "DTDUZENLENENBASLANGICZAMANI": "Edited mission start date"}

def validate_date_input(date_input):
    if len(date_input) != 8 or date_input.isnumeric() == False:
        raise ValueError("Incorrect format (YYYYMMDD)")        
    return True

def soap_call(date):
    client = zeep.Client(wsdl=wsdl)

    response = client.service.GetIettArsivGorev_XML(date)
    
    if len(response) == 0:
        print("No data found")
        exit()

    return response
    
def parse_xml(body):
    output_buffer = []
    for table in body:
        if isinstance(table, lxml.etree._Element) == False:
            raise TypeError(f"Invalid type {type(table)} passed to parse_xml function")
        output_buffer.append(helper_functions.parse_and_translate_values_etree(translate_dict, table))

    return output_buffer

def get_specific_bus_line_data(table_list, bus_line_code):
    bus_line_data = []
    if bus_line_code == "":
        return table_list
    else:
        for table in table_list:
            if bus_line_code == table["Line code"]:
                bus_line_data.append(table)
    return bus_line_data

def main():
    try:
        date_input = input("Enter date: ")

        validate_date_input(date_input)

        response = soap_call(date_input)

        response_parsed = parse_xml(response)

        bus_line_input = helper_functions.special_char_upper_func(input("Enter line code (leave empty for all lines): "))

        specific_bus_line_data = get_specific_bus_line_data(response_parsed, bus_line_input)

        helper_functions.print_result(specific_bus_line_data)
    except ValueError as val_exc:
        print(f"ValueError exception: {val_exc}")  
    except TypeError as type_exc:
        print(f"TypeError exception: {type_exc}")  
if __name__ == "__main__":
    main()
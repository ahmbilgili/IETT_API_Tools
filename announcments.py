# Lists announcments for the given bus line

import zeep
import json
import os
import utils.functions

wsdl = "https://api.ibb.gov.tr/iett/UlasimDinamikVeri/Duyurular.asmx?wsdl"

translate_dict = {"HATKODU": "Line Code", "HAT": "Line", "TIP": "Type", "GUNCELLEME_SAATI": "Update Time", "MESAJ": "Message"}

def format_line_code(line_code_input):
    line_code = utils.functions.special_char_upper_func(line_code_input)
    return line_code

def soap_call():
    client = zeep.Client(wsdl=wsdl)
    announcments_response = client.service.GetDuyurular_json()

    if len(announcments_response) == 0:
        print("No announcments found!")
        exit()

    return announcments_response

def soap_response_to_list(soap_response):
    return json.loads(soap_response)

def get_specific_bus_lines_announcments(line_code, announcment_list):
    output_buffer = []
    for element in announcment_list:
        if line_code in element["HATKODU"]:
            output_buffer.append(utils.functions.parse_and_translate_values_dict(translate_dict, element))
    return output_buffer

def print_elements(outp_buffer):
    print()
    for list_element in outp_buffer: 
        for key, value in list_element.items():
            print(f"{key}: {value}")
        print()

def convert_list_tostr_announcments(announcment_list):
    out_string = ""
    for element in announcment_list:
        for key, value in element.items():
            out_string += f"{key}: {value}\n"
    return out_string + "\n"


def main():
    try:
        line_code = input("Enter line code (leave empty for all lines): ")
        format_line_code(line_code)
        announcments_response = soap_call()
        announcments_response_list = soap_response_to_list(announcments_response)
        specific_announcments = get_specific_bus_lines_announcments(line_code, announcments_response_list)
        print_elements(specific_announcments)

    except IndexError as index_exc:
        print("Index error when iterating/doing something a list:", index_exc)

if __name__ == "__main__": 
    main() 
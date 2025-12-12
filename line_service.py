# Displays general information about given bus line

import zeep
import json
import lxml.etree
import utils.functions as helper_functions

translate_dict = {"HAT_KODU": "Line code", "HAT_ADI": "Line name", "TAM_HAT_ADI": "Complete line name", "HAT_DURUMU": "Line status", "BOLGE": "Region", "SEFER_SURESI": "One-way trip time"}
wsdl = "xml/durak_hat_bilgi.xml"

def take_line_code(line_code_input):
    line_code = helper_functions.special_char_upper_func(line_code_input)
    return line_code

def soap_call(line_code):
    client = zeep.Client(wsdl=wsdl)
    line_service_response = client.service.HatServisi_GYY(line_code) # returns lxml.etree._Element

    if len(line_service_response) == 0:
        print("Bus line not found")
        exit()
    return line_service_response

def parse_etree(input_lxml_etree):
    outp_buffer = []
    for table in input_lxml_etree:
        outp_buffer.append(helper_functions.parse_and_translate_values_etree(translate_dict, table))
    return outp_buffer

def main():
    try:
        line_code = take_line_code(input("Enter bus line code (leave empty for all lines): "))
        line_service_response = soap_call(line_code)
        parsed_response = parse_etree(line_service_response)
        helper_functions.print_result(parsed_response)
    except ValueError as val_error_exc:
        print(val_error_exc)

if __name__ == "__main__": # to prevent accidental execution when imported
    main() 
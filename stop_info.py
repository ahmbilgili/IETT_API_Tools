# Displays information about stops of specified bus line
# Supports searching for a stop of specified bus line

import lxml.etree
import zeep
import sys
import lxml

import utils.functions as helper_functions

translate_dict = {"HATKODU": "Line code", "YON": "Direction", "YON_ADI": "Direction name", "SIRANO": "Queue number", 
                  "DURAKKODU": "Stop code", "DURAKADI": "Stop name", "XKOORDINATI": "X Coordinate (latitude)", "YKOORDINATI": "Y coordinate (longitude)", 
                  "DURAKTIPI": "Stop type", "ISLETMEBOLGE": "Region", "ISLETMEALTBOLGE": "Subregion", "ILCEADI": "Neighborhood name"}

def take_inputs(): # For handling I/O
    line_code = helper_functions.special_char_upper_func(input("Enter bus code: "))
    
    if line_code == "":
        raise ValueError("Bus code cannot be left empty")
    
    direction_choice = helper_functions.special_char_upper_func(input("Enter direction you would like to go (leave empty for all directions): "))

    print("1 - List stops\n2 - Search a stop")
    choice = input("Enter choice: ")

    if choice not in ["1", "2"]:
        raise ValueError("Invalid choice")
    
    stop_name = ""
    if choice == "2":
        stop_name = helper_functions.special_char_upper_func(input("Enter stop name: "))

    IO_Dict = {"Line Code": line_code, "Direction": direction_choice, "Choice": choice, "Stop": stop_name}
    return IO_Dict

def soap_call(hat_kodu, wsdl):
    client = zeep.Client(wsdl=wsdl)
    root = client.service.DurakDetay_GYY_wYonAdi(hat_kodu)

    if len(root) == 0:
        print("Bus line not found")
        exit()
    return root

def parse_soap_response(inputs, root):
    outp_buffer = []
    if inputs["Choice"] == "1":
        if inputs["Direction"] == "":
            for table in root:
                outp_buffer.append(helper_functions.parse_and_translate_values_etree(translate_dict, table))
        else:
            for table in root:
                if inputs["Direction"] in table[2].text:
                    outp_buffer.append(helper_functions.parse_and_translate_values_etree(translate_dict, table))

    elif inputs["Choice"] == "2":
        if inputs["Direction"] == "":
            for table in root:
                if inputs["Stop"] in table[5].text:
                    outp_buffer.append(helper_functions.parse_and_translate_values_etree(translate_dict, table))
        else:
            for table in root:
                if inputs["Direction"] in table[2].text and inputs["Stop"] in table[5].text:
                    outp_buffer.append(helper_functions.parse_and_translate_values_etree(translate_dict, table))
    else:
        raise ValueError("Invalid choice")
    
    if len(outp_buffer) == 0: # I prefer not raising exceptions for this case, this can be a totally valid case.
        print("No stop found")
        exit(1)

    return outp_buffer

def main():
    try:
        wsdl = "xml/durak_hat_bilgi.xml"

        inputs = take_inputs()
        
        root = soap_call(inputs["Line Code"], wsdl)

        outp_buffer = parse_soap_response(inputs, root)
        
        helper_functions.print_result(outp_buffer)

    except ValueError as val_exc:
        print("Value error exception occurred:", val_exc)

if __name__ == "__main__":
    main()

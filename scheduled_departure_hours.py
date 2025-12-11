# Displays scheduled departure hours of given bus line on given weekdays and given direction

from zeep import Client, Settings
import json
import sys
import utils.functions

translate_dict = {"SHATKODU": "Line code", "HATADI": "Line name", "SGUZERAH": "Route", "SYON": "Direction", 
                  "SGUNTIPI": "Day type", "GUZERGAH_ISARETI": "Route sign", "SSERVISTIPI": "Service type", "DT": "Time information"}
wsdl = "xml/PlanlananSeferSaati.asmx.xml"

def validate_and_format_line_code_day(line_code, day):
    line_code = utils.functions.special_char_upper_func(line_code)

    if line_code == "": # I am expecting a hat_kodu, so its reasonable to place exception here.
        raise ValueError("Bus code cannot be left empty")
    
    day = day.upper()

    if day not in {"I", "C", "P"}:
        raise ValueError("Incorrect day choice")

    output_dict = {"Line_Code": line_code, "Day": day}
    return output_dict
    
def soap_call(input_line_code):
    client = Client(wsdl=wsdl)
    line_hours_response = client.service.GetPlanlananSeferSaati_json(input_line_code)

    if len(line_hours_response) == 2:
        print("Timetable not found, it's possible that bus line is incorrect")
        exit()

    return line_hours_response

def convert_soap_response_to_list(soap_response_string):
    soap_response_list = json.loads(soap_response_string)
    return soap_response_list

def obtain_unique_bus_line_names(soap_response_list):
    bus_lines = []

    for element in soap_response_list:
        if element["HATADI"] not in bus_lines: # a bus line can have multiple bus names (endpoints can be different)
            bus_lines.append(element["HATADI"])
    
    return bus_lines

def print_bus_line_names(bus_lines):
    print()
    for element in bus_lines:
        print(element)

def validate_direction(direction):    
    if direction != "G" and direction != "D":
        raise ValueError("Incorrect direction choice")
    return direction

def get_specific_timetables(soap_response_list, user_inputs):
    outp_buffer = []

    for element in soap_response_list:
        if element["SYON"] == user_inputs["Direction"] and element["SGUNTIPI"] == user_inputs["Day"]:
            outp_buffer.append(utils.functions.parse_and_translate_values_dict(translate_dict, element))

    if len(outp_buffer) == 0:
        print("Unable to find timetable of queried bus line with given specifics")
        exit()
        
    return outp_buffer

def print_dictionary(specific_timetables_list):
    print()
    for element in specific_timetables_list:
        for key, value in element.items():
            print(f"{key}: {value}")
        print()

def main():
    try:
        user_inputs = validate_and_format_line_code_day(input("Enter bus line code: "), input("Choose day (I - weekdays, C - Saturday, P - Sunday): "))
        soap_response = soap_call(user_inputs["Line_Code"])

        soap_response_list = convert_soap_response_to_list(soap_response)

        unique_bus_line_names = obtain_unique_bus_line_names(soap_response_list)

        print_bus_line_names(unique_bus_line_names)
        
        direction = input("Enter direction (G - from left to right, D - from right to left): ").upper()
        
        user_inputs["Direction"] = validate_direction(direction)
        
        timetables = get_specific_timetables(soap_response_list, user_inputs)

        print_dictionary(timetables)
    except ValueError as val_exc:
        print("ValueError exception: ", val_exc)

if __name__ == "__main__":
    main()

import pytest
import os
import sys
from lxml import etree
import zeep
import zeep.exceptions

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.append(root_path)

import scheduled_departure_hours

wsdl = "xml/PlanlananSeferSaati.asmx.xml"

def test_validate_and_format_line_code_day_valid_linecode_day():
    input = ("KM18" , "I")
    result = scheduled_departure_hours.validate_and_format_line_code_day(input[0], input[1])
    expected_result = {"Line_Code": "KM18", "Day": "I"}

    assert result == expected_result

def test_validate_and_format_line_code_day_lowercase_line_code_uppercase_day():
    input = ("üm73" , "C")
    result = scheduled_departure_hours.validate_and_format_line_code_day(input[0], input[1])
    expected_result = {"Line_Code": "ÜM73", "Day": "C"}

    assert result == expected_result

def test_validate_and_format_line_code_day_uppercase_line_code_lowercase_day():
    input = ("34i" , "p")
    result = scheduled_departure_hours.validate_and_format_line_code_day(input[0], input[1])
    expected_result = {"Line_Code": "34İ", "Day": "P"}

    assert result == expected_result

def test_validate_and_format_line_code_day_lowercase_line_code_lowercase_day():
    input = ("km43" , "ı")
    result = scheduled_departure_hours.validate_and_format_line_code_day(input[0], input[1])
    expected_result = {"Line_Code": "KM43", "Day": "I"}

    assert result == expected_result

def test_validate_and_format_line_code_day_empty_linecode_valid_day():
    with pytest.raises(ValueError):
        input = ("" , "I")
        result = scheduled_departure_hours.validate_and_format_line_code_day(input[0], input[1])

def test_validate_and_format_line_code_day_valid_linecode_invalid_day():
    with pytest.raises(ValueError):
        input = ("KM18" , "ç")
        result = scheduled_departure_hours.validate_and_format_line_code_day(input[0], input[1])

def test_soap_call_empty_line_code():
    with pytest.raises(zeep.exceptions.Fault):
        input = ""
        response = scheduled_departure_hours.soap_call(input)
 
def test_soap_call_nonexistent_line_code():
    with pytest.raises(SystemExit):
        input = "boyle_bir_hat_yok"
        response = scheduled_departure_hours.soap_call(input)

def test_convert_soap_response_to_list_single_element():
    input = '[{"AB": "C", "D": "ef"}]'
    output = scheduled_departure_hours.convert_soap_response_to_list(input)

    expected_output = [{"AB": "C", "D": "ef"}]

    assert output == expected_output

def test_convert_soap_response_to_list_multiple_elements():
    input = '[{"AB": "C", "D": "ef"}, {"this": "is", "mock": "data"}]'
    output = scheduled_departure_hours.convert_soap_response_to_list(input)

    expected_output = [{"AB": "C", "D": "ef"}, {"this": "is", "mock": "data"}]

    assert output == expected_output

def test_convert_soap_response_to_list_empty():
    input = '[]'
    output = scheduled_departure_hours.convert_soap_response_to_list(input)

    expected_output = []

    assert output == expected_output

def test_obtain_unique_bus_line_names_single_line_input():
    input = [{"HATADI": "SABANCI ÜNİ./MEDENİYET ÜNİ", "some_data": "here_and_there"}]
    output = scheduled_departure_hours.obtain_unique_bus_line_names(input)

    expected_output = ["SABANCI ÜNİ./MEDENİYET ÜNİ"]

    assert output == expected_output

def test_obtain_unique_bus_line_names_multiple_line_input():
    input = [
        {"HATADI": "SABANCI ÜNİ./MEDENİYET ÜNİ", "some_data": "here_and_there"}, 
        {"HATADI": "SABANCI ÜNİ./MEDENİYET ÜNİ", "some_data": "here_and_there"},
        {"HATADI": "AKFIRAT EVLERİ - KARTAL METRO", "some_data": "here_and_there"}
    ]
    output = scheduled_departure_hours.obtain_unique_bus_line_names(input)

    expected_output = ["SABANCI ÜNİ./MEDENİYET ÜNİ", "AKFIRAT EVLERİ - KARTAL METRO"]

    assert output == expected_output

def test_obtain_unique_bus_line_names_empty_input():
    input = []
    output = scheduled_departure_hours.obtain_unique_bus_line_names(input)

    expected_output = []

    assert output == expected_output

def test_print_bus_line_names_single_element_list(capsys):
    input = ["SABANCI ÜNİ./MEDENİYET ÜNİ"]
    scheduled_departure_hours.print_bus_line_names(input)
    captured = capsys.readouterr()

    expected_output = str("SABANCI ÜNİ./MEDENİYET ÜNİ\n")

    assert captured.out == expected_output

def test_print_bus_line_names_multiple_element_list(capsys):
    input = ["SABANCI ÜNİ./MEDENİYET ÜNİ", "AKFIRAT EVLERİ - KARTAL METRO"]
    scheduled_departure_hours.print_bus_line_names(input)
    captured = capsys.readouterr()

    expected_output = str(
        "SABANCI ÜNİ./MEDENİYET ÜNİ\n" + "AKFIRAT EVLERİ - KARTAL METRO\n"
        )

    assert captured.out == expected_output

def test_print_bus_line_names_empty_list(capsys):
    input = []
    scheduled_departure_hours.print_bus_line_names(input)
    captured = capsys.readouterr()

    expected_output = str()

    assert captured.out == expected_output


def test_validate_direction_valid_input():
    input = "G"
    output = scheduled_departure_hours.validate_direction(input)

    expected_output = "G"
    
    assert output == expected_output

def test_validate_direction_invalid_input():
    with pytest.raises(ValueError):
        input = "Ş"
        output = scheduled_departure_hours.validate_direction(input)
    
def test_validate_direction_empty_input():
    with pytest.raises(ValueError):
        input = ""
        output = scheduled_departure_hours.validate_direction(input)

def test_get_specific_timetables_single_element_list():
    inputs = ([
        {"SHATKODU": "KM18", "SYON": "G", "SGUNTIPI": "I"}, 
    ], {"Direction": "G", "Day": "I"})
    output = scheduled_departure_hours.get_specific_timetables(inputs[0], inputs[1])

    expected_output = [{"Line code": "KM18", "Direction": "G", "Day type": "I"}]
    
    assert output == expected_output

def test_get_specific_timetables_multiple_element_list_1():
    inputs = ([
        {"SHATKODU": "KM18", "SYON": "G", "SGUNTIPI": "P"}, 
        {"SHATKODU": "KM18", "SYON": "G", "SGUNTIPI": "C"}, 
        {"SHATKODU": "KM18", "SYON": "G", "SGUNTIPI": "I"}, 
        {"SHATKODU": "KM18", "SYON": "D", "SGUNTIPI": "P"}, 
        {"SHATKODU": "KM18", "SYON": "D", "SGUNTIPI": "C"}, 
        {"SHATKODU": "KM18", "SYON": "D", "SGUNTIPI": "I"}, 
    ], {"Direction": "D", "Day": "C"})
    output = scheduled_departure_hours.get_specific_timetables(inputs[0], inputs[1])

    expected_output = [{"Line code": "KM18", "Direction": "D", "Day type": "C"}]
    
    assert output == expected_output

def test_get_specific_timetables_multiple_element_list_2():
    inputs = ([
        {"SHATKODU": "KM18", "SYON": "D", "SGUNTIPI": "C"}, 
        {"SHATKODU": "UM73", "SYON": "G", "SGUNTIPI": "C"}, 
        {"SHATKODU": "16D", "SYON": "G", "SGUNTIPI": "I"}, 
        {"SHATKODU": "22", "SYON": "D", "SGUNTIPI": "P"}, 
        {"SHATKODU": "132", "SYON": "D", "SGUNTIPI": "C"}, 
        {"SHATKODU": "KM27", "SYON": "D", "SGUNTIPI": "I"}, 
    ], {"Direction": "D", "Day": "C"})
    output = scheduled_departure_hours.get_specific_timetables(inputs[0], inputs[1])

    expected_output = [
        {"Line code": "KM18", "Direction": "D", "Day type": "C"},
        {"Line code": "132", "Direction": "D", "Day type": "C"}]   
    
    assert output == expected_output

def test_get_specific_timetables_multiple_element_list_no_timetable_day():
    with pytest.raises(SystemExit):
        inputs = ([
            {"SHATKODU": "KM18", "SYON": "G", "SGUNTIPI": "C"}, 
            {"SHATKODU": "KM18", "SYON": "G", "SGUNTIPI": "I"}, 
            {"SHATKODU": "KM18", "SYON": "D", "SGUNTIPI": "C"}, 
            {"SHATKODU": "KM18", "SYON": "D", "SGUNTIPI": "I"}, 
        ], {"Direction": "G", "Day": "P"})
        
        output = scheduled_departure_hours.get_specific_timetables(inputs[0], inputs[1])
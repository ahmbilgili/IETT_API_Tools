import sys
import pytest
import zeep
import lxml
import os

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.append(root_path)

import archive

wsdl = "https://api.ibb.gov.tr/iett/ibb/ibb360.asmx?wsdl"


def test_validate_date_input_valid():
    input = "20250601"
    response = archive.validate_date_input(input)
    assert response == True

def test_validate_date_input_invalid_year(capsys):
    with pytest.raises(ValueError) as val_exc:
        input = "abcd0601"
        response = archive.validate_date_input(input)
    expected_exc_message = "Incorrect format (YYYYMMDD)"
    assert val_exc.value.args[0] == expected_exc_message

def test_validate_date_input_valid_date_invalid_length_missing_leading_zero_at_month_field(capsys):
    with pytest.raises(ValueError) as val_exc:
        input = "2025601" # should be 20250611 instead of 2025611
        response = archive.validate_date_input(input) 
    expected_exc_message = "Incorrect format (YYYYMMDD)"
    assert val_exc.value.args[0] == expected_exc_message

def test_validate_date_input_valid_date_invalid_length_missing_leading_zero_at_day_field(capsys):
    with pytest.raises(ValueError) as val_exc:
        input = "2025061" # should be 20250601 instead of 2025061
        response = archive.validate_date_input(input)
    expected_exc_message = "Incorrect format (YYYYMMDD)"
    assert val_exc.value.args[0] == expected_exc_message


def test_soap_call_invalid_date(capsys):
    with pytest.raises(zeep.exceptions.Fault) as zeep_exc:
        input = "abcdefgh"
        response = archive.soap_call(input)
    expected_message_substring = "Server was unable to process request."
    assert expected_message_substring in zeep_exc.value.args[0]

def test_soap_call_date_with_no_data(capsys):
    with pytest.raises(SystemExit):
        input = "20190101"
        response = archive.soap_call(input)
    captured = capsys.readouterr()
    expected_message = "No data found\n"
    assert captured.out == expected_message


def etree_constructor(tables): # helper for test_parse_xml. 
    root_elem = lxml.etree.Element("NewDataSet")
    for i in range(len(tables)):
        root_elem.append(lxml.etree.Element("Table"))
    curr_table_index = 0
    for table in tables:
        for key, value in table.items():
            element = lxml.etree.Element(key)
            element.text = value
            root_elem[curr_table_index].append(element)
        curr_table_index += 1
    return root_elem

def test_parse_xml_single_element_tree():
    input = etree_constructor([{"AB": "C", "D":"EF"}])
    output = archive.parse_xml(input)
    
    expected_output = [{"AB": "C", "D": "EF"}]
    assert output == expected_output

# Turns out lxml.etree.Element cannot have tag "key" if it includes spaces
def test_parse_xml_multiple_element_tree():
    input = etree_constructor([{"AB": "C", "D":"EF"}, {"LineCode": "KM18", "LineName": "SABANCI ÜNİ - KURTKÖY METRO"}])
    output = archive.parse_xml(input)
    
    expected_output = [{"AB": "C", "D":"EF"}, {"LineCode": "KM18", "LineName": "SABANCI ÜNİ - KURTKÖY METRO"}]
    assert output == expected_output

def test_parse_xml_empty_tree():
    input = etree_constructor([])
    output = archive.parse_xml(input)

    expected_output = []
    assert output == expected_output

def test_parse_xml_invalid_input():
    with pytest.raises(TypeError) as type_exc:
        output = archive.parse_xml(["abc", "def"])
    expected_exception_message_header = "Invalid type <class 'str'> passed to parse_xml function"
    assert expected_exception_message_header == type_exc.value.args[0]


def test_get_specific_bus_line_data_no_element_empty_buslinecode():
    input = ([], "")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = []
    assert output == expected_output

def test_get_specific_bus_line_data_no_element_nonempty_buslinecode():
    input = ([], "abc")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = []
    assert output == expected_output

def test_get_specific_bus_line_data_single_element_empty_buslinecode():
    input = ([{"Line code": "KM18", "Line name": "SABANCI ÜNİ - KURTKÖY METRO"}], "")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = [{"Line code": "KM18", "Line name": "SABANCI ÜNİ - KURTKÖY METRO"}]
    assert output == expected_output

def test_get_specific_bus_line_data_single_element_existing_buslinecode():
    input = ([{"Line code": "KM18", "Line name": "SABANCI ÜNİ - KURTKÖY METRO"}], "KM18")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = [{"Line code": "KM18", "Line name": "SABANCI ÜNİ - KURTKÖY METRO"}]
    assert output == expected_output

def test_get_specific_bus_line_data_single_element_nonexistent_buslinecode():
    input = ([{"Line code": "KM18", "Line name": "SABANCI ÜNİ - KURTKÖY METRO"}], "abc")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = []
    assert output == expected_output

def test_get_specific_bus_line_data_multiple_element_empty_buslinecode_multiple_element_output_case():
    input = ([{"Line code": "KM18", "Line name": "SABANCI ÜNİ - KURTKÖY METRO"}, 
              {"Line code": "16D", "Line name": "ALTKAYNARCA / PENDİK - KADIKÖY"}], "")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = [{"Line code": "KM18", "Line name": "SABANCI ÜNİ - KURTKÖY METRO"}, 
              {"Line code": "16D", "Line name": "ALTKAYNARCA / PENDİK - KADIKÖY"}]
    assert output == expected_output

def test_get_specific_bus_line_data_multiple_element_existing_buslinecode_single_element_output_case():
    input = ([{"Line code": "KM18", "Line name": "SABANCI ÜNİ - KURTKÖY METRO"}, 
              {"Line code": "16D", "Line name": "ALTKAYNARCA / PENDİK - KADIKÖY"},
              {"Line code": "133AK", "Line name": "TEPEÖREN - KARTAL"}], "133AK")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = [{"Line code": "133AK", "Line name": "TEPEÖREN - KARTAL"}]
    assert output == expected_output

def test_get_specific_bus_line_data_multiple_element_existing_buslinecode_multiple_element_output_case():
    input = ([{"Line code": "KM18", "Line name": "SABANCI ÜNİ - KURTKÖY METRO"}, 
              {"Line code": "16D", "Line name": "ALTKAYNARCA / PENDİK - KADIKÖY"},
              {"Line code": "133AK", "Line name": "TEPEÖREN - KARTAL"},
              {"Line code": "133AK", "Line name": "TEPEÖREN - KARTAL"},
              {"Line code": "KM18", "Line name": "SABANCI ÜNİ - KURTKÖY METRO"}], "KM18")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = [{"Line code": "KM18", "Line name": "SABANCI ÜNİ - KURTKÖY METRO"},
                       {"Line code": "KM18", "Line name": "SABANCI ÜNİ - KURTKÖY METRO"}]
    assert output == expected_output

def test_get_specific_bus_line_data_multiple_element_nonexistent_buslinecode():
    input = ([{"Line code": "KM18", "Line name": "SABANCI ÜNİ - KURTKÖY METRO"}, 
              {"Line code": "16D", "Line name": "ALTKAYNARCA / PENDİK - KADIKÖY"},
              {"Line code": "133AK", "Line name": "TEPEÖREN - KARTAL"}], "defg")
    output = archive.get_specific_bus_line_data(input[0], input[1])
    expected_output = []
    assert output == expected_output

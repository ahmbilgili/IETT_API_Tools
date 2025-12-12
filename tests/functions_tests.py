import pytest
import sys
import os
import lxml

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.append(root_path)

import utils.functions

# Helper for testing etree_constructor
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


def test_input_singlechar():
    line_code = utils.functions.special_char_upper_func('s')
    assert line_code == 'S'

def test_input_turkishchar():
    line_code = utils.functions.special_char_upper_func('ö')
    assert line_code == 'Ö'

def test_input_mix_lower_upper_noturkishchar():
    line_code = utils.functions.special_char_upper_func('kM18')
    assert line_code == 'KM18'

def test_input_mix_lower_upper_turkishchar():
    line_code = utils.functions.special_char_upper_func('öK1')
    assert line_code == 'ÖK1'

def test_input_empty():
    response = utils.functions.special_char_upper_func("")
    expected_response = ""
    assert response == expected_response

def test_input_special_char():
    response = utils.functions.special_char_upper_func("!.'1")
    expected_response = "!.'1"
    assert response == expected_response

def test_parse_and_translate_values_dict_no_elem():
    output = utils.functions.parse_and_translate_values_dict({"A": "BC", "d": "eF"}, {})
    expected_output = {}
    assert output == expected_output

def test_parse_and_translate_values_dict_single_elem_matching_translate():
    output = utils.functions.parse_and_translate_values_dict({"K": "BC"}, {"K": "bc"})
    expected_output = {"BC": "bc"}
    assert output == expected_output

def test_parse_and_translate_values_dict_single_elem_nomatching_translate():
    output = utils.functions.parse_and_translate_values_dict({"K": "BC", "Z": "eF"}, {"A": "bc"})
    expected_output = {"A": "bc"}
    assert output == expected_output

def test_parse_and_translate_values_dict_multiple_elem_matching_translate_1():
    output = utils.functions.parse_and_translate_values_dict({"A": "BC", "d": "eF"}, {"A": "bc", "d": "ef"})
    expected_output = {"BC": "bc", "eF": "ef"}
    assert output == expected_output

def test_parse_and_translate_values_dict_multiple_elem_matching_translate_2():
    output = utils.functions.parse_and_translate_values_dict({"A": "BC", "Jk": "eF", "pq": "kk"}, {"A": "bc", "d": "ef", "f": "gh", "Jk":"LMNO", "pq": "RST"})
    expected_output = {"BC": "bc", "d": "ef", "f": "gh", "eF": "LMNO", "kk": "RST"}
    assert output == expected_output

def test_parse_and_translate_values_dict_multiple_elem_nomatching_translate():
    output = utils.functions.parse_and_translate_values_dict({"A": "BC", "d": "eF"}, {"G": "bc", "H": "ef"})
    expected_output = {"G": "bc", "H": "ef"}
    assert output == expected_output

def test_parse_and_translate_values_etree_no_elem():
    output = utils.functions.parse_and_translate_values_dict({"A": "BC", "d": "eF"}, {})
    expected_output = {}
    assert output == expected_output

def test_parse_and_translate_values_etree_single_elem_matching_translate():
    output = utils.functions.parse_and_translate_values_dict({"K": "BC"}, {"K": "bc"})
    expected_output = {"BC": "bc"}
    assert output == expected_output

def test_parse_and_translate_values_etree_single_elem_nomatching_translate():
    output = utils.functions.parse_and_translate_values_dict({"K": "BC", "Z": "eF"}, {"A": "bc"})
    expected_output = {"A": "bc"}
    assert output == expected_output

def test_parse_and_translate_values_etree_multiple_elem_matching_translate_1():
    output = utils.functions.parse_and_translate_values_dict({"A": "BC", "d": "eF"}, {"A": "bc", "d": "ef"})
    expected_output = {"BC": "bc", "eF": "ef"}
    assert output == expected_output

def test_parse_and_translate_values_etree_multiple_elem_matching_translate_2():
    output = utils.functions.parse_and_translate_values_dict({"A": "BC", "Jk": "eF", "pq": "kk"}, {"A": "bc", "d": "ef", "f": "gh", "Jk":"LMNO", "pq": "RST"})
    expected_output = {"BC": "bc", "d": "ef", "f": "gh", "eF": "LMNO", "kk": "RST"}
    assert output == expected_output

def test_parse_and_translate_values_etree_multiple_elem_nomatching_translate():
    output = utils.functions.parse_and_translate_values_dict({"A": "BC", "d": "eF"}, {"G": "bc", "H": "ef"})
    expected_output = {"G": "bc", "H": "ef"}
    assert output == expected_output


def test_print_elements_single_element_input(capsys):
    input = [
        {"Line Code": "93M", "Line": "ZEYTINBURNU - MECIDIYEKÖY", "Type": "Günlük", "Update Time": "Kayit Saati: 12:01", "Message": "mock"}
    ]
    utils.functions.print_result(input)
    captured = capsys.readouterr()
    assert captured.out == str(
        "Line Code: 93M\n" +
        "Line: ZEYTINBURNU - MECIDIYEKÖY\n" +
        "Type: Günlük\n" + 
        "Update Time: Kayit Saati: 12:01\n" +
        "Message: mock\n\n"
    )

def test_print_elements_multiple_element_input(capsys):
    input = [
        {"Line Code": "93M", "Line": "ZEYTINBURNU - MECIDIYEKÖY", "Type": "Günlük", "Update Time": "Kayit Saati: 12:01", "Message": "mock"},
        {'Line Code': '93T', 'Line': 'ZEYTINBURNU - TAKSIM', 'Type': 'Günlük', 'Update Time': 'Kayit Saati: 12:01', 'Message': ''},
        {'Line Code': '97GE', 'Line': '15 TEMMUZ MAHALLESI - EMINÖNÜ', 'Type': 'Sefer', 'Update Time': 'Kayit Saati: 04:27', 'Message': 'nock'},
    ]
    utils.functions.print_result(input)
    captured = capsys.readouterr()
    assert captured.out == str(
        "Line Code: 93M\n" +
        "Line: ZEYTINBURNU - MECIDIYEKÖY\n" +
        "Type: Günlük\n" + 
        "Update Time: Kayit Saati: 12:01\n" +
        "Message: mock\n\n" +

        "Line Code: 93T\n" +
        "Line: ZEYTINBURNU - TAKSIM\n" +
        "Type: Günlük\n" + 
        "Update Time: Kayit Saati: 12:01\n" +
        "Message: \n\n" +

        "Line Code: 97GE\n" +
        "Line: 15 TEMMUZ MAHALLESI - EMINÖNÜ\n" +
        "Type: Sefer\n" + 
        "Update Time: Kayit Saati: 04:27\n" +
        "Message: nock\n\n"
    )

def test_print_elements_empty_input(capsys):
    input = []
    utils.functions.print_result(input)
    captured = capsys.readouterr()
    assert captured.out == ""
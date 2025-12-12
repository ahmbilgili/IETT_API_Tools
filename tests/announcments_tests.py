import pytest
import os
import sys
import json

# quite elegant solution
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.append(root_path)

import announcments

def test_soap_response_to_list_nonempty_response_single_dictionary():
    input = '[{"A": "BC", "D": "ef"}]'

    result = announcments.soap_response_to_list(input)
    expected_output = [{"A": "BC", "D": "ef"}]

    assert result == expected_output

def test_soap_response_to_list_nonempty_response_multiple_dictionary():
    input = '[{"A": "BC", "D": "ef"}, {"B": "CD", "E": "fg"}]'

    result = announcments.soap_response_to_list(input)
    expected_output = [{"A": "BC", "D": "ef"}, {"B": "CD", "E": "fg"}]

    assert result == expected_output

def test_soap_response_to_list_empty_response():
    input = "[]"

    result = announcments.soap_response_to_list(input)
    expected_output = []

    assert result == expected_output


def test_get_specific_bus_lines_announcments_busline_exists_single_element_response():
    input = ["1", [{"HATKODU": "1", "HAT": "NA", "MESAJ": "TestMessage1"}, {"HATKODU": "2", "HAT": "NA", "MESAJ": "TestMessage3"}]]
    result = announcments.get_specific_bus_lines_announcments(input[0], input[1])

    expected_result = [{"Line Code": "1", "Line": "NA", "Message": "TestMessage1"}]
    
    assert result == expected_result

def test_get_specific_bus_lines_announcments_busline_exists_multiple_element_response():
    input = ["1", [{"HATKODU": "1", "HAT": "NA", "MESAJ": "TestMessage1"}, {"HATKODU": "1", "HAT": "NA", "MESAJ": "TestMessage2"}, {"HATKODU": "2", "HAT": "NA", "MESAJ": "TestMessage3"}]]
    result = announcments.get_specific_bus_lines_announcments(input[0], input[1])

    expected_result = [{"Line Code": "1", "Line": "NA", "Message": "TestMessage1"}, {"Line Code": "1", "Line": "NA", "Message": "TestMessage2"}]
    
    assert result == expected_result

def test_get_specific_bus_lines_announcments_busline_exists_invalid_busline():
    input = ["3", [{"HATKODU": "1", "HAT": "NA", "MESAJ": "TestMessage1"}, {"HATKODU": "1", "HAT": "NA", "MESAJ": "TestMessage2"}, {"HATKODU": "2", "HAT": "NA", "MESAJ": "TestMessage3"}]]
    result = announcments.get_specific_bus_lines_announcments(input[0], input[1])

    expected_result = []
    
    assert result == expected_result


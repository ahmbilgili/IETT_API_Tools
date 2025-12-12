import pytest
import os
import sys
from lxml import etree

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
sys.path.append(root_path)

import line_service

# https://docs.pytest.org/en/stable/reference/reference.html#std-fixture-capsys

def test_soap_invalid1(capsys):
    with pytest.raises(SystemExit):
        line_service.soap_call("kino_severim")
        captured = capsys.readouterr()
        print(captured)
        assert captured.out == "Hat bulunamadı / Bus line not found\n"

def test_soap_invalid2(capsys):
    with pytest.raises(SystemExit):
        line_service.soap_call("boyle_bir_hat_yok")
        print("this aint getting printed bro")
        captured = capsys.readouterr()
        print(captured)
        assert captured.out == "Hat bulunamadı / Bus line not found\n"

def etree_constructor(tables): # helper for methods below. 
    root_elem = etree.Element("NewDataSet")
    for i in range(len(tables)):
        root_elem.append(etree.Element("Table"))
    curr_table_index = 0
    for table in tables:
        for key, value in table.items():
            element = etree.Element(key)
            element.text = value
            root_elem[curr_table_index].append(element)
        curr_table_index += 1
    return root_elem

# For testing the function above.
def test_parse_etree_singletable(capsys):
    mock_tables = [{"AB": "C", "This_is": "Fake", "Good": "Bye"}]
    mock_etree = etree_constructor(mock_tables)
    result = line_service.parse_etree(mock_etree)
    expected_result = [{"AB": "C", "This_is": "Fake", "Good": "Bye"}]
    assert result == expected_result

def test_print_etree_multipletable(capsys):
    mock_tables = [{"AB": "C", "This_is": "Fake", "Good": "Bye"}, {"This_is": "Table_Two"}]
    mock_etree = etree_constructor(mock_tables)
    result = line_service.parse_etree(mock_etree)
    expected_result = [{"AB": "C", "This_is": "Fake", "Good": "Bye"}, {"This_is": "Table_Two"}]
    assert result == expected_result

def test_print_etree_emptytable(capsys):
    mock_tables = [{}]
    mock_etree = etree_constructor(mock_tables)
    result = line_service.parse_etree(mock_etree)
    expected_result = [{}]
    assert result == expected_result
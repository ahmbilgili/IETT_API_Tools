# to convert some of the turkish lowercase characters to their corresponding upper case pairs
def special_char_upper_func(param):
    special_chars = {"ğ":"Ğ", "ü":"Ü", "i":"İ", "ş":"Ş", "ö":"Ö", "ç":"Ç"}
    for key, value in special_chars.items():
        param = param.replace(key, value)
    return param.upper()

# converts given input to ms
# Example: /DateTime(number)/, extracts number
def ms_parser(line):
    startidx = -1
    endidx = -1

    for i in range(len(line)):
        if (line[i] == '('):
            startidx = i
        elif (line[i] == ')'):
            endidx = i
    date_to_ms = int(line[startidx+1:endidx])
    return date_to_ms

# Converts the dictionary elements in given list to a string format.
def convert_list_tostr(announcment_list):
    out_string = ""
    for element in announcment_list:
        for key, value in element.items():
            out_string += f"{key}: {value}\n"
        out_string += "\n"
    return out_string

# For translating key(s) in dictionary and adding (translated_key, value) pair to a new dictionary
def parse_and_translate_values_dict(translate_dict, buffer):
    temp_dict = {}
    for key, value in buffer.items():
        try:
            temp_dict[translate_dict[key]] = value
        except:
            temp_dict[key] = value
    return temp_dict

def parse_and_translate_values_etree(translate_dict, buffer):
    temp_dict = {}
    for element in buffer:
        try:
            temp_dict[translate_dict[element.tag]] = element.text
        except:
            temp_dict[element.tag] = element.text
    return temp_dict

# Prints results. buffer is a list of dictionaries.
def print_result(buffer):
    for element in buffer:
        for key, value in element.items():
            print(f"{key}: {value}")
        print()
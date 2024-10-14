import ast

def convert_string_to_dict(input_string):
    result = {}
    current_key = ''
    in_brackets = False
    bracket_content = ''

    for char in input_string:
        if char in '{[':
            in_brackets = True
            bracket_content = char
        elif char in ']}':
            in_brackets = False
            bracket_content += char
            result[current_key.rstrip(':').strip()] = ast.literal_eval(bracket_content)
            current_key = ''
        elif char == ',' and not in_brackets:
            if current_key and current_key.rstrip(':').strip() not in result:
                result[current_key.rstrip(':').strip()] = None
            current_key = ''
        elif in_brackets:
            bracket_content += char
        else:
            current_key += char

    if current_key and current_key.rstrip(':').strip() not in result:
        result[current_key.rstrip(':').strip()] = None

    return result

# Test the function
input_str = 'a,b:[1,2,3],c:{1:1,2:2},d,e'
output_dict = convert_string_to_dict(input_str)
print(output_dict)
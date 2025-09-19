
def get_biggest_number_of_code (code_list : list, code_location : int, number_of_prefix : int, prefix_got_digit : bool = False) -> int:
    try:
        code_number_list : list = code_catcher(code_list= code_list, code_location= code_location, number_of_prefix= number_of_prefix)
        prefix_list : list  = prefix_catcher(code_list= code_list, code_location= code_location, number_of_prefix= number_of_prefix)
        if prefix_got_digit:
            pass
        elif _detect_got_digit(prefix_list= prefix_list) :
            raise ValueError(f"The prefix:{prefix_list} got number! "
                             f"if you except the prefix is contain number,SET prefix_got_digit to True!")
        number_list = _list_str_number_to_int_number(str_number_list= code_number_list)
        biggest_number = _get_biggest_number_of_list(number_list= number_list)
        return biggest_number
    except Exception as e:
        raise Exception(f"GET BIGGEST NUMBER OF CODE FAILED. ERROR: {str(e)}")

def code_catcher (code_list : list,code_location : int,number_of_prefix : int) -> list:
    row_got_alpha_count : int = 0 #just for testing bug in debug mode
    code_number_list : list =[]
    for row in code_list:
        if any(item.isalpha() for item in row[code_location][number_of_prefix:]):
            row_got_alpha_count += 1
            continue
        code_number_list.append(row[code_location][number_of_prefix:])
    return code_number_list

def prefix_catcher (code_list : list,code_location : int,number_of_prefix : int) -> list:
    code_number_list : list =[]
    for row in code_list:
        code_number_list.append(row[code_location][0:number_of_prefix])
    return code_number_list

def _get_biggest_number_of_list (number_list : list) -> int:
    biggest_number : int = 0
    try:
        for row in number_list:
            if row > biggest_number:
                biggest_number = row
        return biggest_number
    except ValueError:
        raise ValueError(f"The number_list:{number_list} is not int type list!")

def _list_str_number_to_int_number (str_number_list : list) -> list:
    int_list : list =[]
    try:
        for number in str_number_list:
            int_list.append(int(number))
        return int_list
    except ValueError:
        raise ValueError(f"The list : {str_number_list} is contain string!,_list_str_to_int function is just convert ‘1’ to 1")

def _detect_got_digit(prefix_list : list) -> bool:
    for row in prefix_list:
        if row.isdigit():
            return True
    return False

def generate_code_id (code_list : list, prefix_generate : str, code_location : int, number_of_prefix : int
                      , prefix_got_digit : bool, code_id_digit_count : int) -> str:

    code_number = get_biggest_number_of_code(code_list= code_list, code_location= code_location,
                                             number_of_prefix= number_of_prefix, prefix_got_digit= prefix_got_digit) + 1
    code_id = (prefix_generate + str(code_number).zfill(code_id_digit_count))
    return code_id

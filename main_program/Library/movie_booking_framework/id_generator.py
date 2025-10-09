
#get the biggest number of code (even got prefix)
def get_biggest_number_of_code (
        code_list: list,
        code_location: int,
        number_of_prefix: int,
        prefix_got_digit: bool = False
) -> int:
    try:
        #get the code list from the list
        code_number_list: list = code_catcher(
            code_list= code_list,
            code_location= code_location,
            number_of_prefix= number_of_prefix
        )
        #get the prefix list from the list
        prefix_list: list  = prefix_catcher(
            code_list= code_list,
            code_location= code_location,
            number_of_prefix= number_of_prefix
        )
        #if user set the prefix is got digit,don't do the check
        if prefix_got_digit or number_of_prefix == 0:
            pass
        #if user don't set, check the prefix got digit or not
        elif _detect_got_digit(prefix_list= prefix_list):
            #if prefix got digit,interrupt the action and raise error
            raise ValueError(f"The prefix:{prefix_list} got number! "
                             f"if you except the prefix is contain number,SET prefix_got_digit to True!")
        #turn the str list to int list
        #example: ["1","2","3"] -> [1,2,3]
        number_list = _list_str_number_to_int_number(str_number_list= code_number_list)
        #get the biggest number from the number_list
        biggest_number = _get_biggest_number_of_list(number_list= number_list)
        #return the biggest number
        return biggest_number
    #if python got any error
    except Exception as e:
        #interrupt the action and raise the error
        raise Exception(f"GET BIGGEST NUMBER OF CODE FAILED. ERROR: {str(e)}")

#turn the normal list to code list
#example: [['P001','test','test'],['P002','test','test']] -> ['001','002']
def code_catcher (code_list: list,code_location: int,number_of_prefix: int) -> list:
    #for debugging
    row_got_alpha_count: int = 0 #just for testing bug in debug mode
    code_number_list: list =[]
    for row in code_list:
        #if the code_number got alphabet,count += 1 (row[code_location][number_of_prefix:] is to locate code_number location)
        if any(item.isalpha() for item in row[code_location][number_of_prefix:]):
            row_got_alpha_count += 1
            continue
        #append the code to the list
        if isinstance(code_list[0],list):
            code_number_list.append(row[code_location][number_of_prefix:])
        else:
            code_number_list.append(row[number_of_prefix:])
    #return the code number list
    return code_number_list

#turn the normal list to prefix list
#example: [['P001','test','test'],['P002','test','test']] -> ['P','P']
def prefix_catcher (code_list: list,code_location: int,number_of_prefix: int) -> list:
    code_number_list: list =[]
    for row in code_list:
        if isinstance(code_list[0], list):
            ##append the prefix from code_list (row[code_location][0:number_of_prefix] is to locate prefix location)
            code_number_list.append(row[code_location][0:number_of_prefix])
        else:
            code_number_list.append(row[0:number_of_prefix])
    return code_number_list

#example:
#[1,2,3,4,5,6,7,8] -> 8
def _get_biggest_number_of_list (number_list: list) -> int:
    biggest_number: int = 0
    try:
        for row in number_list:
            if row > biggest_number:
                biggest_number = row
        return biggest_number
    except ValueError:
        raise ValueError(f"The number_list:{number_list} is not int type list!")

#turn the str list to int list
#example:
#['1','2','3','4'] -> [1,2,3,4]
def _list_str_number_to_int_number (str_number_list: list) -> list:
    int_list: list =[]
    try:
        for number in str_number_list:
            #turn the element to int,and append it into list
            int_list.append(int(number))
        #return the list
        return int_list
    #if the str list contain non number ['1','2b']
    except ValueError:
        #interrupt the action and raise error
        raise ValueError(
            f"The list: {str_number_list} is contain string!"
            f"_list_str_to_int function is just convert ‘1’ to 1"
        )

#detect the list got digit or not (if got any digit,will return true)
def _detect_got_digit(prefix_list: list) -> bool:
    for row in prefix_list:
        if row.isdigit():
            return True
    return False

#generate the code_id
def generate_code_id (
        code_list: list,
        prefix_generate: str,
        code_location: int,
        number_of_prefix: int,
        prefix_got_digit: bool,
        code_id_digit_count: int
) -> str:
    # get the biggest number from the list
    code_number = get_biggest_number_of_code(
        code_list= code_list,
        code_location= code_location,
        number_of_prefix= number_of_prefix,
        prefix_got_digit= prefix_got_digit
    ) + 1
    # add the prefix for the number
    code_id = (prefix_generate + str(code_number).zfill(code_id_digit_count))
    # return the code
    return code_id

import random
import os
from main_program.Library.role.clerk import clerk


def get_data_directory(path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    normpath = os.path.normpath(os.path.join(base_dir, "..", "..", "Data", path))
    return normpath


def get_content(path):
    """
    Read file content if exists.
    If file does not exist, create an empty file and return ''
    """
    with open(path, 'r', newline='') as role_file:
        role_file.readline()
        content = role_file.read().strip()
        return content


def get_data(path):
    """
    Read data from file and split into flat list.
    Example file content: 'C001,name,1\nC002,name,2'
    Returns: ['C001','name','1','C002','name','2']
    """
    # record ['C001,name,1', 'C002,name,2', 'C003,name,3']
    content = get_content(path)
    if not content:
        return []
    file_data = content.split('\n')
    final_data = []
    for i in file_data:
        # record ['C001', 'name', '1']   ['C002', 'name', '2']   ['C003', 'name', '3']
        data = i.strip().split(',')
        for j in data:
            # print  C001    name    1   C002    name    2   C003    name    3   003
            final_data.append(j)

    return final_data


def generate_verification_code() -> str:
    """
    Generate a random verification code (1 lowercase, 1 uppercase, 1 digit)
    Example: aB5
    """
    lower_list = []
    upper_list = []
    number_list = []
    for i in range(62):
        if i < 26:
            lower_list.append(chr(ord('a') + i))
        elif 26 <= i < 52:
            upper_list.append(chr(ord('A') + i - 26))
        elif i >= 52:
            number_list.append(chr(ord('0') + i - 52))
    #get random index
    r_lower = random.randint(0, len(lower_list) - 1)
    r_upper = random.randint(0, len(upper_list) - 1)
    r_num = random.randint(0, len(number_list) - 1)
    return lower_list[r_lower] + upper_list[r_upper] + number_list[r_num]


def write_data(path, user_id, name, password, role_prefix,has_balance_column : bool = False):
    """
    Append new user record to CSV file.
    Format: C001,Name,password
    """
    file = open(path, 'a')
    if has_balance_column:
        file.write(f"{role_prefix}{user_id:03d},{name},{password},0\n")
    else:
        file.write(f"{role_prefix}{user_id:03d},{name},{password}\n")
    file.close()

def get_column_count(path):
    with open(path, 'r') as f:
        header = f.readline()
        return len(header.split(','))

def generate_ID(path, prefix):
    """
    Generate the next user ID based on the last one stored in file.
    Example: if last ID is C005, next will be C006.
    """
    if not os.path.exists(path):
        with open(path, 'w') as f:
            pass
            return '000'
    f = open(path, 'r')
    f.readline()
    content = f.read().strip()
    f.close()
    if content == '':
        return '000'
    else:

        last_number = 0
        column_count = get_column_count(path)
        final_data = get_data(path)
        for i in range(0, len(final_data), column_count):
            user_id = final_data[i]
            if user_id.startswith(prefix):
                num = int(user_id[1:])
                if num > last_number:
                    last_number = num

    return last_number + 1


def check_identity(path, name_or_id, input_password):
    """
    Check if username/ID and password match.
    Return role string if valid, otherwise None.
    """
    content = get_content(path)
    if content == '':
        return False
    else:
        file_data = content.split('\n')
        for record in file_data:
            # record ['C001,name,password','C002,name,password']
            part = record.split(',')
            user_id, name, password = part[0], part[1], part[2]
            if ((user_id == name_or_id) or (name == name_or_id)) and input_password == password:
                if user_id.startswith('C'):
                    return 'Customer'
                elif user_id.startswith('M'):
                    return 'Cinema Manager'
                elif user_id.startswith('T'):
                    return 'Technician'
                elif user_id.startswith('K'):
                    return 'Ticketing Clerk'
        return None


def check_data(path, name_or_id, password):
    """
    Check if given user ID or username matches password in file.
    Return True/False.
    """
    content = get_content(path)
    if content == '':
        return False
    else:
        #final_data = ['C001', 'zhihao', '123', '814', 'C002', 'victor', 'Abcde@1', '220', 'C003', 'caixukun', '@Aa11', '9', 'C004', 'menglei', 'Mingda0@', '0']
        final_data = get_data(path)
        #column_count = 3
        column_count = get_column_count(path)
        # judge userid correct or not
        for i in range(0, len(final_data), column_count):
            if name_or_id == final_data[i]:
                # password correct
                return password == final_data[i + 2]
            # judge name
        else:
            for i in range(1, len(final_data), column_count):
                if name_or_id == final_data[i]:
                    # password correct
                    return password == final_data[i + 1]
            return False


def check_password(password, num):
    """
    Validate password with rules:
    - Minimum length
    - At least 1 lowercase, 1 uppercase, 1 number, 1 special char
    - No spaces
    """
    if len(password) < num:
        raise ValueError(f"Password length must not be less than {num}")
    has_lower, has_upper, has_alpha, has_number, has_special_char = False, False, False, False, False
    special_char_list = ["!", "@", "#", "$", "%", "^", "&", "*"]
    for char in password:
        if char.isdigit(): has_number = True
        if char.isupper(): has_upper = True
        if char.islower(): has_lower = True
        if char.isalpha(): has_alpha = True
        if char in special_char_list: has_special_char = True
        if char == " ": raise ValueError("Password should not contain space!")
    if not has_alpha: raise ValueError("Password should contain at least one alpha!")
    if not has_number: raise ValueError("Password should contain at least one number!")
    if not has_upper: raise ValueError("Password should contain at least one uppercase letter!")
    if not has_lower: raise ValueError("Password should contain at least one lowercase letter!")
    if not has_special_char: raise ValueError("Password should contain at least one special character!")


"""def require(char):
    
    Helper function: count type of character (lower/upper/number)
    Updates global counters.
    
    global count_lower, count_number, count_upper
    lower_list = []
    upper_list = []
    number_list = []
    for i in range(62):
        if i < 26:
            lower_list.append(chr(ord('a') + i))
        elif 26 <= i < 52:
            upper_list.append(chr(ord('A') + i - 26))
        elif i >= 52:
            number_list.append(chr(ord('0') + i - 52))
    if char in lower_list:
        count_lower += 1
        return True
    elif char in upper_list:
        count_upper += 1
        return None
    elif char in number_list:
        count_number += 1
        return True
    else:
        return False"""


def check_user_name(new_name, path):
    """
    Check if username already exists in file.
    Raise error if duplicate.
    """
    column_count = get_column_count(path)
    final_data = get_data(path)
    for i in range(1, len(final_data), column_count):
        # i = name
        if new_name == final_data[i]:
            raise ValueError("Username exist!")


def register(path,role_prefix):
    """
    Register new customer user.
    - Input username (must be unique)
    - Input password (must follow rules)
    - Generate new user ID and save to file
    """
    while True:
        try:
            new_name = input("Please enter your name:\n")
            check_user_name(new_name, path)
            break
        except ValueError as e:
            print(e)

    print(
        "password must include one uppercase letter, one lowercase letter, one number, one special character and length > 5")
    while True:
        try:
            new_password = input("input password\n")
            check_password(new_password, 5)
            break
        except ValueError as e:
            print(e)

    new_id = generate_ID(path, role_prefix)
    column_count = get_column_count(path)
    if column_count == 3:
        write_data(path, new_id, new_name, new_password,role_prefix)
    elif column_count == 4:
        write_data(path, new_id, new_name, new_password,role_prefix,True)


def get_id(path, name_or_id):
    """
    Check if username/ID and password match.
    Return role string if valid, otherwise None.
    """
    content = get_content(path)
    if content == '':
        return False
    else:
        file_data = content.split('\n')
        for record in file_data:
            # record ['C001,name,password','C002,name,password']
            part = record.split(',')
            user_id, name, password = part[0], part[1], part[2]
            if (user_id == name_or_id) or (name == name_or_id):
                return user_id
        return None


def login(path):
    """
    User login process:
    - Input ID and password
    - Input verification code
    - Check credentials
    """
    while True:
        print('please login')
        user_id = input('UserID:\n')
        password = input('password:\n')

        while True:
            try:
                verification_code = generate_verification_code()
                print('verification code: ' + verification_code)
                input_verification_code = input('please enter verification Code:\n')
                if input_verification_code != verification_code:
                    raise ValueError('verification code error, please try again')
                else:
                    break
            except ValueError as e:
                print(e)
        flag = check_data(path, user_id, password)
        if flag:
            print('login success')
            user_real_id = get_id(path, user_id)
            return user_real_id
        else:
            print('login failed')
            return None


def user_input_role():
    """
    Let user choose role by number.
    1 = Clerk, 2 = Manager, 3 = Technician, 4 = Customer
    """
    print("1. Ticketing Clerk\n2. Cinema manager\n3. Technician\n4. Customer\n5. Exit")
    while True:
        try:
            role = int(input("please input your role by number\n"))
            if role in (1, 2, 3, 4, 5):
                return role
            else:
                raise ValueError("invalid number, please try again")

        except ValueError as e:
            print(e)


def role(
        customer_data,
        clerk_data,
        manager_data,
        technician_data,
        customer_function,
        clerk_function,
        manager_function,
        technician_function
):
    """
    Main role dispatcher.
    Different role leads to different login/register logic.
    """
    while True:
        role_num = user_input_role()
        if role_num == 5:
            print ("Thank you for using this system")
            break
        elif role_num == 4:
            try:
                choice = int(input("please input login(1) or register(2) by number\n"))
                if choice == 1:
                    user_id = login(customer_data)
                    if user_id is not None:
                        customer_function(user_id)
                elif choice == 2:
                    register(customer_data,'C')
                    print('customer register success')
                else:
                    raise ValueError("invalid number, please try again")
            except ValueError as e:
                print(e)

        elif role_num == 1:
            user_id = login(clerk_data)
            if user_id is not None:
                clerk_function(user_id)


        elif role_num == 2:
            user_id = login(manager_data)
            if user_id is not None:
                manager_function(user_id)


        elif role_num == 3:
            user_id = login(technician_data)
            if user_id is not None:
                technician_function(user_id)

        else:
            print("invalid number, please try again")



if __name__ == '__main__':
     pass
    # main()
    # while True:
    #     try:
    #         main()
    #         pass
    #     except ValueError as e:
    #         print(e)

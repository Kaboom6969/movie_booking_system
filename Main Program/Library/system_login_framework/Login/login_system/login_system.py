import csv
import random
import csv
from operator import truediv


number = 0
count_lower = 0
count_upper = 0
count_number = 0


def get_content(path):
    with open( path, 'r',newline= '') as role_file:
        content = role_file.read().strip()
        return content


def get_data(path):
    # record ['C001,name,1', 'C002,name,2', 'C003,name,3']
    content = get_content(path)
    file_data = content.split('\n')
    final_data = []
    for i in file_data:
        # record ['C001', 'name', '1']   ['C002', 'name', '2']   ['C003', 'name', '3']
        data = i.strip().split(',')
        for j in data:
            # print  C001    name    1   C002    name    2   C003    name    3   003
            final_data.append(j)

    return final_data


def generate_verification_code():
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
    r_lower = random.randint(0, len(lower_list) - 1)
    r_upper = random.randint(0, len(upper_list) - 1)
    r_num = random.randint(0, len(number_list) - 1)
    return lower_list[r_lower] + upper_list[r_upper] + number_list[r_num]


def write_data(path, user_id, name, password):
    file = open(path, 'a')
    file.write(f"C{user_id:03d},{name},{password}\n")
    file.close()


def generate_ID(path, prefix):
    f = open(path, 'r')
    content = f.read().strip()
    f.close()
    if content == '':
        return '000'
    else:

        last_number = 0
        final_data = get_data(path)
        for i in range(0, len(final_data), +3):
            user_id = final_data[i]
            if user_id.startswith(prefix):
                num = int(user_id[1:])
                if num > last_number:
                    last_number = num

    return last_number


def check_identity(path, name_or_id, input_password):
    content = get_content(path)
    if content == '':
        return False
    else:
        file_data = content.split('\n')
        for record in file_data:
            # record ['C001,name,password','C002,name,password']
            user_id, name, password = record.split(',')
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
    content = get_content(path)
    if content == '':
        return False
    else:
        final_data = get_data(path)
        # judge userid correct or not
        for i in range(0, len(final_data), +3):
            if name_or_id == final_data[i]:
                # password correct
                return password == final_data[i + 2]
            # judge name
        else:
            for i in range(1, len(final_data), +3):
                if name_or_id == final_data[i]:
                    # password correct
                    return password == final_data[i + 1]
            return False


def check_password(password, num):
    if len(password) < num:
        # print('password must longer than ' + str(num))
        return False
    else:
        for char in password:
            require(char)
            if count_upper >= 1 and count_lower >= 1 and count_number >= 1:
                return True
        return False


def require(char):
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
        return False


def check_user_name(new_name, path):
    final_data = get_data(path)
    for i in range(1, len(final_data), +3):
        # i = name
        if new_name == final_data[i]:
            return False
    return True


def register(path):
    while True:
        try:
            new_name = input('new name:')
            flag = check_user_name(new_name, path)
            if flag:
                break
            else:
                raise ValueError('username exist, please try again')
        except ValueError as e:
            print(e)

    while True:
        try:
            print("password must include one uppercase letter, one lowercase letter, one number and length > 5")
            new_password = input("input password\n")
            flag = check_password(new_password, 5)
            if flag:
                print("register success")
                break
            else:
                raise ValueError("fail, please try again")
        except ValueError as e:
            print(e)
    latest_id = generate_ID(path, 'C')
    new_id = int(latest_id) + 1
    write_data(path, new_id, new_name, new_password)


def login(path):
    while True:
        print('please login')
        name_or_id = input('name or UserID:')
        password = input('password:')

        while True:
            try:
                verification_code = generate_verification_code()
                print('verification code: ' + verification_code)
                input_verification_code = input('please enter verification Code:')
                if input_verification_code != verification_code:
                    raise ValueError('verification code error, please try again')
                else:
                    break
            except ValueError as e:
                print(e)
        flag = check_data(path, name_or_id, password)
        if flag:
            print('login success')
            return True
        else:
            print('login failed')
            return False


def user_input_role():
    print("Ticketing Clerk(1), Cinema manager(2), Technician(3), Customer(4)")
    while True:
        try:
            role = int(input("please input your role by number\n"))
            if role in (1, 2, 3, 4):
                return role
            else:
                raise ValueError("invalid number, please try again")

        except ValueError as e:
            print(e)


def role(customer_data, clerk_data, manager_data, technician_data):
    role_num = user_input_role()
    if role_num == 4:
        while True:
            try:
                choice = int(input("please input login(1) or register(2) by number\n"))
                if choice == 1:
                    flag = login(customer_data)
                    if flag:
                        print('customer function')
                    break
                elif choice == 2:
                    register(customer_data)
                    print('customer register success')
                    break
                else:
                    raise ValueError("invalid number, please try again")
            except ValueError as e:
                print(e)


    elif role_num == 1:
        flag = login(clerk_data)
        if flag:
            print("clerk function")


    elif role_num == 2:
        flag = login(manager_data)
        if flag:
            print("manager function")


    elif role_num == 3:
        flag = login(technician_data)
        if flag:
            print("technician function")

    else:
        print("invalid number, please try again")


def main():
    role(customer_data='customer.csv', clerk_data='clerk.csv', manager_data='manager.csv',
         technician_data='technician.csv')


if __name__ == '__main__':
    while True:
        try:
            main()
        except ValueError as e:
            print(e)

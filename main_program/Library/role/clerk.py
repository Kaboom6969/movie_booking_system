from logging import raiseExceptions


import os
from datetime import datetime
from movie_booking_system.main_program.Library.movie_booking_framework.movie_list_framework import *
from movie_booking_system.main_program.Library.movie_booking_framework.movie_seats_framework import *
from movie_booking_system.main_program.Library.movie_booking_framework.seat_visualizer import *
from movie_booking_system.main_program.Library.movie_booking_framework.cinema_services import *
from movie_booking_system.main_program.Library.movie_booking_framework.framework_utils import *
from movie_booking_system.main_program.Library.movie_booking_framework.valid_checker import *
from movie_booking_system.main_program.Library.movie_booking_framework.id_generator import *


def get_customer_csv_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    customer_path = os.path.normpath(
        os.path.join(base_dir, "..", "system_login_framework/Login/login_system/customer.csv"))
    return customer_path


def get_Data_Directory_path(path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.normpath(os.path.join(base_dir, "..", "..", "Data/" + path))
    return data_path


def write_booking_data(path, data):
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def get_and_print_booking_data(path, input_movie_code):
    booking_data_list = []
    with (open(path, 'r') as f):
        reader = csv.reader(f)
        rows = list(reader)
        # header = [Book ID,User ID,Movie Code,Date,(1:booking 2:paid),seat(x-axis),seat(y-axis),Source]
        header = rows[0]
        print(
            f"{header[0]:<10}{header[1]:<10}{header[2]:<13}{header[3]:<13}{header[4]:<21}{header[5]:<15}{header[6]:<15}{header[7]:<15}")
        for row in rows[1:]:
            booking_id, user_id, movie_code, date, status, x_axis, y_axis, source = row
            if input_movie_code == movie_code:
                print(
                    f"{booking_id:<10}{user_id:<10}{movie_code:<13}{date:<13}{status:<21}{x_axis:<15}{y_axis:<15}{source:<15}")
                booking_data_list.append(row)
        return booking_data_list


def generate_booking_id(path):
    id_max = 0
    directory_path = get_Data_Directory_path(path)
    with (open(directory_path, 'r') as booking_read):
        reader = csv.reader(booking_read)
        rows = list(reader)
        if len(rows) <= 1:
            return "B001"
        for row in rows[1:]:
            if not row:
                continue
            booking_id = row[0]
            if booking_id.startswith("B"):
                try:
                    id_num = int(booking_id[1:])
                    if id_num > id_max:
                        id_max = id_num
                except ValueError as e:
                    continue

    next_id = id_max + 1
    return f"B{next_id:03d}"


def get_user_choice():
    while True:
        print("\nplease enter your choice:")
        try:
            choice = int(input(
                "\nbooking(1), cancel or modify booking(2), check movie seats(3), print receipt(4), quit(5)\n"))
            if choice in [1, 2, 3, 4, 5]:
                return choice
            else:
                print("Please enter a valid option (1-5).")
        except ValueError as e:
            print(e)


def select_movie(movie_list):
    while True:
        print("\n")
        print(movie_list)
        # 输入代码
        input_movie_code = input("please enter your movie code: \n")
        for movie in movie_list:
            if movie[0] == input_movie_code:
                return input_movie_code
        else:
            print("please enter valid movie code")


def generate_seat_axis(column, row):
    return f"{column},{row}"


def check_booking_full(movie_seat_list):
    capacity = get_capacity(movie_seat_list)
    if capacity == 0:
        return True
    return False


def handle_booking(movie_seats_csv, booking_data_csv, template_seats_csv, movie_seat_list, input_movie_code, user_id):
    booking_full = check_booking_full(movie_seat_list)
    if booking_full:
        print("booking is full")
        return
    while True:
        while True:
            print_movie_seat_as_emojis(movie_seat_list)
            try:
                print(f"\nrow should be between 1 and {len(movie_seat_list)}")
                row = int(input("Please enter the row number: "))  # y_axis
                print_movie_seat_as_emojis(movie_seat_list, -1, row)
                break
            except ValueError as e:
                print(e)
        while True:
            try:
                print(f"\ncolumn should be between 1 and {len(movie_seat_list[0])}")
                column = int(input("Please enter the column number: "))  # x_axis
                print_movie_seat_as_emojis(movie_seat_list, column, row)
                break
            except ValueError as e:
                print(e)

        if not movie_seats_pointer_valid_check(movie_seat_list, column, row):
            print(f"Invalid seat, please try again")
            continue
        try:
            seat_value = movie_seats_specify_value(movie_seat_list, column, row)
        except IndexError as e:
            print(e)
            continue
        if seat_value == '-1':
            print_movie_seat_as_emojis(movie_seat_list, column, row)
            print("Invalid seat, please try again")
        elif seat_value == '1':
            print_movie_seat_as_emojis(movie_seat_list, column, row)
            print("This seat is already taken. Please enter another one")
        else:
            today = datetime.today().strftime('%Y/%m/%d')
            print("Purchased successfully")
            booking_data_csv_path = get_Data_Directory_path(booking_data_csv)
            booking_id = generate_booking_id(booking_data_csv)
            data_row = [[booking_id, user_id, input_movie_code, today, 2, column, row, 'Clerk']]
            write_booking_data(booking_data_csv_path, data_row)
            link_seats(movie_seats_csv=movie_seats_csv, booking_data_csv=booking_data_csv,
                       template_seats_csv=template_seats_csv)
            movie_seat_list.clear()
            read_movie_seats_csv(movie_seats_csv=movie_seats_csv, movie_seats=movie_seat_list,
                                 movie_code=input_movie_code)
            print_movie_seat_as_emojis(movie_seat_list)
            break


def checking_movie(movie_seats_csv:str,movie_seat_list:list,input_movie_code:str):
    movie_seat_list.clear()
    read_movie_seats_csv(movie_seats_csv=movie_seats_csv, movie_seats=movie_seat_list, movie_code=input_movie_code)
    print_movie_seat_as_emojis(movie_seat_list)
    capacity = get_capacity(movie_seat_list)
    print(f"\n This movie seat capacity is {capacity}")


def check_booking_id(booking_data_list, input_booking_id):
    for booking_data in booking_data_list:
        if input_booking_id == booking_data[0]:
            return input_booking_id
    return None


def get_user_seat_axis(booking_data_list, input_booking_id):
    for booking_data in booking_data_list:
        if input_booking_id == booking_data[0]:
            return booking_data[5], booking_data[6]
    return None


def get_user_booking_axis_and_booking_id(booking_data_list):
    while True:
        input_booking_id = input('please enter your booking id: \n')
        booking_id = check_booking_id(booking_data_list, input_booking_id)
        if booking_id is not None:
            column, row = get_user_seat_axis(booking_data_list, input_booking_id)  # x_axis  # y_axis
            break
        else:
            print("please enter valid booking id")
            continue

    return column, row, booking_id


def get_modify_choice():
    while True:
        print("\nplease enter your choice:")
        try:
            choice = int(input(
                "\ncancel booking(1), modify booking(2), quit(3)\n"))
            if choice in [1, 2, 3]:
                return choice
            else:
                print("Please enter a valid option (1-3).")
        except ValueError as e:
            print(e)


def delete_user_booking_data(booking_data_csv, booking_id):
    with open(booking_data_csv, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)
    updated_rows = []
    for row in rows:
        if row[0] != booking_id:
            updated_rows.append(row)
    with open(booking_data_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(updated_rows)


def check_booking_data(booking_data_csv, input_movie_code):
    booking_data_csv_path = get_Data_Directory_path(booking_data_csv)
    with open(booking_data_csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)
        filter_movie_list = []
        for row in rows:
            if row[2] == input_movie_code:
                filter_movie_list.append(row)
        if not filter_movie_list:
            print('no booking data found!')
            return False
        else:
            return True

def modify_booking_data(booking_data_csv, booking_id):
    with open(booking_data_csv, 'r', newline='') as f:
        reader = csv.reader(f)
        for i in reader:
            print(i)



def modify_booking(movie_seats_csv, booking_data_csv, template_seats_csv, movie_seat_list, input_movie_code, user_id):
    booking_data_exist = check_booking_data(booking_data_csv, input_movie_code)
    if booking_data_exist:
        while True:
            booking_data_csv_path = get_Data_Directory_path(booking_data_csv)
            booking_data_list = get_and_print_booking_data(booking_data_csv_path, input_movie_code)
            column, row, booking_id = get_user_booking_axis_and_booking_id(booking_data_list)
            choice = get_modify_choice()
            # cancel booking(1), modify booking(2), quit(3)
            if choice == 1:
                delete_user_booking_data(booking_data_csv_path, booking_id)
                link_seats(movie_seats_csv=movie_seats_csv, booking_data_csv=booking_data_csv,
                           template_seats_csv=template_seats_csv)
                break
            elif choice == 2:
                handle_booking(movie_seats_csv=movie_seats_csv, booking_data_csv=booking_data_csv,template_seats_csv=template_seats_csv,
                               movie_seat_list=movie_seat_list, input_movie_code=input_movie_code, user_id=user_id)
                modify_movie_seats_list(movie_seat_list, int(column), int(row), 1)
                update_movie_seats_csv(movie_seats_csv=movie_seats_csv, movie_seats=movie_seat_list,
                                       movie_code=input_movie_code)
            elif choice == 3:
                break


def modify_customer_seat(booking_id, movie_seat_list):
    print_movie_seat_as_emojis(movie_seat_list)


def clerk(user_id):
    while True:
        # 订票
        movie_list = []
        # get movie list
        read_movie_list_csv(movie_list_csv="movie_list.csv", movie_list=movie_list, movie_code="all")

        # get user movie input
        input_movie_code = select_movie(movie_list)

        movie_seat_list = []
        # get movie seat list
        read_movie_seats_csv(movie_seats_csv="movie_seat.csv", movie_seats=movie_seat_list, movie_code=input_movie_code)

        while True:
            choice = get_user_choice()
            if choice == 1:
                handle_booking(movie_seats_csv="movie_seat.csv", booking_data_csv="booking_data.csv",
                               template_seats_csv="template_seats.csv",
                               movie_seat_list=movie_seat_list, input_movie_code=input_movie_code, user_id=user_id)

            elif choice == 2:
                modify_booking(movie_seats_csv="movie_seat.csv", booking_data_csv="booking_data.csv",
                                    template_seats_csv="template_seats.csv",
                                    movie_seat_list=movie_seat_list, input_movie_code=input_movie_code, user_id=user_id)
                link_seats(movie_seats_csv="movie_seat.csv", booking_data_csv="booking_data.csv",
                           template_seats_csv="template_seats.csv")
            elif choice == 3:
                checking_movie(movie_seats_csv="movie_seat.csv", movie_seat_list=movie_seat_list, input_movie_code=input_movie_code)
            elif choice == 4:
                print("receipt")
            elif choice == 5:
                break


# 取消或修改booking
# 查看电影列表
# 打印订单

def main():
    clerk(user_id='K001')
    #path = get_Data_Directory_path("booking_data.csv")
    #modify_booking_data(booking_data_csv=path,booking_id="")


if __name__ == '__main__':
    main()

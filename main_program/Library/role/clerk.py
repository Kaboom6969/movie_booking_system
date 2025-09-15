from logging import raiseExceptions

from movie_booking_system.main_program.Library.movie_booking_framework.movie_list_framework import read_movie_list_csv
from movie_booking_system.main_program.Library.movie_booking_framework.movie_seats_framework import *
from movie_booking_system.main_program.Library.system_login_framework.Login.login_system.login_system import *
import os
from datetime import datetime


def get_customer_csv_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    customer_path = os.path.normpath(
        os.path.join(base_dir, "..", "system_login_framework/Login/login_system/customer.csv"))
    return customer_path


def get_Data_Directory_path(path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    movie_seat_path = os.path.normpath(os.path.join(base_dir, "..", "..", "Data/" + path))
    return movie_seat_path


def write_booking_data(path, data):
    with open(path, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)


def get_and_print_booking_data(path, input_movie_code):
    booking_data_list = []
    with (open(path, 'r') as f):
        reader = csv.reader(f)
        rows = list(reader)
        # header = [Book ID,User ID,Movie Code,Date,(1:booking 2:paid),Seat(x-axis,y-axis)]
        header = rows[0]
        print(f"{header[0]:<10}{header[1]:<10}{header[2]:<13}{header[3]:<13}{header[4]:<21}{header[5]:<10}")
        for row in rows[1:]:
            booking_id, user_id, movie_code, date, status, seat = row
            if input_movie_code == movie_code:
                print(f"{booking_id:<10}{user_id:<10}{movie_code:<13}{date:<13}{status:<21}{seat:<10}")
                booking_data_list.append(row)
        return booking_data_list


def generate_booking_id(path):
    id_max = 0
    with (open(path, 'r') as booking_read):
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


def handle_booking(movie_seat_list, input_movie_code):
    while True:
        print_movie_seat_as_emojis(movie_seat_list)
        print(f"\nrow should be between 1 and {len(movie_seat_list)}")
        row = int(input("Please enter the row number: "))  # y_axis
        print(f"\ncolumn should be between 1 and {len(movie_seat_list[0])}")
        column = int(input("Please enter the column number: "))  # x_axis
        if not movie_seats_pointer_valid_check(movie_seat_list, column, row):
            print(f"Invalid seat, please try again")
            continue
        try:
            seat_value = movie_seats_specify_value(movie_seat_list, column, row)
            print(seat_value)
        except IndexError as e:
            print(e)
            continue
        if seat_value == '-1':
            print("Invalid seat, please try again")
        elif seat_value == '1':
            print("This seat is already taken. Please enter another one")
        else:
            customer_csv_path = get_customer_csv_path()
            customer_id = login(customer_csv_path)
            if customer_id is not None:
                today = datetime.today().strftime('%Y/%m/%d')
                print("Purchased successfully")
                modify_movie_seats_list(movie_seat_list, column, row, 1)
                update_movie_seats_csv(movie_seats_csv="movie_seat.csv", movie_seats=movie_seat_list,
                                       movie_code=input_movie_code)
                booking_data_csv_path = get_Data_Directory_path("booking_data.csv")
                booking_id = generate_booking_id(booking_data_csv_path)
                seat_axis = generate_seat_axis(column, row)
                data_row = [[booking_id, customer_id, input_movie_code, today, 2, seat_axis]]
                write_booking_data(booking_data_csv_path, data_row)
                break
            else:
                print("login failed please try again")
            break


def checking_movie(movie_seat_list):
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
            return booking_data[5]
    return None


def get_user_booking_axis_and_booking_id(booking_data_list):
    while True:
        input_booking_id = input('please enter your booking id: \n')
        booking_id = check_booking_id(booking_data_list, input_booking_id)
        if booking_id is not None:
            seat_axis = get_user_seat_axis(booking_data_list, input_booking_id)
            seat_list = seat_axis.split(",")
            column = seat_list[0]  # x_axis
            row = seat_list[1]  # y_axis
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

def delete_user_booking_data(booking_data_csv,booking_id):
    with open(booking_data_csv,'r',newline='') as f:
        reader = csv.reader(f)
        rows = list(reader)
    updated_rows = []
    for row in rows:
        if row[0] != booking_id:
            updated_rows.append(row)
    with open(booking_data_csv,'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerows(updated_rows)

def modify_booking_data(booking_data_csv, input_movie_code, movie_seat_list,movie_seats_csv):
    while True:
        booking_data_csv_path = get_Data_Directory_path(booking_data_csv)
        booking_data_list = get_and_print_booking_data(booking_data_csv_path, input_movie_code)
        print(booking_data_list)
        column, row, booking_id = get_user_booking_axis_and_booking_id(booking_data_list)
        choice = get_modify_choice()
        if choice == 1:
            modify_movie_seats_list(movie_seat_list, int(column), int(row), 0)
            update_movie_seats_csv(movie_seats_csv=movie_seats_csv, movie_seats=movie_seat_list,
                                   movie_code=input_movie_code)
            delete_user_booking_data(booking_data_csv_path, booking_id)
            break
        elif choice == 2:
            pass
        elif choice == 3:
            break



def clerk():
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
                handle_booking(movie_seat_list=movie_seat_list, input_movie_code=input_movie_code)
            elif choice == 2:
                modify_booking_data(booking_data_csv="booking_data.csv", input_movie_code=input_movie_code,
                                    movie_seat_list=movie_seat_list,movie_seats_csv="movie_seat.csv")
            elif choice == 3:
                checking_movie(movie_seat_list)
            elif choice == 4:
                print("receipt")
            elif choice == 5:
                break


# 取消或修改booking
# 查看电影列表
# 打印订单

def main():
    clerk()
    #delete_user_booking_data(booking_data_csv="booking_data.csv")


if __name__ == '__main__':
    main()

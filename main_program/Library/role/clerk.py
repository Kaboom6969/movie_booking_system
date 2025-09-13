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


def read_booking_data(path):
    with (open(path, 'r') as f):
        reader = csv.reader(f)
        rows = list(reader)
        for row in rows:
            user_id, movie_code, date, status = row
            print(f"{user_id: <10}{movie_code:<15}{date:<15}{status:<10}")

def generate_booking_id(path):
    id_max = 1
    with (open(path, 'r') as booking_read):
        reader = csv.reader(booking_read)
        rows = list(reader)
        if len(rows) == 1:
            return f"B{id_max:03d}"
        elif len(rows) >= 2:
            for i in range(1,len(rows),++1):
                booking_id = rows[i][0]
                if id_max < int(booking_id[1:]):
                    id_max = int(booking_id[1:])
                id_max = id_max + 1
            return f"B{id_max:03d}"
        return None


def clerk():
    while True:
        # 订票
        movie_list = []
        read_movie_list_csv(movie_list_csv="movie_list.csv", movie_list=movie_list, movie_code="all")
        while True:
            print("\n")
            print(movie_list)
            # 输入代码t
            input_movie_code = input("please enter your movie code: \n")
            flag = False
            for movie in movie_list:
                if movie[0] == input_movie_code:
                    flag = True
            if flag:
                break
            else:
                print("please enter valid movie code")

        movie_seat_list = []
        read_movie_seats_csv(movie_seats_csv="movie_seat.csv", movie_seats=movie_seat_list, movie_code=input_movie_code)

        while True:
            print("\nplease enter your choice:")
            choice = input("\nbooking(1), cancel or modify booking(2), check movie seats(3), print receipt(4), quit(5)\n")
            if choice == "1":
                while True:
                    x_axis = True
                    y_axis = True
                    print_movie_seat_as_emojis(movie_seat_list)
                    print(f"\nrow should be between 1 and {len(movie_seat_list)}")
                    row = int(input("Please enter the row number: "))
                    print(f"\ncolumn should be between 1 and {len(movie_seat_list[0])}")
                    column = int(input("Please enter the column number: "))
                    if column < 1 or column > len(movie_seat_list[0]):  # Validate x_axis
                        print(f"column should be between 1 and {len(movie_seat_list[0])}\nYour column is {column}")
                        x_axis = False
                    if row < 1 or row > len(movie_seat_list):  # Validate y_axis
                        print(f"row should be between 1 and {len(movie_seat_list)}\nYour row is {row}")
                        y_axis = False
                    if x_axis and y_axis:
                        if movie_seat_list[len(movie_seat_list) - row][column - 1] == '-1':
                            print("Invalid seat, please try again")
                        elif movie_seat_list[len(movie_seat_list) - row][column - 1] == '1':
                            print("This seat is already taken. Please enter another one")
                        else:
                            customer_csv_path = get_customer_csv_path()
                            customer_id = login(customer_csv_path)
                            if customer_id is not None:
                                today = datetime.today().strftime('%Y/%m/%d')
                                print("Purchased successfully")
                                modify_movie_seats_list(movie_seat_list, column, row, 1)
                                update_movie_seats_csv(movie_seats_csv="movie_seat.csv", movie_seats=movie_seat_list,movie_code=input_movie_code)
                                booking_data_csv_path = get_Data_Directory_path("booking_data.csv")
                                booking_id = generate_booking_id(booking_data_csv_path)
                                data_row = [[booking_id, customer_id, input_movie_code, today, 2]]
                                write_booking_data(booking_data_csv_path, data_row)
                                break
                            else:
                                print("login failed please try again")
                            break
                break

            elif choice == "2":
                booking_data_csv_path = get_Data_Directory_path("booking_data.csv")
                read_booking_data(booking_data_csv_path)
                break
            elif choice == "3":
                print_movie_seat_as_emojis(movie_seat_list)
                break
            elif choice == "4":
                print("receipt")
            elif choice == "5":
                break


# 取消或修改booking
# 查看电影列表
# 打印订单

def main():
    clerk()


if __name__ == '__main__':
    main()

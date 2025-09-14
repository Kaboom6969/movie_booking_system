from movie_booking_system.main_program.Library.movie_booking_framework.movie_seats_framework import *
from movie_booking_system.main_program.Library.movie_booking_framework.movie_list_framework import *

DEFAULT_WIDTH = 20

def check_ticket_bought(customer_code : str,booking_data_csv : str,movie_list_csv : str) -> list:
    booking_list : list = []            #format: ['B001','C001', '001', '2025/8/13','2']
    movie_code_list : list = []         #format:'001'
    read_movie_list_csv(movie_list_csv= booking_data_csv, movie_list= booking_list, movie_code= customer_code,movie_mode = False,code_location = 1)
    print(f"{'Movie Code': <{DEFAULT_WIDTH}}{'Booking Date': <{DEFAULT_WIDTH}}")
    print("-" * (DEFAULT_WIDTH * 2 + 1))
    for row in booking_list:
        movie_code_list.append(row[2])
        print(f"{str(row[2]): <{DEFAULT_WIDTH}}{str(row[3]): <{DEFAULT_WIDTH}}")
    return movie_code_list

def booking_to_movie_list_print(movie_code_list : list, movie_code : str, movie_list_csv : str) -> None:
    if movie_code not in movie_code_list:
        raise ValueError("Please enter the valid movie code!")
    else:
        booking_movie_list : list = []  #format:[['002', 'Joker', 'cinema002', '19:00', '22:00']]
        read_movie_list_csv(movie_list_csv= movie_list_csv, movie_list= booking_movie_list, movie_code= movie_code)
        movie_list_print_with_format(data_list= booking_movie_list)

def movie_list_print_with_format(data_list : list,movie_seats_csv : str, DEFAULT_WIDTH : int = DEFAULT_WIDTH) -> None:
    print(f"{'Movie Code': <{DEFAULT_WIDTH}}{'Movie Name': <{DEFAULT_WIDTH}}"
          f"{'Cinema Location': <{DEFAULT_WIDTH}}{'Start Time': <{DEFAULT_WIDTH}}"
          f"{'End Time': <{DEFAULT_WIDTH}}{'Capacity': <{DEFAULT_WIDTH}}")
    print("-" * (DEFAULT_WIDTH * 6 + 1))
    for row in data_list:
        seat_list_temp : list = []
        read_movie_seats_csv(movie_seats_csv= movie_seats_csv,movie_seats= seat_list_temp,movie_code= row[0])
        for data in row:
            print(f"{data: <{DEFAULT_WIDTH}}", end="")
        print(f"{get_capacity(seat_list_temp): <{DEFAULT_WIDTH}}", end ="")
        print()

def code_range_create(code_list : list,code_location : int) -> list:
    code_range_list : list =[]
    for row in code_list:
        code_range_list.append(row[code_location])
    return code_range_list

def book_movie(movie_code : str,movie_seats_csv : str) -> None:
    while True:
        try:
            movie_seats : list = movie_list_to_movie_seats_print(movie_code= movie_code,movie_seats_csv= movie_seats_csv)
            x_range : list = x_range_calculate(movie_seats= movie_seats)
            y_range : list = y_range_calculate(movie_seats= movie_seats)
        except Exception as e:
            raise Exception(f"BOOK MOVIE FAILED!ERROR:{e}\nTHIS IS PROGRAM BUG!\nPLEASE CHECK THE PROGRAM!")

        while True:
            try:
                while True:
                    try:
                        x_pointer = int(input(f"Please enter the column number (x_axis:{x_range[0]} to {x_range[1]}): "))
                    except ValueError as e:
                        raise ValueError("Column number should be a number!")
                    except IndexError as e:
                        raise IndexError(f"Column number should be in the range({x_range[0]} - {x_range[1]})")

                    movie_list_to_movie_seats_print(movie_code=movie_code, movie_seats_csv=movie_seats_csv,x_pointer=x_pointer)
                    break

                while True:
                    try:
                        y_pointer = int(input(f"Please enter the row number (y_axis:{y_range[0]} to {y_range[1]}:"))
                    except ValueError as e:
                        raise ValueError("Row number should be a number!")
                    except IndexError as e:
                        raise IndexError(f"Row number should be in the range({y_range[0]} - {y_range[1]}")

                    movie_list_to_movie_seats_print(movie_code=movie_code, movie_seats_csv=movie_seats_csv, x_pointer= x_pointer, y_pointer= y_pointer)
                    break

            seats_value = movie_seats_specify_value(movie_seats=movie_seats, x_axis=x_pointer, y_axis=y_pointer)
            if seats_value in "1": raise ValueError("seats_booked")
            elif seats_value in "-1": raise ValueError("seats_not_exixts")
            break

        except ValueError as e:
            if "seat_booked" in e:
                print("This seat is already been booked,Please enter the axis again!")
            if "seats_not_exixts" in e:
                print("This seat is not exists,Please enter the axis again!")

        while True:
            try:
                if seats_value in "0":
                    while True:
                        try:
                            user_input = str(input("Are You (S)ure? OR (C)ancel it ?"))
                            if user_input.lower() not in "s" and user_input.lower() not in "c":
                                raise ValueError("user_input value error")
                            break
                        except ValueError as e:
                            print("The command must be S(s) or C(c)!")

                if user_input.lower() in "s":
                    modify_movie_seats_list(movie_seat_list= movie_seats,x_axis= x_pointer,y_axis= y_pointer,target_number= 1)
                    update_movie_seats_csv(movie_seats_csv= movie_seats_csv,movie_seats= movie_seats,movie_code= movie_code)
                    quit = True
                    break
                elif user_input.lower() in "c":
                    break
        if quit == True:
            break





def movie_list_to_movie_seats_print(movie_code : str,movie_seats_csv : str,x_pointer = -1,y_pointer = -1) -> list:
    movie_seats_list : list = []
    read_movie_seats_csv(movie_seats_csv= movie_seats_csv,movie_seats = movie_seats_list,movie_code= movie_code)
    print()
    print("-" * int(DEFAULT_WIDTH * 1.8))
    print_movie_seat_as_emojis(movie_seats_list,x_pointer,y_pointer)
    print("-" * int(DEFAULT_WIDTH * 1.8))
    print(f"Movie Code:{movie_code}")
    return movie_seats_list

def check_all_movie_list(movie_list_csv : str,movie_seats_csv : str) -> list:
        movie_list_all : list = []
        read_movie_list_csv(movie_list_csv= movie_list_csv,movie_list= movie_list_all)
        movie_list_print_with_format(data_list= movie_list_all,movie_seats_csv= movie_seats_csv)
        return code_range_create(code_list= movie_list_all,code_location= 0)




#JUST TEST
if __name__ == '__main__':
    try:
        code_range : list =check_all_movie_list("movie_list.csv","movie_seat.csv")
        # bought_movie : list = check_ticket_bought(customer_code = "C001",booking_data_csv = "booking_data.csv", movie_list_csv = "movie_list.csv")
        code = str(input("Please enter the movie code that you want to check"))
        # booking_to_movie_list_print(movie_code_list = bought_movie, movie_code = code, movie_list_csv ="movie_list.csv")
        # user_command = str(input("Please Enter Your Command\n(C)heck Seat\t(Q)uit\n"))
        # if 'c' in user_command.lower():
        movie_list_to_movie_seats_print(movie_code= code,movie_seats_csv= "movie_seat.csv")
    except IndexError:
        print("Please enter the movie code in the range!")


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

#def book_movie(movie_code : str,movie_seats_csv : str) -> None:

def movie_list_to_movie_seats_print(movie_code : str,movie_seats_csv : str):
    movie_seats_list : list = []
    read_movie_seats_csv(movie_seats_csv= movie_seats_csv,movie_seats = movie_seats_list,movie_code= movie_code)
    print()
    print("-" * int(DEFAULT_WIDTH * 1.8))
    print_movie_seat_as_emojis(movie_seats_list)
    print("-" * int(DEFAULT_WIDTH * 1.8))
    print(f"Movie Code:{movie_code}")

def check_all_movie_list(movie_list_csv : str,movie_seats_csv : str) -> list:
        movie_list_all : list = []
        read_movie_list_csv (movie_list_csv= movie_list_csv,movie_list= movie_list_all)
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


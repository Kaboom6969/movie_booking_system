from movie_booking_system.main_program.Library.movie_booking_framework.movie_seats_framework import *
from movie_booking_system.main_program.Library.movie_booking_framework.movie_list_framework import *

DEFAULT_WIDTH = 20

def check_ticket_bought(customer_code : str,booking_data_csv : str,movie_list_csv : str) -> list:
    booking_list : list = []            #format: ['C001', '001', '2025/8/13', '1']
    movie_code_list : list = []         #format:'001'
    read_movie_list_csv(movie_list_csv= booking_data_csv, movie_list= booking_list, movie_code= customer_code,movie_mode = False)
    print(f"{'Movie Code': <{DEFAULT_WIDTH}}{'Booking Date': <{DEFAULT_WIDTH}}")
    print("-" * (DEFAULT_WIDTH * 2 + 1))
    for row in booking_list:
        movie_code_list.append(row[1])
        print(f"{str(row[1]): <{DEFAULT_WIDTH}}{str(row[2]): <{DEFAULT_WIDTH}}")
    return movie_code_list

def booking_to_movie_print(movie_code_list : list, movie_code : str, movie_list_csv : str) -> None:
    if movie_code not in movie_code_list:
        raise ValueError("Please enter the valid movie code!")
    else:
        booking_movie_list : list = []  #format:[['002', 'Joker', 'cinema002', '19:00', '22:00']]
        read_movie_list_csv(movie_list_csv= movie_list_csv, movie_list= booking_movie_list, movie_code= movie_code)
        print(f"{'Movie Code': <{DEFAULT_WIDTH}}{'Movie Name': <{DEFAULT_WIDTH}}"
              f"{'Cinema Location': <{DEFAULT_WIDTH}}{'Start Time': <{DEFAULT_WIDTH}}{'End Time': <{DEFAULT_WIDTH}}")
        print("-"*(DEFAULT_WIDTH*5+1))
        for row in booking_movie_list:
            for data in row:
                print(f"{data: <{DEFAULT_WIDTH}}",end="")
            print()


#JUST TEST
if __name__ == '__main__':
    bought_movie : list = check_ticket_bought(customer_code = "C001",booking_data_csv = "booking_data.csv", movie_list_csv = "movie_list.csv")
    code = str(input("Please enter the movie code that you want to check"))
    booking_to_movie_print(movie_code_list = bought_movie, movie_code = code,movie_list_csv = "movie_list.csv")

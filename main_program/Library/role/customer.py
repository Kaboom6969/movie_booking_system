from movie_booking_system.main_program.Library.movie_booking_framework.movie_seats_framework import *
from movie_booking_system.main_program.Library.movie_booking_framework.movie_list_framework import *

def check_ticket_bought(customer_code : str,booking_data_csv : str,movie_list_csv : str):
    booking_list : list = []
    read_movie_list_csv(movie_list_csv= booking_data_csv, movie_list= booking_list, movie_code= customer_code)
    print(booking_list)

if __name__ == '__main__':
    check_ticket_bought(customer_code = C001,booking_data_csv = "booking_data.csv", movie_list_csv = "movie_list.csv")

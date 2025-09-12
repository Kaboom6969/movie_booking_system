from movie_booking_system.main_program.Library.movie_booking_framework.movie_seats_framework import *
from movie_booking_system.main_program.Library.movie_booking_framework.movie_list_framework import *

def check_ticket_bought(booking_data_csv : str,movie_list_csv : str):
    booking_list : list = []
    read_movie_list_csv(movie_list_csv= booking_data_csv, movie_list= booking_list)

from main_program.Library.cache_framework import data_dictionary_framework as ddf
from main_program.Library.data_communication_framework import cache_csv_sync_framework as ccsf
from main_program.Library.movie_booking_framework import cinema_services as cnsv, cinema_services

#testinggggggggggggggggggggggggggg
if __name__ == '__main__':
    ddf.init_all_dictionary()
    cnsv.sync_all(movie_list_csv="movie_list.csv",movie_seats_csv="movie_seat.csv",cinema_device_list_csv="cinema_device_list.csv",default_template_code= "TEMPLATE001")

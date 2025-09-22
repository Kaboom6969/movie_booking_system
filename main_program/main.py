from main_program.Library.movie_booking_framework import data_dictionary_framework as ddf
from main_program.Library.role import *
from main_program.Library.role.customer import book_movie_operation


#testinggggggggggggggggggggggggggg
if __name__ == '__main__':
    ddf.init_all_dictionary()
    print(ddf.MOVIE_SEATS_DICTIONARY)
    print(ddf.MOVIE_LIST_DICTIONARY)
    print(ddf.BOOKING_DATA_DICTIONARY)
    print(ddf.CINEMA_DEVICE_DICTIONARY)
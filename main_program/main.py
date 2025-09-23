from main_program.Library.cache_framework import data_dictionary_framework as ddf
from main_program.Library.data_communication_framework import cache_csv_sync_framework as ccsf

#testinggggggggggggggggggggggggggg
if __name__ == '__main__':
    ddf.init_all_dictionary()
    print(ddf.MOVIE_SEATS_DICTIONARY)
    print(ddf.MOVIE_LIST_DICTIONARY)
    print(ddf.BOOKING_DATA_DICTIONARY)
    print(ddf.CINEMA_DEVICE_DICTIONARY)
    print(ddf.TEMPLATE_SEATS_DICTIONARY)
    print(ddf.MOVIE_TEMPLATE_CODE_DICTIONARY)
    ccsf.seats_cache_write_to_csv(seats_csv= "movie_seat.csv",seats_dictionary_cache= ddf.MOVIE_SEATS_DICTIONARY
                                  ,mt_code_dictionary_cache= ddf.MOVIE_TEMPLATE_CODE_DICTIONARY)
    ccsf.list_cache_write_to_csv(list_csv="movie_list.csv",list_dictionary_cache= ddf.MOVIE_LIST_DICTIONARY)
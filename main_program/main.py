from main_program.Library.cache_framework import data_dictionary_framework as ddf

#testinggggggggggggggggggggggggggg
if __name__ == '__main__':
    ddf.init_all_dictionary()
    print(ddf.MOVIE_SEATS_DICTIONARY)
    print(ddf.MOVIE_LIST_DICTIONARY)
    print(ddf.BOOKING_DATA_DICTIONARY)
    print(ddf.CINEMA_DEVICE_DICTIONARY)
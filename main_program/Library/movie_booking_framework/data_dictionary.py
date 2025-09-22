from .movie_list_framework import *
MOVIE_LIST_DICTIONARY : dict = {}
BOOKING_DATA_DICTIONARY : dict = {}
CINEMA_DEVICE_DICTIONARY : dict = {}

def list_dictionary_create (list_csv : str,code_location : int) -> dict:
    movie_list_temp : list = []
    movie_list_dict_in_func : dict = {}
    read_movie_list_csv(movie_list_csv= list_csv, movie_list= movie_list_temp)
    for row in movie_list_temp:
        key : str = row[code_location]
        row.remove(key)
        movie_list_dict_in_func.update({key:row[:]})
    return movie_list_dict_in_func

def dictionary_update(dictionary : dict,key_location : int,list_to_add : list) -> None:
    list_to_add_temp : list = list_to_add[:]
    key : str = list_to_add_temp[key_location]
    list_to_add_temp.remove(key)
    dictionary.update({key:list_to_add_temp})





def init_all_dictionary():
    global MOVIE_LIST_DICTIONARY,BOOKING_DATA_DICTIONARY,CINEMA_DEVICE_DICTIONARY
    MOVIE_LIST_DICTIONARY = list_dictionary_create (list_csv= "movie_list.csv", code_location = 0)
    BOOKING_DATA_DICTIONARY = list_dictionary_create (list_csv= "booking_data.csv", code_location = 0)
    CINEMA_DEVICE_DICTIONARY = list_dictionary_create (list_csv= "cinema_device_list.csv", code_location = 0)
    print (MOVIE_LIST_DICTIONARY)
    print (BOOKING_DATA_DICTIONARY)
    print (CINEMA_DEVICE_DICTIONARY)



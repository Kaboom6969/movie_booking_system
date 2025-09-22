from .movie_list_framework import *
from .movie_seats_framework import *
from .valid_checker import *
MOVIE_LIST_DICTIONARY : dict = {}
BOOKING_DATA_DICTIONARY : dict = {}
CINEMA_DEVICE_DICTIONARY : dict = {}
MOVIE_SEATS_DICTIONARY : dict = {}

def seat_dictionary_create (seats_csv : str) -> dict:
    key: str = ""
    movie_seats_temp: list = []
    movie_seats_dict_in_func : dict = {}
    movie_seats_csv_valid_check(movie_seats_csv= seats_csv)
    movie_seats_raw_data: list = read_movie_seats_csv_raw_data(movie_seats_csv= seats_csv)
    read_data_mode : bool = False
    for row in movie_seats_raw_data:
        if row[0] == "CODE":
            key = row[1]
            read_data_mode = True
        if read_data_mode and row[0] == "DATA":
            movie_seats_temp.append(row[1:])
        if read_data_mode and row[0] == "END":
            movie_seats_dict_in_func.update({key:movie_seats_temp[:]})
            key = ""
            read_data_mode = False
            movie_seats_temp.clear()
    return movie_seats_dict_in_func

def seat_dictionary_update (dictionary : dict,key_to_add : str,seats_list_to_add : list) -> dict:
    dictionary.update({key_to_add:seats_list_to_add})
    return dictionary

# python 3.9++ for this function !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def dictionary_update_with_dict (dictionary : dict,dictionary_to_add : dict) -> dict:
    return dictionary | dictionary_to_add

def dictionary_delete (dictionary : dict,key_to_delete : str) -> dict:
    try:
        debug_data = dictionary.pop(key_to_delete)
    except KeyError:
        raise ValueError(f"{key_to_delete} not found in dictionary!")
    return dictionary


def list_dictionary_create (list_csv : str,code_location : int) -> dict:
    movie_list_temp : list = []
    movie_list_dict_in_func : dict = {}
    read_movie_list_csv(movie_list_csv= list_csv, movie_list= movie_list_temp)
    for row in movie_list_temp:
        key : str = row[code_location]
        row.remove(key)
        movie_list_dict_in_func.update({key:row[:]})
    return movie_list_dict_in_func

def list_dictionary_update(dictionary : dict, key_location : int, list_to_add : list) -> None:
    list_to_add_temp : list = list_to_add[:]
    key : str = list_to_add_temp[key_location]
    list_to_add_temp.remove(key)
    dictionary.update({key:list_to_add_temp})





def init_all_dictionary():
    global MOVIE_LIST_DICTIONARY,BOOKING_DATA_DICTIONARY,CINEMA_DEVICE_DICTIONARY,MOVIE_SEATS_DICTIONARY
    MOVIE_LIST_DICTIONARY = list_dictionary_create (list_csv= "movie_list.csv", code_location = 0)
    BOOKING_DATA_DICTIONARY = list_dictionary_create (list_csv= "booking_data.csv", code_location = 0)
    CINEMA_DEVICE_DICTIONARY = list_dictionary_create (list_csv= "cinema_device_list.csv", code_location = 0)
    MOVIE_SEATS_DICTIONARY = seat_dictionary_create(seats_csv= "movie_seat.csv")
    print (MOVIE_LIST_DICTIONARY)
    print (BOOKING_DATA_DICTIONARY)
    print (CINEMA_DEVICE_DICTIONARY)
    print (MOVIE_SEATS_DICTIONARY)



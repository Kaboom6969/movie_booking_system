from main_program.Library.movie_booking_framework import valid_checker as vc
from main_program.Library.movie_booking_framework import movie_seats_framework as msf
from main_program.Library.movie_booking_framework import movie_list_framework as mlf
DICTIONARY_INIT_STATUS : bool = False
MOVIE_LIST_DICTIONARY : dict = {}
BOOKING_DATA_DICTIONARY : dict = {}
CINEMA_DEVICE_DICTIONARY : dict = {}
MOVIE_SEATS_DICTIONARY : dict = {}
TEMPLATE_SEATS_DICTIONARY : dict = {}
MOVIE_TEMPLATE_CODE_DICTIONARY : dict = {}

def seat_dictionary_init (seats_csv : str) -> tuple[dict,dict]:
    key: str = ""
    movie_seats_temp: list = []
    seats_dict_in_func : dict = {}
    movie_template_code_in_func : dict = {}
    movie_seats_raw_data: list = msf.read_movie_seats_csv_raw_data(movie_seats_csv= seats_csv,skip_check= True)
    seats_dict_in_func.update({"base file name" : seats_csv})
    seats_dict_in_func.update({"header":movie_seats_raw_data[0]})
    read_data_mode : bool = False
    for row in movie_seats_raw_data[1:]:
        if row[0] == "CODE":
            key = row[1]
            if row[1].isdigit(): #detect the row[1] is movie code or not(because this function also been use by template seats
                movie_template_code_in_func.update({key:row[2]}) #{001 : TEMPLATE001}
            read_data_mode = True
        if read_data_mode and row[0] == "DATA":
            movie_seats_temp.append(row[1:])
        if read_data_mode and row[0] == "END":
            seats_dict_in_func.update({key:movie_seats_temp[:]})
            key = ""
            read_data_mode = False
            movie_seats_temp.clear()
    return seats_dict_in_func,movie_template_code_in_func

def seat_dictionary_update (dictionary : dict, key_to_add : str, seats_data_to_add : list) -> dict:
    dictionary.update({key_to_add:seats_data_to_add})
    return dictionary

# python 3.9++ for this function !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def dictionary_update_with_dict (dictionary : dict,dictionary_to_add : dict) -> dict:
    return dictionary | dictionary_to_add

def dictionary_delete (dictionary : dict,key_to_delete : str,skip_key_not_found_error : bool = False) -> dict:
    try:
        debug_data = dictionary.pop(key_to_delete)
    except KeyError:
        if skip_key_not_found_error: pass
        else: raise ValueError(f"{key_to_delete} not found in dictionary!")
    return dictionary


def list_dictionary_init (list_csv : str, code_location : int) -> dict:
    movie_list_temp : list = []
    movie_list_dict_in_func : dict = {}
    mlf.read_movie_list_csv(movie_list_csv= list_csv, movie_list= movie_list_temp,read_header= True)
    movie_list_dict_in_func.update({"base file name" : list_csv})
    movie_list_dict_in_func.update({"header":movie_list_temp[0][:]})
    movie_list_dict_in_func.update({"code_location" : code_location})
    for row in movie_list_temp[1:]:
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
    global MOVIE_LIST_DICTIONARY,BOOKING_DATA_DICTIONARY,CINEMA_DEVICE_DICTIONARY,MOVIE_SEATS_DICTIONARY,\
        DICTIONARY_INIT_STATUS,TEMPLATE_SEATS_DICTIONARY,MOVIE_TEMPLATE_CODE_DICTIONARY
    MOVIE_LIST_DICTIONARY = list_dictionary_init (list_csv="movie_list.csv", code_location = 0)
    BOOKING_DATA_DICTIONARY = list_dictionary_init (list_csv="booking_data.csv", code_location = 0)
    CINEMA_DEVICE_DICTIONARY = list_dictionary_init (list_csv="cinema_device_list.csv", code_location = 0)
    MOVIE_SEATS_DICTIONARY,MOVIE_TEMPLATE_CODE_DICTIONARY = seat_dictionary_init(seats_csv="movie_seat.csv")
    TEMPLATE_SEATS_DICTIONARY,_ = seat_dictionary_init(seats_csv="template_seats.csv")
    DICTIONARY_INIT_STATUS = True
    # print (MOVIE_LIST_DICTIONARY)
    # print (BOOKING_DATA_DICTIONARY)
    # print (CINEMA_DEVICE_DICTIONARY)
    # print (MOVIE_SEATS_DICTIONARY)

def read_list_from_cache (dictionary_cache : dict, code : str = "all", code_location : int = 0) -> list:
    cache_list: list = []
    list_for_all : list = []
    try:
        if code == "all":
            keys : list = list(dictionary_cache.keys())
            values : list = list(dictionary_cache.values())
            for key_element,value_element in zip(keys,values):
                cache_list.extend(value_element)
                cache_list.insert(code_location,key_element)
                list_for_all.append(cache_list[:])
                cache_list.clear()
            return list_for_all
        else:
            keys : str = code
            values : list = dictionary_cache[code]
            cache_list.extend(values)
            cache_list.insert(code_location,keys)
            return [cache_list]
    except KeyError:
        raise KeyError(f"Cannot Find the code:{code} in code location:{code_location}!")

def read_seats_from_cache (cache_dictionary : dict,code : str) -> list:
    cache_list: list = []
    for value in cache_dictionary[code]:
        cache_list.append(value)
    return cache_list




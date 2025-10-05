from main_program.Library.movie_booking_framework import valid_checker as vc
from main_program.Library.movie_booking_framework import movie_seats_framework as msf
from main_program.Library.movie_booking_framework import movie_list_framework as mlf
DICTIONARY_INIT_STATUS : bool = False
MOVIE_LIST_DICTIONARY : dict = {}
BOOKING_DATA_DICTIONARY : dict = {}
CINEMA_DEVICE_DICTIONARY : dict = {}
MOVIE_SEATS_DICTIONARY : dict = {}
CINEMA_SEATS_DICTIONARY : dict = {}
MOVIE_CINEMA_CODE_DICTIONARY : dict = {}
MOVIE_DEVICE_CODE_DICTIONARY : dict = {}

def seat_dictionary_init (seats_csv : str) -> tuple[dict,dict]:
    key: str = ""
    movie_seats_temp: list = []
    seats_dict_in_func : dict = {}
    movie_cinema_code_in_func : dict = {}
    movie_seats_raw_data: list = msf.read_movie_seats_csv_raw_data(movie_seats_csv= seats_csv,skip_check= True)
    seats_dict_in_func.update({"base file name" : seats_csv})
    seats_dict_in_func.update({"header":movie_seats_raw_data[0]})
    read_data_mode : bool = False
    for row in movie_seats_raw_data[1:]:
        if row[0] == "CODE":
            key = row[1]
            if row[1].isdigit(): #detect the row[1] is movie code or not(because this function also been use by cinema seats
                movie_cinema_code_in_func.update({key:row[2]}) #{001 : CINEMA001}
            read_data_mode = True
        if read_data_mode and row[0] == "DATA":
            movie_seats_temp.append(row[1:])
        if read_data_mode and row[0] == "END":
            seats_dict_in_func.update({key:movie_seats_temp[:]})
            key = ""
            read_data_mode = False
            movie_seats_temp.clear()
    return seats_dict_in_func,movie_cinema_code_in_func

def seat_dictionary_update (seats_dictionary : dict, mt_code_dictionary : dict, code_to_update : str, seats_data_to_add : list, cinema_code : str = None) -> dict:
    seats_dictionary.update({code_to_update:seats_data_to_add})
    if cinema_code is not None: mt_code_dictionary.update({code_to_update:cinema_code})
    return seats_dictionary

def dictionary_update_with_dict (dictionary : dict,dictionary_to_add : dict) -> None:
    dictionary.update(dictionary_to_add)


def dictionary_delete (dictionary : dict,key_to_delete : str,skip_key_not_found_error : bool = False) -> dict:
    try:
        debug_data = dictionary.pop(key_to_delete)
    except KeyError:
        if skip_key_not_found_error: pass
        else: raise ValueError(f"{key_to_delete} not found in dictionary!")
    return dictionary


def list_dictionary_init (list_csv : str, code_location : int) -> dict:
    try:
        movie_list_temp : list = []
        movie_list_dict_in_func : dict = {}
        mlf.read_movie_list_csv(movie_list_csv= list_csv, movie_list= movie_list_temp,read_header= True)
        movie_list_dict_in_func.update({"base file name" : list_csv})
        movie_list_dict_in_func.update({"header":movie_list_temp[0][:]})
        movie_list_dict_in_func.update({"code_location" : code_location})
        try:
            for row in movie_list_temp[1:]:
                key : str = row[code_location]
                row.remove(key)
                movie_list_dict_in_func.update({key:row[:]})
        except IndexError:
            raise IndexError(f"code_location : {code_location} is not in the range!")

    except Exception as e:
        raise Exception(f"LIST DICTIONARY INIT FAILED! ERROR:{str(e)}")
    return movie_list_dict_in_func

def primary_foreign_key_dictionary_init (list_dict : dict, PK_location : int, FK_location : int) -> dict:
    try:
        list_temp : list = read_list_from_cache(dictionary_cache= list_dict)
        dictionary_in_func : dict = {}
        try:
            for row in list_temp:
                dictionary_in_func.update({row[PK_location]:row[FK_location]})
        except IndexError:
            raise IndexError(f"PK_location : {PK_location} or FK_location : {FK_location} is not in the range!")

    except Exception as e:
        raise Exception(f"PF KEY DICTIONARY INIT FAILED! ERROR:{str(e)}")
    return dictionary_in_func


def list_dictionary_update(dictionary : dict,list_to_add : list) -> None:
    key_location = dictionary.get("code_location")
    list_to_add_temp : list = list_to_add[:]
    key : str = list_to_add_temp[key_location]
    list_to_add_temp.remove(key)
    dictionary.update({key:list_to_add_temp})





def init_all_dictionary():
    global MOVIE_LIST_DICTIONARY,BOOKING_DATA_DICTIONARY,CINEMA_DEVICE_DICTIONARY,MOVIE_SEATS_DICTIONARY,\
        DICTIONARY_INIT_STATUS,CINEMA_SEATS_DICTIONARY,MOVIE_CINEMA_CODE_DICTIONARY,MOVIE_DEVICE_CODE_DICTIONARY
    MOVIE_LIST_DICTIONARY = list_dictionary_init (list_csv="movie_list.csv", code_location = 0)
    BOOKING_DATA_DICTIONARY = list_dictionary_init (list_csv="booking_data.csv", code_location = 0)
    CINEMA_DEVICE_DICTIONARY = list_dictionary_init (list_csv="cinema_device_list.csv", code_location = 0)
    MOVIE_SEATS_DICTIONARY,_= seat_dictionary_init(seats_csv="movie_seat.csv")
    CINEMA_SEATS_DICTIONARY,_ = seat_dictionary_init(seats_csv="cinema_seats.csv")
    MOVIE_DEVICE_CODE_DICTIONARY = primary_foreign_key_dictionary_init(list_dict = CINEMA_DEVICE_DICTIONARY, PK_location = 1, FK_location = 0)
    MOVIE_CINEMA_CODE_DICTIONARY = primary_foreign_key_dictionary_init(list_dict = MOVIE_LIST_DICTIONARY, PK_location = 0, FK_location = 2)
    DICTIONARY_INIT_STATUS = True
    # print (MOVIE_LIST_DICTIONARY)
    # print (BOOKING_DATA_DICTIONARY)
    # print (CINEMA_DEVICE_DICTIONARY)
    # print (MOVIE_SEATS_DICTIONARY)

def read_list_from_cache (dictionary_cache : dict, code : str = "all",header_insert : bool = True,code_location:int=None) -> list:
    cache_list: list = []
    list_for_all : list = []
    if code_location is None: code_location : int = dictionary_cache.get("code_location")
    try:
        if code == "all":
            for key_element,value_element in dictionary_cache.items():
                if key_element in ["header", "base file name", "code_location"]: continue
                value_temp = value_element[:]
                cache_list.extend(value_temp)
                if header_insert: cache_list.insert(code_location,key_element)
                list_for_all.append(cache_list[:])
                cache_list.clear()
            return list_for_all
        else:
            keys : str = code
            values : list = dictionary_cache[code]
            cache_list.extend(values)
            if header_insert: cache_list.insert(code_location,keys)
            return cache_list
    except KeyError:
        raise KeyError(f"Cannot Find the code:{code} in code location:{code_location}!")

def read_seats_from_cache (cache_dictionary : dict,code : str) -> list:
    cache_list: list = []
    for value in cache_dictionary[code]:
        cache_list.append(value)
    return cache_list

def seats_code_catcher_from_cache (seats_cache : dict) -> list:
    code_list : list = []
    for key in seats_cache.keys():
        if key in ["header","base file name"] : continue
        code_list.append(key)
    return code_list





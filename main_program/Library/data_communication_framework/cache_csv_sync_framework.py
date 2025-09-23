from main_program.Library.movie_booking_framework import movie_list_framework as mlf
from main_program.Library.movie_booking_framework import movie_seats_framework as msf
from main_program.Library.movie_booking_framework import data_dictionary_framework as ddf
import warnings

def update_list_sync (list_csv : str,list_data : list,dictionary_cache : dict,code : str,code_location : int = 0) -> None:
    mlf.update_movie_list_csv(movie_list_csv= list_csv,movie_list= list_data,movie_code= code,code_location= code_location)
    try:
        ddf.list_dictionary_update(dictionary= dictionary_cache,list_to_add= list_data)
    except Exception as e:
        raise ValueError(f"Update cache error!\nError : str{e}")

def add_list_sync (list_csv : str,list_data : list,dictionary_cache : dict,code : str,code_location : int = 0) -> None:
    mlf.add_movie_list_csv(movie_list_csv= list_csv,movie_list= list_data,movie_code= code,code_location= code_location)
    try:
        ddf.list_dictionary_update(dictionary= dictionary_cache,list_to_add= list_data)
    except Exception as e:
        raise ValueError(f"Update cache error!\nError : str{e}")

def delete_list_sync (list_csv : str,dictionary_cache : dict,code : str,code_location : int = 0) -> None:
    mlf.delete_movie_list_csv(movie_list_csv= list_csv,movie_code= code,code_location= code_location)
    try:
        ddf.dictionary_delete(dictionary= dictionary_cache,key_to_delete= code)
    except Exception as e:
        raise ValueError(f"Update cache error!\nError : str{e}")

def read_list_from_cache (dictionary_cache : dict,code : str = "all",code_location : int = 0) -> list:
    return ddf.read_list_from_cache(dictionary_cache= dictionary_cache,code= code,code_location= code_location)
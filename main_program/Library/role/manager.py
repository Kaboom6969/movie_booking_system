import os
import csv
from datetime import datetime
Encapsulation
from main_program.Library.cache_framework.data_dictionary_framework import init_all_dictionary
from main_program.Library.data_communication_framework import cache_csv_sync_framework as ccsf
from main_program.Library.cache_framework import data_dictionary_framework as ddf
from main_program.Library.movie_booking_framework import id_generator as idg
from main_program.Library.movie_booking_framework import valid_checker as vc
from main_program.Library.movie_booking_framework import framework_utils as fu
from main_program.Library.movie_booking_framework import cinema_services as cnsv
from main_program.Library.movie_booking_framework.framework_utils import element_input
from main_program.Library.movie_booking_framework.movie_seats_framework import get_capacity


def get_code_range (dictionary_cache : dict) -> list:
    code_list : list = list(dictionary_cache.keys())
    code_list_copy : list = code_list[:]
    for i in code_list:
        if i in ["header","base file name","code_location"]:
            code_list_copy.remove(i)
    return code_list_copy

def movie_list_print_with_format(data_list : list,
                                 DEFAULT_WIDTH : int = 30,movie_seats_dict : dict = None) -> None:
    if movie_seats_dict is None: movie_seats_dict = ddf.MOVIE_SEATS_DICTIONARY
    print(f"{'Movie Code': <{DEFAULT_WIDTH}}{'Movie Name': <{DEFAULT_WIDTH}}"
          f"{'Cinema Location': <{DEFAULT_WIDTH}}{'Start Time': <{DEFAULT_WIDTH}}"
          f"{'End Time': <{DEFAULT_WIDTH}}{'Date': <{DEFAULT_WIDTH}}"
          f"{'Price': <{DEFAULT_WIDTH}}{'Capacity': <{DEFAULT_WIDTH}}")
    print("-" * (DEFAULT_WIDTH * 8 + 1))
    for row in data_list:
        seat_list_temp : list = ccsf.read_seats_from_cache(cache_dictionary=movie_seats_dict, code=row[0])
        for data in row:
            print(f"{data: <{DEFAULT_WIDTH}}", end="")
        print(f"{get_capacity(seat_list_temp): <{DEFAULT_WIDTH}}", end ="")
        print()

def add_movie_operation (cinema_seats_dict:dict=None,movie_list_dict:dict=None,movie_seats_dict:dict=None,cinema_device_dict:dict=None) -> None:
    if cinema_seats_dict is None: cinema_seats_dict = ddf.CINEMA_SEATS_DICTIONARY
    if movie_list_dict is None: movie_list_dict= ddf.MOVIE_LIST_DICTIONARY
    if movie_seats_dict is None: movie_seats_dict = ddf.MOVIE_SEATS_DICTIONARY
    if cinema_device_dict is None: cinema_device_dict = ddf.CINEMA_DEVICE_DICTIONARY
    movie_code_list = get_code_range(movie_list_dict)
    cinema_code_range_filtered = sorted(list(set(get_code_range(cinema_seats_dict))))
    movie_list_header : list = movie_list_dict["header"]
    movie_code = idg.generate_code_id(movie_code_list,prefix_generate="",code_location=movie_list_dict["code_location"],
                                      number_of_prefix=0,prefix_got_digit= False,code_id_digit_count=4)
    added_movie_list : list = [movie_code]
    for i in movie_list_header[1:]:
        if "date" in i: user_input = fu.element_input(element_name= i, valid_check_func= vc.date_valid_check)
        elif "time" in i: user_input = fu.element_input(element_name= i, valid_check_func= vc.time_valid_check)
        elif "CINEMA" in i: user_input = fu.element_input(element_name= i,input_range= cinema_code_range_filtered)
        else: user_input = fu.element_input(element_name= i)
        added_movie_list.append(user_input)

    ccsf.list_dictionary_update(dictionary= movie_list_dict,list_to_add=added_movie_list)



def delete_movie_operation(movie_list_dict:dict=None,movie_seats_dict:dict=None,cinema_device_dict:dict=None) -> None:
    if movie_list_dict is None: movie_list_dict= ddf.MOVIE_LIST_DICTIONARY
    if movie_seats_dict is None: movie_seats_dict = ddf.MOVIE_SEATS_DICTIONARY
    if cinema_device_dict is None: cinema_device_dict = ddf.CINEMA_DEVICE_DICTIONARY
    movie_list_header : list = movie_list_dict["header"]
    movie_code_range : list = get_code_range(movie_list_dict)
    movie_code_to_delete = fu.element_input(element_name=movie_list_header[0],input_range= movie_code_range)
    movie_list_print_with_format(data_list= [ccsf.read_list_from_cache(dictionary_cache= movie_list_dict,code=movie_code_to_delete)])
    print (f"Are You Sure You Want Delete Movie Code: {movie_code_to_delete}?")
    user_operation :str = fu.element_input(element_name= "command (Y/N)",input_range= ["Y","y","N","n"])
    if user_operation.lower() == "y":
        ccsf.dictionary_delete(dictionary=movie_list_dict,key_to_delete=movie_code_to_delete)
        # This is just for test,after compile,the sync all function will be placed at the bottom of manager()
    if user_operation.lower() == "n":
        return

def modify_movie_operation(movie_list_dict:dict=None,movie_seats_dict:dict=None,cinema_device_dict:dict=None
                           ,cinema_seats_dict:dict=None) -> None:
    if movie_list_dict is None: movie_list_dict= ddf.MOVIE_LIST_DICTIONARY
    if movie_seats_dict is None: movie_seats_dict = ddf.MOVIE_SEATS_DICTIONARY
    if cinema_device_dict is None: cinema_device_dict = ddf.CINEMA_DEVICE_DICTIONARY
    if cinema_seats_dict is None: cinema_seats_dict = ddf.CINEMA_SEATS_DICTIONARY
    movie_list_header : list = movie_list_dict["header"]
    movie_code_range : list = get_code_range(movie_list_dict)
    cinema_code_range_filtered = sorted(list(set(get_code_range(cinema_seats_dict))))
    movie_code_to_modify = fu.element_input(element_name=movie_list_header[0],input_range= movie_code_range)
    movie_list_print_with_format(data_list= [ccsf.read_list_from_cache(dictionary_cache= movie_list_dict,code=movie_code_to_modify)])
    print (f"Are You Sure You Want Modify Movie Code: {movie_code_to_modify}?")
    user_operation: str = fu.element_input(element_name="command (Y/N)", input_range=["Y", "y", "N", "n"])
    if user_operation.lower() == "y":
        movie_list_specify : list = ccsf.read_list_from_cache(dictionary_cache= movie_list_dict,code=movie_code_to_modify)
        selected_modify,header_to_modify = fu.element_input(element_name= "data that you want to modify", input_range= movie_list_header[1:],return_range_index=True)
        if "time" in selected_modify: data_to_modify = fu.element_input(element_name= selected_modify, valid_check_func= vc.time_valid_check)
        elif "date" in selected_modify: data_to_modify = fu.element_input(element_name= selected_modify, valid_check_func= vc.date_valid_check)
        elif "CINEMA" in selected_modify: data_to_modify = fu.element_input(element_name= selected_modify,input_range=cinema_code_range_filtered)
        else: data_to_modify = fu.element_input(element_name= selected_modify)
        movie_list_specify[header_to_modify + 1] = data_to_modify
        ccsf.list_dictionary_update(dictionary=movie_list_dict,list_to_add=movie_list_specify)
    if user_operation.lower() == "n":
        return




def manager() -> None:
    while True:
        print("Welcome to Movie Booking System")
        print("Select Your Operation:")
        print("1. Add Movie\n2. Delete Movie\n3. Modify Movie\n4. Exit")
        user_input = element_input(element_name= "user_operation", input_range= ["1","2","3","4"])
        match user_input:
            case "1":
                add_movie_operation()
            case "2":
                delete_movie_operation()
            case "3":
                modify_movie_operation()
            case "4":
                break
            case _:
                raise ValueError("case _ isn't callable in normal progress!\nPlease Check your element_input parameters!")
        try:
            cnsv.sync_all()
        except ValueError as e:
            if "schedule" in e.args[0] or "Sort" in e.args[0]:
                error_message = e.args[0]
                conflict_data = e.args[1]
                print(error_message)
                print(f"conflict schedule:{conflict_data}\n")
                print("Please Enter Your operation\n1. Manual Sort\n2. Auto Sort(Recommended)\n3. Discard this change")
                user_operation = element_input(element_name= "operation", input_range= ["1", "2", "3"])
                match user_operation:
                    case "1":
                        modify_movie_operation()
                    case "2":
                        auto_sort_status,still_conflict_data = cnsv.schedule_auto_sort(schedule_conflict_list= conflict_data)
                        if not auto_sort_status: raise ValueError("Auto Sort Failed!",still_conflict_data)
                    case "3":
                        ddf.init_all_dictionary()
                try:
                    cnsv.sync_all()
                except ValueError as e: raise e

            else: raise ValueError(e)
        except Exception as e:
            print(f"UNKNOWN ERROR",e)
            print("THE CACHE WILL FORCED ROLLBACK")
            ccsf.init_all_dictionary()



if __name__ == "__main__":
    init_all_dictionary()
    manager()

        


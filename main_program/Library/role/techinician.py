import datetime
import os
from main_program.Library.movie_booking_framework import framework_utils as fu
from main_program.Library.cache_framework import data_dictionary_framework as ddf
from main_program.Library.data_communication_framework import cache_csv_sync_framework as ccsf
from main_program.Library.role.customer import DEFAULT_WIDTH


#这个是利用movie_booking框架的例子，（请将后续的函数都修改至适配此框架）
def view_upcoming_movies(movie_list_dict : dict=None):
    if movie_list_dict is None:movie_list_dict = ddf.MOVIE_LIST_DICTIONARY
    movie_list : list = ccsf.read_list_from_cache(dictionary_cache= movie_list_dict)
    movie_list_filtered : list = []
    time_now = datetime.date.today()
    for row in movie_list:
        if split_date(date= row[5],separate_symbol= '/') > time_now: movie_list_filtered.append(row)
    movie_list_print_technician_ver(data_list= movie_list_filtered)


def split_date (date : str,separate_symbol : str):
    date_split = date.split(separate_symbol)
    return datetime.date(int(date_split[0]),int(date_split[1]),int(date_split[2]))



def movie_list_print_technician_ver(data_list : list) -> None:
    print(f"{'Movie Code': <{DEFAULT_WIDTH}}{'Movie Name': <{DEFAULT_WIDTH}}"
          f"{'Cinema Location': <{DEFAULT_WIDTH}}{'Start Time': <{DEFAULT_WIDTH}}"
          f"{'End Time': <{DEFAULT_WIDTH}}{'Date': <{DEFAULT_WIDTH}}")
    print("-" * (DEFAULT_WIDTH * 6 + 1))
    for row in data_list:
        for data in row[0:6]:
            print(f"{data: <{DEFAULT_WIDTH}}", end="")
        print()


def report_issue(cinema_device_csv : str,cinema_device_dict : dict=None,md_code_dict : dict = None) -> None:
    if cinema_device_dict is None: cinema_device_dict = ddf.CINEMA_DEVICE_DICTIONARY
    if md_code_dict is None: md_code_dict = ddf.MOVIE_DEVICE_CODE_DICTIONARY
    device_list = device_actual_list_get(cinema_device_dict= cinema_device_dict)
    device_str = fu.list_to_str_line(data_list=device_list,blank_need=False)
    movie_code = input("please enter movie code: ")
    issue_device = input(f"Update ({device_str}) Status: ")
    issue_status = input("Change equipment status? (0:good, 1:breakdown, 2:under maintainence): ")
    try:
        status = int(issue_status)
        if status not in [0, 1, 2]:
            raise ValueError (f"Status: {status} should be 0 or 1 or 2")
    except ValueError as e:
        print(f"Invalid Input,{e}")
        return
    update_status(cinema_device_csv= cinema_device_csv,movie_code= movie_code,issue_device= issue_device,
                  issue_status= issue_status,device_list= device_list,cinema_device_dict= cinema_device_dict,
                  md_code_dict= md_code_dict)

def device_actual_list_get (cinema_device_dict : dict) -> list:
    if cinema_device_dict is None: cinema_device_dict = ddf.CINEMA_DEVICE_DICTIONARY
    cinema_device_header : list = cinema_device_dict.get("header")
    cinema_device_filtered : list = fu.keyword_only_for_list(any_dimension_list= cinema_device_header,keyword= "_status")
    device_list : list = fu.keyword_erase_for_list(any_dimension_list= cinema_device_filtered,keyword= "_status")
    return device_list

def update_status(cinema_device_csv : str,movie_code : str,issue_device : str,issue_status : str,device_list : list,
                  cinema_device_dict : dict=None,md_code_dict : dict=None) -> None:
    if cinema_device_dict is None: cinema_device_dict = ddf.CINEMA_DEVICE_DICTIONARY
    if md_code_dict is None: md_code_dict = ddf.MOVIE_DEVICE_CODE_DICTIONARY
    device_location : int = 0
    for index,device in enumerate(device_list):
        if device == issue_device:
            device_location = index + 2
            break
    technician_code : str = md_code_dict.get(movie_code)
    cinema_device_list_specify : list = ccsf.read_list_from_cache(dictionary_cache= cinema_device_dict,
                                                                  code=technician_code)
    cinema_device_list_specify[device_location] = issue_status
    ccsf.list_dictionary_update(dictionary= cinema_device_dict,list_to_add= cinema_device_list_specify)
    ccsf.list_cache_write_to_csv(list_csv=cinema_device_csv,list_dictionary_cache= cinema_device_dict)

def check_equipment_status(cinema_device_dict : dict =None) -> None:
    if cinema_device_dict is None: cinema_device_dict = ddf.CINEMA_DEVICE_DICTIONARY
    cinema_device_header : list = cinema_device_dict.get("header")
    cinema_device_list : list = ccsf.read_list_from_cache(dictionary_cache= cinema_device_dict)
    status_dictionary : dict = {'0' : 'good', '1' : 'breakdown', '2' : 'under maintenance'}
    for row in cinema_device_list:
        print(*(f"{cinema_device_header[i]}:{status_dictionary.get(row[i],row[i])}\n" for i in range(len(cinema_device_header))))





if __name__ == "__main__":
    ddf.init_all_dictionary()
    view_upcoming_movies()
    report_issue(cinema_device_csv= "cinema_device_list.csv")
    check_equipment_status()
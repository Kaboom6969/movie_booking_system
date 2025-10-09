import datetime
import warnings

from main_program.Library.cache_framework.data_dictionary_framework import init_all_dictionary
from main_program.Library.movie_booking_framework import framework_utils as fu
from main_program.Library.cache_framework import data_dictionary_framework as ddf
from main_program.Library.data_communication_framework import cache_csv_sync_framework as ccsf
from main_program.Library.movie_booking_framework import cinema_services as cnsv
from main_program.Library.role.customer import DEFAULT_WIDTH


#这个是利用movie_booking框架的例子，（请将后续的函数都修改至适配此框架）
def view_upcoming_movies(movie_list_dict: dict=None):
    if movie_list_dict is None:movie_list_dict = ddf.MOVIE_LIST_DICTIONARY
    movie_list: list = ccsf.read_list_from_cache(dictionary_cache= movie_list_dict)
    movie_list_filtered: list = []
    time_now = datetime.date.today()
    for row in movie_list:
        if split_date(date= row[5],separate_symbol= '/') > time_now: movie_list_filtered.append(row)
    movie_list_print_technician_ver(data_list= movie_list_filtered)


def split_date (date: str,separate_symbol: str):
    date_split = date.split(separate_symbol)
    return datetime.date(int(date_split[0]),int(date_split[1]),int(date_split[2]))



def movie_list_print_technician_ver(data_list: list) -> None:
    print(f"{'Movie Code': <{DEFAULT_WIDTH}}{'Movie Name': <{DEFAULT_WIDTH}}"
          f"{'Cinema Location': <{DEFAULT_WIDTH}}{'Start Time': <{DEFAULT_WIDTH}}"
          f"{'End Time': <{DEFAULT_WIDTH}}{'Date': <{DEFAULT_WIDTH}}")
    print("-" * (DEFAULT_WIDTH * 6 + 1))
    for row in data_list:
        for data in row[0:6]:
            print(f"{data: <{DEFAULT_WIDTH}}", end="")
        print()


def report_issue_operation(cinema_device_dict: dict=None) -> None:
    if cinema_device_dict is None: cinema_device_dict = ddf.CINEMA_DEVICE_DICTIONARY
    device_list = device_actual_list_get(cinema_device_dict= cinema_device_dict)
    cinema_code_range: list = fu.get_code_range(dictionary_cache= cinema_device_dict)
    cinema_code: str = fu.element_input(element_name= "cinema number",input_range= cinema_code_range)
    device_str = fu.list_to_str_line(data_list=device_list,blank_need=False)
    print(f"Update ({device_str}) Status")
    issue_device = fu.element_input(element_name="command",input_range=device_list)
    update_status(cinema_number= cinema_code,issue_device= issue_device,
                  issue_status= '1',device_list= device_list,cinema_device_dict= cinema_device_dict)

def device_actual_list_get (cinema_device_dict: dict=None) -> list:
    if cinema_device_dict is None: cinema_device_dict = ddf.CINEMA_DEVICE_DICTIONARY
    cinema_device_header: list = cinema_device_dict.get("header")
    cinema_device_filtered: list = fu.keyword_only_for_list(
        any_dimension_list= cinema_device_header,
        keyword= "_status"
    )
    device_list: list = fu.keyword_erase_for_list(any_dimension_list= cinema_device_filtered,keyword= "_status")
    return device_list

def update_status(cinema_number: str,issue_device: str,issue_status: str,device_list: list,
                  cinema_device_dict: dict=None) -> None:
    if cinema_device_dict is None: cinema_device_dict = ddf.CINEMA_DEVICE_DICTIONARY
    device_location: int = 0
    for index,device in enumerate(device_list):
        if device == issue_device:
            device_location = index + 1
            break
    cinema_device_list_specify: list = ccsf.read_list_from_cache(dictionary_cache= cinema_device_dict,
                                                                  code=cinema_number)
    cinema_device_list_specify[device_location] = issue_status
    ccsf.list_dictionary_update(dictionary= cinema_device_dict,list_to_add= cinema_device_list_specify)

def check_equipment_status(cinema_device_dict: dict =None, cinema_number: str = "all") -> list:
    if cinema_device_dict is None: cinema_device_dict = ddf.CINEMA_DEVICE_DICTIONARY
    cinema_device_header: list = cinema_device_dict.get("header")
    if cinema_number == "all": cinema_device_list: list = ccsf.read_list_from_cache(
        dictionary_cache= cinema_device_dict
    )
    else: cinema_device_list: list = ccsf.read_list_from_cache(
        dictionary_cache= cinema_device_dict,
        code=cinema_number
    )
    status_dictionary: dict = {'0': 'good', '1': 'breakdown', '2': 'under maintenance'}
    cinema_device_list = fu.one_dimension_list_to_two_dimension_list(any_dimension_list= cinema_device_list)
    for row in cinema_device_list:
        print(
            *(f"{cinema_device_header[i]}:"
              f"{status_dictionary.get(row[i],row[i])}\n"
              for i in range(len(cinema_device_header))
            )
        )
    return cinema_device_list

def check_equipment_status_operation(cinema_device_dict: dict =None) -> None:
    if cinema_device_dict is None: cinema_device_dict = ddf.CINEMA_DEVICE_DICTIONARY
    technician_code_range: list = fu.get_code_range(dictionary_cache= cinema_device_dict)
    cinema_device_code: str = fu.element_input(element_name= "cinema number",input_range=technician_code_range)
    check_equipment_status(cinema_number= cinema_device_code)
    input ("\nEnter Any key to continue...")


def confirm_equipment_status(cinema_device_dict: dict =None) -> None:
    if cinema_device_dict is None: cinema_device_dict = ddf.CINEMA_DEVICE_DICTIONARY
    cinema_device_list: list = ddf.read_list_from_cache(dictionary_cache= cinema_device_dict)
    cinema_header_location: dict = fu.header_location_get(header_list= cinema_device_dict["header"])
    for row in cinema_device_list:
        good_status: bool = cinema_status_check(cinema_device_list_one_dimension= row)
        if good_status:
            print (f"{row[cinema_header_location["cinema_number"]]} is all good!")
        else:
            print(f"{row[cinema_header_location["cinema_number"]]} got problem!")
    input ("\nEnter Any key to continue...")

def cinema_status_check(cinema_device_list_one_dimension: list) -> bool:
    for element in cinema_device_list_one_dimension:
        if element == '1' or element == '2': return False
    return True

def update_issue_status_operation(cinema_device_dict: dict = None) -> None:
    if cinema_device_dict is None: cinema_device_dict = ddf.CINEMA_DEVICE_DICTIONARY
    cinema_device_list: list = ddf.read_list_from_cache(dictionary_cache= cinema_device_dict)
    cinema_header_location: dict = fu.header_location_get(header_list= cinema_device_dict["header"])
    device_list = device_actual_list_get(cinema_device_dict=cinema_device_dict)
    problem_cinema: list = []
    for row in cinema_device_list:
        if not cinema_status_check(cinema_device_list_one_dimension= row):
            problem_cinema.append(row[cinema_header_location["cinema_number"]])
    print(f"Problem Cinema: {problem_cinema}")
    user_cinema: str = fu.element_input(element_name= "cinema number with problem",input_range=problem_cinema)
    user_cinema_device_status: list = cinema_device_dict[user_cinema]
    device_list_filtered: list = device_list_filtered_for_problem_device(
        device_actual_list= device_list,
        device_status=user_cinema_device_status
    )
    print(f"Problem Device: {device_list_filtered}")
    device_to_update = fu.element_input(element_name="command", input_range=device_list_filtered)
    status_to_update: str  = str(int(fu.get_operation_choice(
        'Please Select Your Status',
        'good',
        'breakdown',
        'under maintenance'
    )) - 1)
    update_status(
        cinema_number= user_cinema,
        issue_device= device_to_update,
        issue_status=status_to_update,
        device_list= device_list
    )


def device_list_filtered_for_problem_device (device_actual_list: list,device_status: list) -> list:
    device_list_filtered: list = []
    for status,device in zip(device_status,device_actual_list):
        if status == '0': continue
        device_list_filtered.append(device)
    return device_list_filtered





def technician() -> None:
    print("Welcome to Movie Booking System")
    while True:
        try:
            match fu.get_operation_choice(
                "Select Your Operation",
                'View Upcoming Movie',
                'Report Issue',
                'Check Equipment Status',
                'Confirm Equipment Status',
                'Update Issue Status',
                'Exit'
            ):
                case '1':
                    view_upcoming_movies()
                case '2':
                    report_issue_operation()
                case '3':
                    check_equipment_status_operation()
                case '4':
                    confirm_equipment_status()
                case '5':
                    update_issue_status_operation()
                case '6':
                    break
        except Exception as e:
            raise Exception("ERROR DETECTED,ERROR:",e)
        try:
            cnsv.sync_all()
        except ValueError as e:
            if "schedule" in e.args[0] or "Sort" in e.args[0]:
                error_message = e.args[0]
                conflict_data = e.args[1]
                print(error_message)
                while True:
                    print("This don't have the permissions to solve it.\nYou should call Manager to solve it.")
                    print("1.Disregard the risk and proceed\n2.Exit and discard all the changes")
                    user_command = fu.element_input(element_name="command",input_range=['1','2'])
                    match user_command:
                        case '1':
                            warnings.warn("THIS IS A VERY RISKY OPERATION,PLEASE ENTER 'CONFIRM' TO DO IT")
                            if input("CONFIRM YOU WANT TO DO IT:") == "CONFIRM":
                                cnsv.sync_all(skip_conflict_test=True)
                                break
                            continue
                        case '2':
                            print("Please call Manager to solve it.")
                            init_all_dictionary()
                    break



if __name__ == "__main__":
    init_all_dictionary()
    technician()
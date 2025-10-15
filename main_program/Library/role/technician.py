import datetime
import warnings

from main_program.Library.movie_booking_framework import framework_utils as fu
from main_program.Library.cache_framework import data_dictionary_framework as ddf
from main_program.Library.data_communication_framework import cache_csv_sync_framework as ccsf
from main_program.Library.movie_booking_framework import cinema_services as cnsv

#这个是利用movie_booking框架的例子，（请将后续的函数都修改至适配此框架）
def view_upcoming_movies(movie_list_dict: dict):
    movie_list: list = ccsf.read_list_from_cache(dictionary_cache= movie_list_dict)     #get all rows data
    movie_list_filtered: list = []      # container for future shows
    time_now = datetime.date.today()    # today date for comparison
    for row in movie_list:      # iterate all movie rows
        # keep if show date is after today
        if split_date(date= row[5],separate_symbol= '/') > time_now:
            movie_list_filtered.append(row)    # collect future rows
    movie_list_print_technician_ver(data_list= movie_list_filtered)


def split_date (date: str,separate_symbol: str):
    date_split = date.split(separate_symbol)    #split into [YYYY,MM,DD]
    return datetime.date(int(date_split[0]),int(date_split[1]),int(date_split[2]))  #build date



def movie_list_print_technician_ver(data_list: list) -> None:
    # header line will fixed widths from fu.DEFAULT_WIDTH
    print(f"{'Movie Code': <{fu.DEFAULT_WIDTH}}{'Movie Name': <{fu.DEFAULT_WIDTH}}"
          f"{'Cinema Location': <{fu.DEFAULT_WIDTH}}{'Start Time': <{fu.DEFAULT_WIDTH}}"
          f"{'End Time': <{fu.DEFAULT_WIDTH}}{'Date': <{fu.DEFAULT_WIDTH}}")    #Print column headers
    print("-" * (fu.DEFAULT_WIDTH * 6 + 1)) #underlines
    for row in data_list:   #each movie
        for data in row[0:6]:   #only first 6 columns are printed
            print(f"{data: <{fu.DEFAULT_WIDTH}}", end="")   #fixed-width cell
        print() #newline after each row


def report_issue_operation(cinema_device_dict: dict) -> None:
    device_list = device_actual_list_get(cinema_device_dict= cinema_device_dict)     # e.g. ['projector','server',...]
    cinema_code_range: list = fu.get_code_range(dictionary_cache= cinema_device_dict)   # valid cinema IDs
    cinema_code: str = fu.element_input(element_name= "cinema number",input_range= cinema_code_range)    # choose one cinema
    device_str = fu.list_to_str_line(data_list=device_list,blank_need=False)    # 'projector/aircond/...'
    print(f"Update ({device_str}) Status")  #promt
    issue_device = fu.element_input(element_name="command",input_range=device_list) #choose device
    # write status '1' (breakdown) back to the cache
    update_status(cinema_number= cinema_code,issue_device= issue_device,
                  issue_status= '1',device_list= device_list,cinema_device_dict= cinema_device_dict)

def device_actual_list_get (cinema_device_dict: dict) -> list:
    cinema_device_header: list = cinema_device_dict.get("header")   #header row
    cinema_device_filtered: list = fu.keyword_only_for_list(    #keep columns that end with '_status'
        any_dimension_list= cinema_device_header,
        keyword= "_status"
    )
    device_list: list = fu.keyword_erase_for_list(any_dimension_list= cinema_device_filtered,keyword= "_status")    # strip suffix
    return device_list

def update_status(cinema_number: str,issue_device: str,issue_status: str,device_list: list,
                  cinema_device_dict: dict) -> None:
    device_location: int = 0    #position of the device's status column
    for index,device in enumerate(device_list):     # map device name --> column index
        if device == issue_device:
            device_location = index + 1     #+1 because column 0 is usually cinema id
            break
    # fetch the specific cinema row
    cinema_device_list_specify: list = ccsf.read_list_from_cache(dictionary_cache= cinema_device_dict,
                                                                  code=cinema_number)
    cinema_device_list_specify[device_location] = issue_status      #set status code
    ccsf.list_dictionary_update(dictionary= cinema_device_dict,list_to_add= cinema_device_list_specify)     #save

def check_equipment_status(cinema_device_dict: dict, cinema_number: str = "all") -> list:
    cinema_device_header: list = cinema_device_dict.get("header")
    if cinema_number == "all":  #get all rows
        cinema_device_list: list = ccsf.read_list_from_cache(dictionary_cache= cinema_device_dict
    )
    else:   # get one row by code
        cinema_device_list: list = ccsf.read_list_from_cache(
        dictionary_cache= cinema_device_dict,
        code=cinema_number
    )
    status_dictionary: dict = {'0': 'good', '1': 'breakdown', '2': 'under maintenance'}     #mapping
    cinema_device_list = fu.one_dimension_list_to_two_dimension_list(any_dimension_list= cinema_device_list)    #reshape
    for row in cinema_device_list:  #for each cinema row
        print(
            *(f"{cinema_device_header[i]}:"     #header:
              f"{status_dictionary.get(row[i],row[i])}\n"      #map code --> label
              for i in range(len(cinema_device_header))
            )
        )   # print as multiple 'Header: Value' lines
    return cinema_device_list   #return list

def check_equipment_status_operation(cinema_device_dict: dict) -> None:
    # Wrapper that asks for a cinema code then calls check_equipment_status(...)
    technician_code_range: list = fu.get_code_range(dictionary_cache= cinema_device_dict)   #valid cinema IDs
    cinema_device_code: str = fu.element_input(element_name= "cinema number",input_range=technician_code_range) # choose
    check_equipment_status(cinema_device_dict= cinema_device_dict,cinema_number= cinema_device_code)    #print status


def confirm_equipment_status(cinema_device_dict: dict) -> None:
    cinema_device_list: list = ddf.read_list_from_cache(dictionary_cache= cinema_device_dict)
    cinema_header_location: dict = fu.header_location_get(header_list= cinema_device_dict["header"])
    for row in cinema_device_list:  #check each cinema row
        good_status: bool = cinema_status_check(cinema_device_list_one_dimension= row)  # True if all 0
        if good_status:
            print (f"{row[cinema_header_location["cinema_number"]]} is all good!") # all devices good
        else:
            print(f"{row[cinema_header_location["cinema_number"]]} got problem!")   # at least one device is not '0'

def cinema_status_check(cinema_device_list_one_dimension: list) -> bool:
    ### Return True only if every device status in the row equals '0' (good)
    for element in cinema_device_list_one_dimension:
        if element == '1' or element == '2':
            return False
    return True

def update_issue_status_operation(cinema_device_dict: dict) -> None:
    cinema_device_list: list = ddf.read_list_from_cache(dictionary_cache= cinema_device_dict)
    cinema_header_location: dict = fu.header_location_get(header_list= cinema_device_dict["header"])
    device_list = device_actual_list_get(cinema_device_dict=cinema_device_dict)
    problem_cinema: list = []   #collect cinemas that need fix
    for row in cinema_device_list:  #scan all rows
        if not cinema_status_check(cinema_device_list_one_dimension= row):  #if any status not '0'
            problem_cinema.append(row[cinema_header_location["cinema_number"]]) #remember cinema code
    print(f"Problem Cinema: {problem_cinema}")  #quick summary
    user_cinema: str = fu.element_input(element_name= "cinema number with problem",input_range=problem_cinema)  #choose
    user_cinema_device_status: list = cinema_device_dict[user_cinema]   # status list for that cinema (raw row)
    device_list_filtered: list = device_list_filtered_for_problem_device(
        device_actual_list= device_list,
        device_status=user_cinema_device_status
    )
    print(f"Problem Device: {device_list_filtered}")    #show only devices needing updates
    # choose which device to update
    device_to_update = fu.element_input(element_name="command", input_range=device_list_filtered)
    # Choose the new status (menu returns 1..3, so we subtract 1 -> '0','1','2').
    status_to_update: str  = str(int(fu.get_operation_choice(
        'Please Select Your Status',
        'good',
        'breakdown',
        'under maintenance'
    )) - 1)

    # Persist the change back to the cache dictionary.
    update_status(
        cinema_number= user_cinema,
        issue_device= device_to_update,
        issue_status=status_to_update,
        device_list= device_list,
        cinema_device_dict= cinema_device_dict,
    )


def device_list_filtered_for_problem_device (device_actual_list: list,device_status: list) -> list:
    # Zip devices with their status and return only those whose status != '0'
    device_list_filtered: list = []
    for status,device in zip(device_status,device_actual_list): #pair wise (status,name)
        if status == '0': #skip healthy device
            continue
        device_list_filtered.append(device) #keep problem device
    return device_list_filtered





def technician(technician_id : str,
               movie_list_dict:dict= None,
               cinema_device_dict:dict= None,
    ) -> None:
    """
    Technician Console Menu
    """
    if movie_list_dict is None: movie_list_dict= ddf.MOVIE_LIST_DICTIONARY
    if cinema_device_dict is None: cinema_device_dict= ddf.CINEMA_DEVICE_DICTIONARY

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
                case '1':   #show future movie
                    view_upcoming_movies(
                        movie_list_dict= movie_list_dict
                    )
                case '2':   #mark breakdown
                    report_issue_operation(
                        cinema_device_dict= cinema_device_dict
                    )
                case '3':   #detailed view
                    check_equipment_status_operation(
                        cinema_device_dict= cinema_device_dict
                    )
                case '4':   #quick health summary
                    confirm_equipment_status(
                        cinema_device_dict= cinema_device_dict
                    )
                case '5':   #update problem devices
                    update_issue_status_operation(
                        cinema_device_dict= cinema_device_dict
                    )
                case '6':   #exit loop
                    break
            fu.empty_input("Press Enter to continue...")    #pause between actions
        except Exception as e:
            raise Exception("ERROR DETECTED,ERROR:",e)
        # Attempt an ordinary sync
        try:
            cnsv.sync_all()
        except ValueError as e:
            # When sync hits schedule/sort conflicts, the original code asks the user what to do next.
            if "schedule" in e.args[0] or "Sort" in e.args[0]:
                error_message = e.args[0]
                conflict_data = e.args[1]
                print(error_message)    #show conflict summary
                while True:
                    print("This don't have the permissions to solve it.\nYou should call Manager to solve it.")
                    print("1.Disregard the risk and proceed\n2.Exit and discard all the changes")
                    user_command = fu.element_input(element_name="command",input_range=['1','2'])
                    match user_command:
                        case '1':
                            warnings.warn("THIS IS A VERY RISKY OPERATION,PLEASE ENTER 'CONFIRM' TO DO IT")
                            if input("CONFIRM YOU WANT TO DO IT:") == "CONFIRM":
                                cnsv.sync_all(skip_conflict_test=True)  #force sync
                                break   #exit recovery loop
                            continue
                        case '2':
                            print("Please call Manager to solve it.")
                            ccsf.init_all_dictionary()  #re-init to a safe state
                    break



if __name__ == "__main__":
    ccsf.init_all_dictionary()
    technician()
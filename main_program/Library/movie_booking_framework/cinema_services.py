from .id_generator import *
from .movie_seats_framework import *
from .movie_list_framework import *
from main_program.Library.data_communication_framework import cache_csv_sync_framework as ccsf
from main_program.Library.cache_framework import data_dictionary_framework as ddf
from .valid_checker import movie_seats_csv_valid_check
from ..cache_framework.data_dictionary_framework import primary_foreign_key_dictionary_init, read_list_from_cache
from main_program.Library.movie_booking_framework import framework_utils as fu

def sync_all(movie_list_dict : dict=None, movie_seats_dict : dict=None, cinema_device_dict : dict =None,
             cinema_seats_dict : dict=None, mc_code_dict : dict=None, md_code_dict : dict=None, booking_data_dict : dict=None) -> None:
    if movie_list_dict is None: movie_list_dict = ddf.MOVIE_LIST_DICTIONARY
    if movie_seats_dict is None: movie_seats_dict = ddf.MOVIE_SEATS_DICTIONARY
    if cinema_device_dict is None: cinema_device_dict = ddf.CINEMA_DEVICE_DICTIONARY
    if cinema_seats_dict is None: cinema_seats_dict = ddf.CINEMA_SEATS_DICTIONARY
    if mc_code_dict is None: mc_code_dict = ddf.MOVIE_CINEMA_CODE_DICTIONARY
    if md_code_dict is None: md_code_dict = ddf.MOVIE_DEVICE_CODE_DICTIONARY
    if booking_data_dict is None: booking_data_dict = ddf.BOOKING_DATA_DICTIONARY

    movie_schedule_conflict_check_status,schedule_conflict_data = conflict_check_for_movie_schedule()
    if not movie_schedule_conflict_check_status:
        raise ValueError("Schedule conflict detected:",schedule_conflict_data)
    sync_file()
    ddf.MOVIE_CINEMA_CODE_DICTIONARY = primary_foreign_key_dictionary_init(list_dict= movie_list_dict, PK_location=0,
                                                                           FK_location=2)
    link_status,link_conflict_data = link_seats()
    if not link_status:
        raise ValueError("Link conflict detected:",link_conflict_data)


def link_seats (booking_id_location : int = 0,
                book_movie_code_location : int = 2, book_x_seats_location : int = 5, book_y_seats_location : int = 6,
                movie_seats_dict=None, booking_data_dict=None, cinema_seats_dict=None, mc_code_dict=None) -> tuple[bool,list]:
    if booking_data_dict is None: booking_data_dict = ddf.BOOKING_DATA_DICTIONARY
    if cinema_seats_dict is None: cinema_seats_dict = ddf.CINEMA_SEATS_DICTIONARY
    if movie_seats_dict is None: movie_seats_dict = ddf.MOVIE_SEATS_DICTIONARY
    if mc_code_dict is None : mc_code_dict = ddf.MOVIE_CINEMA_CODE_DICTIONARY
    booking_data_csv = booking_data_dict["base file name"]
    movie_seats_csv = movie_seats_dict["base file name"]
    booking_data_list : list = ccsf.read_list_from_cache(dictionary_cache= booking_data_dict)
    conflict_booking_id_list : list = []
    #First init the seats file (all the data of seats clear)
    movie_seats_cache_whole_init(movie_seats_dict= movie_seats_dict, cinema_seats_dict= cinema_seats_dict, mc_code_dict= mc_code_dict)
    for row in booking_data_list:
        #get the data of booking (movie code,x,y) from booking data list)
        #[movie_code,x_axis,y_axis]
        bkid_mvcode_x_y_list : list = get_booking_id_movie_code_x_y_value_list(booking_data_array= row,booking_id_location= booking_id_location,
                                                               movie_code_location= book_movie_code_location,
                                                               x_seats_location= book_x_seats_location,
                                                               y_seats_location= book_y_seats_location)
        #read the current movie seats (from the bkid_mvcode_x_y_list)
        current_movie_seats : list = ccsf.read_seats_from_cache(cache_dictionary= movie_seats_dict,code= bkid_mvcode_x_y_list[1])
        conflict_detect,conflict_data = conflict_detect_for_link_seats(current_movie_seats= current_movie_seats,bkid_mvcode_x_y_list= bkid_mvcode_x_y_list)
        if not conflict_detect:
            modify_movie_seats_list(movie_seat_list=current_movie_seats,x_axis=bkid_mvcode_x_y_list[2],y_axis=bkid_mvcode_x_y_list[3],target_number= 1)
            # update it to the movie seats csv
            ccsf.seat_dictionary_update(seats_dictionary= movie_seats_dict, mt_code_dictionary=mc_code_dict,
                                        code_to_update=bkid_mvcode_x_y_list[1], seats_data_to_add=current_movie_seats)
        else:conflict_booking_id_list.append(conflict_data)
    ccsf.list_cache_write_to_csv(list_csv= booking_data_csv,list_dictionary_cache= booking_data_dict)
    ccsf.seats_cache_write_to_csv(seats_csv= movie_seats_csv, seats_dictionary_cache= movie_seats_dict,
                                  mt_code_dictionary_cache= mc_code_dict)
    if conflict_booking_id_list: return False,conflict_booking_id_list
    else: return True,[]

def movie_seats_cache_whole_init (movie_seats_dict : dict, cinema_seats_dict : dict, mc_code_dict : dict) -> None:
    for movie_code,cinema_code in mc_code_dict.items():
        #init the movie seats(one only,but using for loop so can init all the file)
        movie_seats_init(movie_code= movie_code, cinema_code= cinema_code.upper(), movie_seats_dict= movie_seats_dict,
                         cinema_seats_dict= cinema_seats_dict, mc_code_dict= mc_code_dict)


def movie_seats_init(movie_code : str, cinema_code : str,
                     movie_seats_dict : dict, cinema_seats_dict : dict, mc_code_dict : dict) -> None:
    # read the template data
    cinema_seats : list = ccsf.read_seats_from_cache(cache_dictionary= cinema_seats_dict, code= cinema_code.upper())
    #overwrite the old data with template data
    ccsf.seat_dictionary_update(seats_dictionary= movie_seats_dict, mt_code_dictionary=mc_code_dict, code_to_update= movie_code,
                                seats_data_to_add= cinema_seats)




#IMPORTANT:please check the movie_code_location,x_seats_location,and y_seats_location is the correct location or not!
#I have no error detection for this EXCEPTION!!!!!!
def get_booking_id_movie_code_x_y_value_list (booking_data_array : list,booking_id_location : int,movie_code_location : int, x_seats_location : int, y_seats_location : int) -> list:
    #check the booking_data_array is one dimension list or not (no 2d list allow)
    if any(isinstance(element, (list,tuple)) for element in booking_data_array):
        #if the booking_data_array is 2d list,interrupt the action and raise error
        raise TypeError (f"booking_data_array: {booking_data_array} must be a array (no 2d list allowed)")
    bkid_mvcode_x_y_list : list = []
    #add the booking id
    bkid_mvcode_x_y_list.append(booking_data_array[booking_id_location])
    #add the movie code
    bkid_mvcode_x_y_list.append(booking_data_array[movie_code_location])
    #add the x axis
    bkid_mvcode_x_y_list.append(int(booking_data_array[x_seats_location]))
    #add the y axis
    bkid_mvcode_x_y_list.append(int(booking_data_array[y_seats_location]))
    #return the list
    return bkid_mvcode_x_y_list


#yup,just calculate the mismatched
def mismatched_calculate (main_list : list, compared_list : list) -> list:
    calculated_list : list = []
    for item in main_list:
        #if the element of main_list is not in compared_list,it shows that the element is mismatched
        if item not in compared_list:
            #append the mismatched element into the list
            calculated_list.append(item)
    #return the mismatched list
    return calculated_list






#sync the movie list,movie seats, and cinema device list
#The SSOT is movie list
def sync_file (movie_list_dict : dict=None, movie_seats_dict : dict=None, cinema_device_dict : dict =None,
               template_seats_dict : dict=None, mt_code_dict : dict=None, md_code_dict : dict=None) -> None:
    if movie_seats_dict is None: movie_seats_dict = ddf.MOVIE_SEATS_DICTIONARY
    if movie_list_dict is None: movie_list_dict = ddf.MOVIE_LIST_DICTIONARY
    if cinema_device_dict is None: cinema_device_dict = ddf.CINEMA_DEVICE_DICTIONARY
    if template_seats_dict is None: template_seats_dict = ddf.CINEMA_SEATS_DICTIONARY
    if mt_code_dict is None: mt_code_dict = ddf.MOVIE_CINEMA_CODE_DICTIONARY
    if md_code_dict is None: md_code_dict = ddf.MOVIE_DEVICE_CODE_DICTIONARY

    movie_list_csv = movie_list_dict["base file name"]
    movie_seats_csv = movie_seats_dict["base file name"]
    cinema_device_list_csv = cinema_device_dict["base file name"]

    #read the data from csv file
    #
    # read the daw data of movie seats first
    # read all the list from movie list
    movie_list: list = ccsf.read_list_from_cache(dictionary_cache=movie_list_dict)
    # read all the list from cinema device list
    cinema_device_list : list = ccsf.read_list_from_cache(dictionary_cache= cinema_device_dict)

    #catch the code from the data
    #
    # catch movie code from cinema device list
    cinema_device_movie_code_list : list = code_catcher(code_list= cinema_device_list,code_location= 1,number_of_prefix= 0)
    # catch movie code from movie list
    movie_list_code_list : list = code_catcher(code_list= movie_list,code_location= 0,number_of_prefix= 0)
    # catch movie code from movie_seats
    movie_seats_code_list : list = ccsf.seats_code_catcher_from_cache(seats_cache= movie_seats_dict)

    #calculate the mismatched from those movie code
    #
    # calculate mismatched of movie seats and movie list (for delete part)
    seats_list_mismatched : list = mismatched_calculate(main_list= movie_seats_code_list,
                                                        compared_list= movie_list_code_list)
    # calculate mismatched of device list and movie list (for delete part)
    device_list_mismatched: list = mismatched_calculate(main_list=cinema_device_movie_code_list,
                                                        compared_list=movie_list_code_list)
    # calculate mismatched of movie list and device list (for add part)
    list_seats_mismatched : list = mismatched_calculate(main_list= movie_list_code_list,
                                                        compared_list= movie_seats_code_list)
    # calculate mismatched of  movie list and device list (for add part)
    list_device_mismatched : list = mismatched_calculate(main_list= movie_list_code_list,
                                                         compared_list= cinema_device_movie_code_list)
    #SYNC PART (delete first,then add)
    #sync delete part
    _sync_delete(seats_list_mismatched= seats_list_mismatched,device_list_mismatched= device_list_mismatched,
                 movie_seats_dict= movie_seats_dict,cinema_device_dict= cinema_device_dict,md_code_dict=md_code_dict,
                 mt_code_dict= mt_code_dict)
    #sync add part
    _sync_add(movie_list_dict= movie_list_dict,list_seats_mismatched= list_seats_mismatched,
              list_device_mismatched= list_device_mismatched,movie_seats_dict= movie_seats_dict,
              template_seats_dict= template_seats_dict,mt_code_dict= mt_code_dict, md_code_dict= md_code_dict,
              cinema_device_dict= cinema_device_dict)
    ccsf.list_cache_write_to_csv(list_csv=movie_list_csv,list_dictionary_cache= movie_list_dict)
    ccsf.seats_cache_write_to_csv(seats_csv=movie_seats_csv,seats_dictionary_cache= movie_seats_dict,mt_code_dictionary_cache= mt_code_dict)
    ccsf.list_cache_write_to_csv(list_csv=cinema_device_list_csv,list_dictionary_cache= cinema_device_dict)


def _sync_delete (seats_list_mismatched : list,
                  device_list_mismatched : list, movie_seats_dict : dict,
                  cinema_device_dict : dict, md_code_dict : dict, mt_code_dict : dict) -> None:
    if seats_list_mismatched:
        for movie_code in seats_list_mismatched:
            # delete the movie seats that is extra
            ccsf.dictionary_delete(dictionary= movie_seats_dict,key_to_delete= movie_code)
        # uncomment below if the delete function is broke
        # raise ValueError(f"movie seats file:{movie_seats_csv} GOT THE CODE:{seats_list_mismatched} BUT THE movie list "
        #                  f"file: {movie_list_csv} DONT GOT!\nPLEASE DELETE THE CODE IN THE movie "
        #                  f"seats file:{movie_seats_csv} manually!")
    if device_list_mismatched:
        for movie_code in device_list_mismatched:
            ccsf.dictionary_delete(dictionary= cinema_device_dict, key_to_delete= md_code_dict[movie_code])
        # uncomment below if the delete function is broke
        # raise ValueError(f"cinema device list file:{cinema_device_list_csv} GOT THE CODE:{device_list_mismatched} BUT "
        #                  f"THE movie list file: {movie_list_csv} DONT GOT!\nPLEASE DELETE THE CODE IN THE cinema device "
        #                  f"list file: {cinema_device_list_csv} manually!")


def _sync_add (list_seats_mismatched : list,list_device_mismatched : list,
               movie_seats_dict :dict,template_seats_dict :dict,mt_code_dict : dict,
               cinema_device_dict : dict,md_code_dict : dict,movie_list_dict:dict) -> None:
    if list_seats_mismatched:
         for movie_code in list_seats_mismatched:
            # add the movie seats that is lack
            cinema_code = movie_list_dict[movie_code][1].upper()
            movie_seats_init(movie_code= movie_code, cinema_code= cinema_code,
                             movie_seats_dict= movie_seats_dict, mc_code_dict= mt_code_dict,
                             cinema_seats_dict= template_seats_dict)
            dictionary_for_mt : dict = {movie_code : cinema_code}
    if list_device_mismatched:
        #read the cinema device list to make sure the technician code generate is always the newest data
        #check the device list csv got what number of device
        header = cinema_device_dict.get('header')
        default_device_status = keyword_count_for_list(any_dimension_list= header,keyword="status")
        for movie_code in list_device_mismatched:
            temp_list: list = ccsf.read_list_from_cache(dictionary_cache=cinema_device_dict)
            #generate technician code
            tech_code = generate_code_id(code_list= temp_list,prefix_generate="TC",code_location= 0,
                                         number_of_prefix= 2,prefix_got_digit= False,code_id_digit_count= 4)
            #generate the new device list
            device_list_new : list = data_convert_to_list(tech_code,movie_code,*(0 for _ in range(default_device_status)))
            # add the device list that is lack
            ccsf.list_dictionary_update(dictionary= cinema_device_dict,list_to_add= device_list_new)
            dictionary_for_md : dict = {movie_code : tech_code}


def conflict_detect_for_link_seats (current_movie_seats:list,bkid_mvcode_x_y_list:list,booking_data_dict:dict=None,movie_seats_dict:dict=None) -> tuple[bool,str]:
    if booking_data_dict is None: booking_data_dict = ddf.BOOKING_DATA_DICTIONARY
    if movie_seats_dict is None: movie_seats_dict = ddf.MOVIE_SEATS_DICTIONARY
    # detect the actually seat is available or not
    movie_seat_value = movie_seats_specify_value(movie_seats=current_movie_seats, x_axis=bkid_mvcode_x_y_list[2],
                                 y_axis=bkid_mvcode_x_y_list[3])
    if  movie_seat_value == "-1" or movie_seat_value == "1":
        return True,bkid_mvcode_x_y_list[0]
    return False,""





def conflict_check_for_movie_schedule (movie_list_dict : dict=None) -> tuple[bool,list]:
    if movie_list_dict is None: movie_list_dict = ddf.MOVIE_LIST_DICTIONARY
    movie_list_header = read_list_from_cache(dictionary_cache=movie_list_dict, code="header", header_insert=False)
    movie_list = read_list_from_cache(dictionary_cache=movie_list_dict)
    header_dict = fu.header_location_get(header_list=movie_list_header)
    conflict_detect_status_preliminary,conflict_dict = _conflict_detect_preliminary(header_dict=header_dict,movie_list=movie_list)
    if not conflict_detect_status_preliminary: return True,[]
    conflict_final_detect_status,final_conflict_list = _conflict_detect_meticulous(header_dict= header_dict,
                                                                                    conflict_dict= conflict_dict)
    if not conflict_final_detect_status : return True,[]
    return False,final_conflict_list



def _conflict_detect_preliminary(header_dict : dict,movie_list : list) -> tuple[bool,dict]:
    movie_code_location : int = header_dict["movie_code"]
    cinema_location : int = header_dict["CINEMA_number"]
    date_location : int = header_dict["date"]
    group_dict : dict = {}
    conflict_dict : dict = {}

    for row in movie_list:
        movie_code = row[movie_code_location]
        cinema = row[cinema_location]
        date = row[date_location]
        if not group_dict.get(cinema + date): group_dict.update({cinema + date: []})
        group_dict[cinema + date].append(movie_code)

    for keys, values in group_dict.items():
        if len(values) > 1: conflict_dict.update({keys: group_dict[keys]})

    if not conflict_dict: return False, {}
    return True, conflict_dict

def _conflict_detect_meticulous (header_dict : dict,conflict_dict : dict,movie_list_dict : dict=None) -> tuple[bool,list]:
    if not movie_list_dict: movie_list_dict = ddf.MOVIE_LIST_DICTIONARY
    start_time_location : int = header_dict["movie_time_start"] - 1
    end_time_location : int = header_dict["movie_time_end"] - 1
    conflict_time_list_three_dimension : list = []
    true_conflict_movie_code : list = []
    for code_row in conflict_dict.values():
        conflict_list_two_dimension : list = []
        for code in code_row:
            conflict_list_one_dimension : list = []
            conflict_list_one_dimension.append(code)
            conflict_list_one_dimension.append(fu.time_to_minute(movie_list_dict.get(code)[start_time_location]))
            conflict_list_one_dimension.append(fu.time_to_minute(movie_list_dict.get(code)[end_time_location]))
            conflict_list_two_dimension.append(conflict_list_one_dimension)
        conflict_time_list_three_dimension.append(sorted(conflict_list_two_dimension, key= lambda movie:movie[1]))
    for conflict_data in conflict_time_list_three_dimension:
        conflict_code_set : set = set()
        true_conflict_one_dimension: list = []
        for i in range(len(conflict_data) - 1):
            if conflict_check_light(minuteAEND=conflict_data[i][2],minuteBSTART=conflict_data[i+1][1]):
                continue
            conflict_code_set.add(conflict_data[i][0])
            conflict_code_set.add(conflict_data[i+1][0])
        for i in range(len(conflict_data)):
            if not conflict_code_set: break
            if conflict_data[i][0] in conflict_code_set:
                true_conflict_one_dimension.append(f"**{conflict_data[i][0]}**")
                continue
            true_conflict_one_dimension.append(conflict_data[i][0])
        if conflict_code_set : true_conflict_movie_code.append(true_conflict_one_dimension)

    if not true_conflict_movie_code: return False,[]
    return True,true_conflict_movie_code

def conflict_check_light (minuteAEND : int, minuteBSTART: int) -> bool:
    if minuteAEND <= minuteBSTART: return True
    return False





def conflict_data_auto_sort(schedule_conflict_list : list,movie_list_dict:dict = None) -> None:
    if movie_list_dict is None: movie_list_dict = ddf.MOVIE_LIST_DICTIONARY
    header_location_dict : dict = header_location_get(ccsf.read_list_from_cache(dictionary_cache=movie_list_dict,
                                                                                code="header",header_insert=False))
    start_time_location : int = header_location_dict["movie_time_start"] - 1
    end_time_location : int = header_location_dict["movie_time_end"] - 1
    conflict_time_dict : dict = {}
    conflict_list_auto_failed : list =[]
    schedule_conflict_list_strip = fu.keyword_erase_for_list(any_dimension_list=schedule_conflict_list,keyword="**")
    for conflict_row in schedule_conflict_list_strip:
        for code in conflict_row:
            conflict_time_dict.update({code:[fu.time_to_minute(movie_list_dict.get(code)[start_time_location])]})
            conflict_time_dict[code].append(fu.time_to_minute(movie_list_dict.get(code)[end_time_location]))

    for conflict_row in schedule_conflict_list_strip:
        time_interval : int = 0
        for i in range(len(conflict_row) - 1):
            #
            #整体原理讲解，先检测相邻的电影是否冲突（列表需已排列）
            #如有冲突，把后面的电影推到第一个电影后面
            #如此往复...
            #
            if not conflict_check_light(minuteAEND=conflict_time_dict[conflict_row[i]][1],minuteBSTART=conflict_time_dict[conflict_row[i+1]][0]):
                time_interval = conflict_time_dict[conflict_row[i+1]][1] - conflict_time_dict[conflict_row[i+1]][0]
                conflict_time_dict[conflict_row[i+1]][0] = conflict_time_dict[conflict_row[i]][1]
                conflict_time_dict[conflict_row[i+1]][1] = conflict_time_dict[conflict_row[i]][1] + time_interval

        if conflict_time_dict[conflict_row[-1]][1] > 1440: time_interval = conflict_time_dict[conflict_row[-1]][1] - 1440
        conflict_time_dict[conflict_row[0]][0] -= time_interval
        conflict_time_dict[conflict_row[0]][1] -= time_interval
        if conflict_time_dict[conflict_row[0]][0] < 0 :
            conflict_list_auto_failed.append(conflict_row)
            continue
        for i in range(1, len(conflict_row)):
            conflict_time_dict[conflict_row[i]][0] -= time_interval
            conflict_time_dict[conflict_row[i]][1] -= time_interval














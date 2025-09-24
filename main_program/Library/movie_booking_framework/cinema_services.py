from .id_generator import *
from .movie_seats_framework import *
from .movie_list_framework import *
from main_program.Library.data_communication_framework import cache_csv_sync_framework as ccsf
from main_program.Library.cache_framework import data_dictionary_framework as ddf
from .valid_checker import movie_seats_csv_valid_check

def link_seats (movie_seats_csv : str, booking_data_csv : str,
                book_movie_code_location : int = 2, book_x_seats_location : int = 5, book_y_seats_location : int = 6,
                movie_seats_dict=None, booking_data_dict=None, template_seats_dict=None, mt_code_dict=None) -> None:
    if booking_data_dict is None: booking_data_dict = ddf.BOOKING_DATA_DICTIONARY
    if template_seats_dict is None: template_seats_dict = ddf.TEMPLATE_SEATS_DICTIONARY
    if movie_seats_dict is None: movie_seats_dict = ddf.MOVIE_SEATS_DICTIONARY
    if mt_code_dict is None : mt_code_dict = ddf.MOVIE_TEMPLATE_CODE_DICTIONARY
    booking_data_list : list = ccsf.read_list_from_cache(dictionary_cache= booking_data_dict)
    #First init the seats file (all the data of seats clear)
    movie_seats_cache_whole_init(movie_seats_dict= movie_seats_dict,template_seats_dict= template_seats_dict,mt_code_dict= mt_code_dict)
    for row in booking_data_list:
        #get the data of booking (movie code,x,y) from booking data list)
        #[movie_code,x_axis,y_axis]
        mvcode_x_y_list : list = get_movie_code_x_y_value_list(booking_data_array= row,
                                                               movie_code_location= book_movie_code_location,
                                                               x_seats_location= book_x_seats_location,
                                                               y_seats_location= book_y_seats_location)
        #read the current movie seats (from the mvcode_x_y_list)
        current_movie_seats : list = ccsf.read_seats_from_cache(cache_dictionary= movie_seats_dict,code= mvcode_x_y_list[0])
        # detect the actually seat is available or not
        if movie_seats_specify_value(movie_seats=current_movie_seats,x_axis=mvcode_x_y_list[1],y_axis=mvcode_x_y_list[2]) ==  "-1":
            #this usually happen in manager change the template code of movie seats
            raise ValueError(f"This movie seat is unvailable(-1)!You should check your booking data file!\n"
                             f"movie_seats: {current_movie_seats}\nx_axis: {mvcode_x_y_list[1]}\ny_axis: {mvcode_x_y_list[2]}")
        # if no problem,modify the actual seat
        modify_movie_seats_list(movie_seat_list=current_movie_seats,x_axis=mvcode_x_y_list[1],y_axis=mvcode_x_y_list[2],target_number= 1)
        # update it to the movie seats csv
        ccsf.seat_dictionary_update(seats_dictionary= movie_seats_dict,mt_code_dictionary=mt_code_dict,
                                        code_to_update=mvcode_x_y_list[0],seats_data_to_add=current_movie_seats)
    ccsf.list_cache_write_to_csv(list_csv= booking_data_csv,list_dictionary_cache= booking_data_dict)
    ccsf.seats_cache_write_to_csv(seats_csv= movie_seats_csv,seats_dictionary_cache= movie_seats_dict,
                                      mt_code_dictionary_cache= mt_code_dict)

def movie_seats_cache_whole_init (movie_seats_dict : dict, template_seats_dict : dict, mt_code_dict : dict) -> None:
    for movie_code,template_code in mt_code_dict.items():
        #init the movie seats(one only,but using for loop so can init all the file)
        movie_seats_init(movie_code= movie_code,template_code= template_code,movie_seats_dict= movie_seats_dict,
                         template_seats_dict= template_seats_dict,mt_code_dict= mt_code_dict)


def movie_seats_init(movie_code : str, template_code : str,
                     movie_seats_dict : dict, template_seats_dict : dict, mt_code_dict : dict) -> None:
    # read the template data
    template_seats : list = ccsf.read_seats_from_cache(cache_dictionary= template_seats_dict,code= template_code)
    #overwrite the old data with template data
    ccsf.seat_dictionary_update(seats_dictionary= movie_seats_dict,mt_code_dictionary=mt_code_dict,code_to_update= movie_code,
                                    seats_data_to_add= template_seats)




#IMPORTANT:please check the movie_code_location,x_seats_location,and y_seats_location is the correct location or not!
#I have no error detection for this EXCEPTION!!!!!!
def get_movie_code_x_y_value_list (booking_data_array : list,movie_code_location : int, x_seats_location : int, y_seats_location : int) -> list:
    #check the booking_data_array is one dimension list or not (no 2d list allow)
    if any(isinstance(element, (list,tuple)) for element in booking_data_array):
        #if the booking_data_array is 2d list,interrupt the action and raise error
        raise TypeError (f"booking_data_array: {booking_data_array} must be a array (no 2d list allowed)")
    mvcode_x_y_list : list = []
    #add the movie code
    mvcode_x_y_list.append(booking_data_array[movie_code_location])
    #add the x axis
    mvcode_x_y_list.append(int(booking_data_array[x_seats_location]))
    #add the y axis
    mvcode_x_y_list.append(int(booking_data_array[y_seats_location]))
    #return the list
    return mvcode_x_y_list


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


#yup,just convert the data to list
#for example
#the_list = data_convert_to_list ("x","ok","zzzz")
#the_list = ["x","ok","zzzz"]
def data_convert_to_list (*args):
    target_list : list = []
    #unpack the args and use for loop to append the inside item of args
    for item in args:
        target_list.append(item)
    #return the list
    return target_list


#yup this function just only for device column count
#if i have time,i will turn this function to universal function
def device_count_for_device_list (cinema_device_list : list) -> int:
    device_count : int = 0
    for row in cinema_device_list:
        for item in row:
            #if "status" keyword is in item,it shows that the item is device column
            if "status" in item:
                device_count += 1
            else:
                continue
    return device_count


#sync the movie list,movie seats, and cinema device list
#The SSOT is movie list
def sync_all (movie_list_csv : str, movie_seats_csv : str,cinema_device_list_csv : str,default_template_code : str,
              movie_list_dict : dict=None,movie_seats_dict : dict=None,cinema_device_dict : dict =None,
              template_seats_dict : dict=None, mt_code_dict : dict=None,md_code_dict : dict=None) -> None:
    if movie_seats_dict is None: movie_seats_dict = ddf.MOVIE_SEATS_DICTIONARY
    if movie_list_dict is None: movie_list_dict = ddf.MOVIE_LIST_DICTIONARY
    if cinema_device_dict is None: cinema_device_dict = ddf.CINEMA_DEVICE_DICTIONARY
    if template_seats_dict is None: template_seats_dict = ddf.TEMPLATE_SEATS_DICTIONARY
    if mt_code_dict is None: mt_code_dict = ddf.MOVIE_TEMPLATE_CODE_DICTIONARY
    if md_code_dict is None: md_code_dict = ddf.MOVIE_DEVICE_CODE_DICTIONARY
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
    _sync_add(default_template_code=default_template_code,list_seats_mismatched= list_seats_mismatched,
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
            ccsf.dictionary_delete(dictionary= mt_code_dict,key_to_delete= movie_code)
        # uncomment below if the delete function is broke
        # raise ValueError(f"movie seats file:{movie_seats_csv} GOT THE CODE:{seats_list_mismatched} BUT THE movie list "
        #                  f"file: {movie_list_csv} DONT GOT!\nPLEASE DELETE THE CODE IN THE movie "
        #                  f"seats file:{movie_seats_csv} manually!")
    if device_list_mismatched:
        for movie_code in device_list_mismatched:
            ccsf.dictionary_delete(dictionary= cinema_device_dict, key_to_delete= md_code_dict[movie_code])
            ccsf.dictionary_delete(dictionary= md_code_dict,key_to_delete= movie_code)
        # uncomment below if the delete function is broke
        # raise ValueError(f"cinema device list file:{cinema_device_list_csv} GOT THE CODE:{device_list_mismatched} BUT "
        #                  f"THE movie list file: {movie_list_csv} DONT GOT!\nPLEASE DELETE THE CODE IN THE cinema device "
        #                  f"list file: {cinema_device_list_csv} manually!")


def _sync_add (default_template_code : str,list_seats_mismatched : list,list_device_mismatched : list,
               movie_seats_dict :dict,template_seats_dict :dict,mt_code_dict : dict,
               cinema_device_dict : dict,md_code_dict : dict) -> None:
    if list_seats_mismatched:
         for movie_code in list_seats_mismatched:
            # add the movie seats that is lack
            movie_seats_init(movie_code= movie_code,template_code= default_template_code,
                             movie_seats_dict= movie_seats_dict,mt_code_dict= mt_code_dict,template_seats_dict= template_seats_dict)
            dictionary_for_mt : dict = {movie_code : default_template_code}
            ccsf.dictionary_update_with_dict(dictionary= mt_code_dict,dictionary_to_add= dictionary_for_mt)
    if list_device_mismatched:
        #read the cinema device list to make sure the technician code generate is always the newest data
        temp_list : list = ccsf.read_list_from_cache(dictionary_cache= cinema_device_dict)
        #check the device list csv got what number of device
        default_device_status = device_count_for_device_list(cinema_device_list=temp_list)
        for movie_code in list_device_mismatched:
            #generate technician code
            tech_code = generate_code_id(code_list= temp_list,prefix_generate="TC",code_location= 0,
                                         number_of_prefix= 2,prefix_got_digit= False,code_id_digit_count= 0)
            #generate the new device list
            device_list_new : list = data_convert_to_list(tech_code,movie_code,*(0 for _ in range(default_device_status)))
            # add the device list that is lack
            ccsf.list_dictionary_update(dictionary= cinema_device_dict,key_location= 0,list_to_add= device_list_new)
            dictionary_for_md : dict = {movie_code : tech_code}
            ccsf.dictionary_update_with_dict(dictionary= md_code_dict,dictionary_to_add= dictionary_for_md)
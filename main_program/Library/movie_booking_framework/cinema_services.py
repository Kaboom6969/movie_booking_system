from .id_generator import *
from .movie_seats_framework import *
from .movie_list_framework import *
from .valid_checker import movie_seats_csv_valid_check

def link_seats (movie_seats_csv : str, booking_data_csv : str,template_seats_csv : str,book_movie_code_location : int = 2, book_x_seats_location : int = 5, book_y_seats_location : int = 6) -> None:
    booking_data_list : list = []
    #First init the seats file (all the data of seats clear)
    movie_seats_csv_whole_init(movie_seats_csv= movie_seats_csv,template_seats_csv= template_seats_csv)
    #read the booking data
    read_movie_list_csv(movie_list_csv= booking_data_csv,movie_list=booking_data_list)
    for row in booking_data_list:
        #get the data of booking (movie code,x,y) from booking data list)
        #[movie_code,x_axis,y_axis]
        mvcode_x_y_list : list = get_movie_code_x_y_value_list(booking_data_array= row,
                                                               movie_code_location= book_movie_code_location,
                                                               x_seats_location= book_x_seats_location,
                                                               y_seats_location= book_y_seats_location)
        current_movie_seats : list = []
        #read the current movie seats (from the mvcode_x_y_list)
        read_movie_seats_csv(movie_seats_csv= movie_seats_csv,movie_seats= current_movie_seats,movie_code= mvcode_x_y_list[0])
        # detect the actually seat is available or not
        if movie_seats_specify_value(movie_seats=current_movie_seats,x_axis=mvcode_x_y_list[1],y_axis=mvcode_x_y_list[2]) ==  "-1":
            #this usually happen in manager change the template code of movie seats
            raise ValueError(f"This movie seat is unvailable(-1)!You should check your booking data file!\n"
                             f"movie_seats: {current_movie_seats}\nx_axis: {mvcode_x_y_list[1]}\ny_axis: {mvcode_x_y_list[2]}")
        # if no problem,modify the actual seat
        modify_movie_seats_list(movie_seat_list=current_movie_seats,x_axis=mvcode_x_y_list[1],y_axis=mvcode_x_y_list[2],target_number= 1)
        # update it to the movie seats csv
        update_movie_seats_csv(movie_seats_csv= movie_seats_csv,movie_seats=current_movie_seats,movie_code= mvcode_x_y_list[0])

def movie_seats_csv_whole_init (movie_seats_csv : str,template_seats_csv : str) -> None:
    try:
        movie_seats_csv_valid_check(movie_seats_csv)
    except Exception as e:
        raise Exception(f"INIT FAILED! ERROR:{e}")
    movie_seats_csv_path = get_path(movie_seats_csv)
    movie_code_array : list = []
    template_code_array : list = []
    with open(movie_seats_csv_path,'r',newline ='') as ms_csv_r:
        next(ms_csv_r)
        for line in ms_csv_r:
            if not line.strip(): continue
            row = parse_csv_line(line)
            if row[0] == "CODE":
                movie_code_array.append(row[1])
                template_code_array.append(row[2])
    if len(movie_code_array) != len(template_code_array):
        raise ValueError("The number of movie code and template code should be same! Please check the file!")
    for movie_code,template_code in zip(movie_code_array,template_code_array):
        movie_seats_init(movie_seats_csv= movie_seats_csv,template_seats_csv= template_seats_csv,movie_code= movie_code,template_code= template_code)

def add_movie_seats_from_template (movie_seats_csv : str, template_seats_csv : str, movie_code : str, template_code : str) -> None:
    new_movie_seats : list = []
    read_movie_seats_csv(movie_seats_csv= template_seats_csv,movie_seats= new_movie_seats,movie_code= template_code,skip_valid_check= True)
    add_movie_seats_csv(movie_seats_csv= movie_seats_csv,movie_seats= new_movie_seats,movie_code= movie_code, template_code= template_code)


def movie_seats_init(movie_seats_csv : str, template_seats_csv : str, movie_code : str,template_code : str) -> None:
    template_seats : list = []
    read_movie_seats_csv(movie_seats_csv= template_seats_csv,movie_seats= template_seats,movie_code= template_code,skip_valid_check= True)
    update_movie_seats_csv(movie_seats_csv= movie_seats_csv,movie_seats= template_seats,movie_code= movie_code)

def get_movie_code_x_y_value_list (booking_data_array : list,movie_code_location : int, x_seats_location : int, y_seats_location : int) -> list:
    if any(isinstance(element, (list,tuple)) for element in booking_data_array):
        raise TypeError (f"booking_data_array: {booking_data_array} must be a array (no 2d list allowed)")
    mvcode_x_y_list : list = []
    mvcode_x_y_list.append(booking_data_array[movie_code_location])
    mvcode_x_y_list.append(int(booking_data_array[x_seats_location]))
    mvcode_x_y_list.append(int(booking_data_array[y_seats_location]))
    return mvcode_x_y_list

def mismatched_calculate (main_list : list, compared_list : list) -> list:
    calculated_list : list = []
    for item in main_list:
        if item not in compared_list:
            calculated_list.append(item)
    return calculated_list

def data_convert_to_list (*args):
    target_list : list = []
    for item in args:
        target_list.append(item)
    return target_list

def device_count_for_device_list (cinema_device_list : list) -> int:
    device_count : int = 0
    for row in cinema_device_list:
        for item in row:
            if "status" in item:
                device_count += 1
            else:
                continue
    return device_count



def sync_all (movie_list_csv : str, movie_seats_csv : str,cinema_device_list_csv : str,templates_seats_csv : str,default_template_code : str) -> None:
    movie_list : list = []
    cinema_device_list : list = []

    #read the data from csv file
    #
    # read the daw data of movie seats first
    movie_seats_raw_data : list = read_movie_seats_csv_raw_data(movie_seats_csv= movie_seats_csv)
    # read all the list from movie list
    read_movie_list_csv(movie_list_csv= movie_list_csv,movie_list= movie_list)
    # read all the list from cinema device list
    read_movie_list_csv(movie_list_csv= cinema_device_list_csv,movie_list= cinema_device_list,read_header= True)

    #catch the code from the data
    #
    # catch movie code from cinema device list
    cinema_device_movie_code_list : list = code_catcher(code_list= cinema_device_list,code_location= 1,number_of_prefix= 0)
    # catch movie code from movie list
    movie_list_code_list : list = code_catcher(code_list= movie_list,code_location= 0,number_of_prefix= 0)
    # catch movie code from movie_seats
    movie_seats_code_list : list = seats_code_catcher(movie_seats_raw_data= movie_seats_raw_data)

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
    _sync_delete(movie_seats_csv= movie_seats_csv,cinema_device_list_csv= cinema_device_list_csv,
                 seats_list_mismatched= seats_list_mismatched,device_list_mismatched= device_list_mismatched)
    #sync add part
    _sync_add(movie_seats_csv= movie_seats_csv,cinema_device_list_csv= cinema_device_list_csv,
              templates_seats_csv= templates_seats_csv,default_template_code=default_template_code,
              list_seats_mismatched= list_seats_mismatched,list_device_mismatched= list_device_mismatched)


def _sync_delete (movie_seats_csv : str, cinema_device_list_csv : str,seats_list_mismatched : list,
                  device_list_mismatched : list) -> None:
    if seats_list_mismatched:
        for movie_code in seats_list_mismatched:
            # delete the movie seats that is extra
            delete_movie_seats_csv(movie_seats_csv= movie_seats_csv,movie_code= movie_code)
        # uncomment below if the delete function is broke
        # raise ValueError(f"movie seats file:{movie_seats_csv} GOT THE CODE:{seats_list_mismatched} BUT THE movie list "
        #                  f"file: {movie_list_csv} DONT GOT!\nPLEASE DELETE THE CODE IN THE movie "
        #                  f"seats file:{movie_seats_csv} manually!")
    if device_list_mismatched:
        for movie_code in device_list_mismatched:
            delete_movie_list_csv(movie_list_csv=cinema_device_list_csv, movie_code=movie_code, code_location=1) #delete the device list that is extra
        # uncomment below if the delete function is broke
        # raise ValueError(f"cinema device list file:{cinema_device_list_csv} GOT THE CODE:{device_list_mismatched} BUT "
        #                  f"THE movie list file: {movie_list_csv} DONT GOT!\nPLEASE DELETE THE CODE IN THE cinema device "
        #                  f"list file: {cinema_device_list_csv} manually!")


def _sync_add (movie_seats_csv : str,cinema_device_list_csv : str,templates_seats_csv : str,
               default_template_code : str,list_seats_mismatched : list,list_device_mismatched : list) -> None:
    if list_seats_mismatched:
         for movie_code in list_seats_mismatched:
            # add the movie seats that is lack
            add_movie_seats_from_template(movie_seats_csv= movie_seats_csv,template_seats_csv= templates_seats_csv,
                                          movie_code= movie_code,template_code= default_template_code)
    if list_device_mismatched:
        temp_list : list = []
        #read the cinema device list to make sure the technician code generate is always the newest data
        read_movie_list_csv(movie_list_csv=cinema_device_list_csv, movie_list=temp_list, read_header=True)
        #check the device list csv got what number of device
        default_device_status = device_count_for_device_list(cinema_device_list=temp_list)
        for movie_code in list_device_mismatched:
            #generate technician code
            tech_code = generate_code_id(code_list= temp_list,prefix_generate="TC",code_location= 0,
                                         number_of_prefix= 2,prefix_got_digit= False,code_id_digit_count= 0)
            #generate the new device list
            device_list_new : list = data_convert_to_list(tech_code,movie_code,*(0 for i in range(default_device_status)))
            # add the device list that is lack
            add_movie_list_csv(movie_list_csv= cinema_device_list_csv,movie_list= device_list_new,movie_code= tech_code)
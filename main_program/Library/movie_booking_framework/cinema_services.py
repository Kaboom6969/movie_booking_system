from .movie_seats_framework import *
from .movie_list_framework import *
from .valid_checker import movie_seats_csv_valid_check

def link_seats (movie_seats_csv : str, booking_data_csv : str,template_seats_csv : str,book_movie_code_location : int = 2, book_x_seats_location : int = 5, book_y_seats_location : int = 6) -> None:
    booking_data_list : list = []
    movie_seats_csv_whole_init(movie_seats_csv= movie_seats_csv,template_seats_csv= template_seats_csv)
    read_movie_list_csv(movie_list_csv= booking_data_csv,movie_list=booking_data_list)
    for row in booking_data_list:
        #[movie_code,x_axis,y_axis]
        mvcode_x_y_list : list = get_movie_code_x_y_value_list(booking_data_array= row,
                                                               movie_code_location= book_movie_code_location,
                                                               x_seats_location= book_x_seats_location,
                                                               y_seats_location= book_y_seats_location)
        movie_seats : list = []
        read_movie_seats_csv(movie_seats_csv= movie_seats_csv,movie_seats= movie_seats,movie_code= mvcode_x_y_list[0])
        if movie_seats_specify_value(movie_seats=movie_seats,x_axis=mvcode_x_y_list[1],y_axis=mvcode_x_y_list[2]) ==  "-1":
            raise ValueError(f"This movie seat is unvailable(-1)!You should check your booking data file!\n"
                             f"movie_seats: {movie_seats}\nx_axis: {mvcode_x_y_list[1]}\ny_axis: {mvcode_x_y_list[2]}")
        modify_movie_seats_list(movie_seat_list=movie_seats,x_axis=mvcode_x_y_list[1],y_axis=mvcode_x_y_list[2],target_number= 1)
        update_movie_seats_csv(movie_seats_csv= movie_seats_csv,movie_seats=movie_seats,movie_code= mvcode_x_y_list[0])

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
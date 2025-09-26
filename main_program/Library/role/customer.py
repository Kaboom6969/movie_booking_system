from main_program.Library.movie_booking_framework.seat_visualizer import *
from main_program.Library.movie_booking_framework.cinema_services import *
from main_program.Library.cache_framework.data_dictionary_framework import *
from main_program.Library.data_communication_framework import cache_csv_sync_framework as ccsf
import datetime

DEFAULT_WIDTH = 30

def check_ticket_bought(customer_code : str,return_booking_code : bool,booking_data_dict : dict = None) -> list:
    if booking_data_dict is None: booking_data_dict = ddf.BOOKING_DATA_DICTIONARY
    # format: ['B001','C001', '001','2025/8/13','2','3','3','Online']
    booking_list : list = ccsf.read_list_from_cache(dictionary_cache= booking_data_dict)
    booking_list_filtered : list = [row for row in booking_list if row[1]==customer_code]
    booking_code_list : list = []         #format:'B001'
    print(f"{'booking_id' : <{DEFAULT_WIDTH}}{'User_id': <{DEFAULT_WIDTH}}{'Movie Code': <{DEFAULT_WIDTH}}{'Booking Date': <{DEFAULT_WIDTH}}")
    print("-" * (DEFAULT_WIDTH * 4 + 1))
    for row in booking_list_filtered:
        if return_booking_code:
            booking_code_list.append(row[0])
        else:
            booking_code_list.append(row[2])
        print(f"{row[0]: <{DEFAULT_WIDTH}}{row[1]: <{DEFAULT_WIDTH}}{str(row[2]): <{DEFAULT_WIDTH}}{str(row[3]): <{DEFAULT_WIDTH}}")
    return booking_code_list

def booking_to_movie_list_print(movie_code_list : list, movie_code : str, movie_list_dict : dict = None) -> None:
    if movie_list_dict is None: movie_list_dict = ddf.MOVIE_LIST_DICTIONARY
    if movie_code not in movie_code_list:
        raise ValueError("Please enter the valid movie code!")
    else:
        #format: [['002', 'Joker', 'cinema002', '19:00', '22:00']]
        booking_movie_list : list = ccsf.read_list_from_cache(dictionary_cache= movie_list_dict,code= movie_code)
        movie_list_print_with_format(data_list= booking_movie_list)

def movie_list_print_with_format(data_list : list,
                                 DEFAULT_WIDTH : int = DEFAULT_WIDTH,movie_seats_dict : dict = None) -> None:
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

def code_range_create(code_list : list,code_location : int) -> list:
    code_range_list : list =[]
    for row in code_list:
        code_range_list.append(row[code_location])
    return code_range_list

def book_movie_operation(movie_code : str,movie_seats_csv : str,booking_data_csv,user_id : str,
                         booking_data_dict : dict=None) -> None:
    if booking_data_dict is None:booking_data_dict = ddf.BOOKING_DATA_DICTIONARY
    try:
        link_seats(movie_seats_csv= movie_seats_csv, booking_data_csv= booking_data_csv)
        booking_movie_seats = movie_list_to_movie_seats_print(movie_code=movie_code)
        x_range = x_range_calculate(movie_seats=booking_movie_seats)
        y_range = y_range_calculate(movie_seats=booking_movie_seats)
        first_attempt = True
        try_again = False
        while first_attempt or try_again:
            first_attempt = False
            x_pointer = book_movie_input(range_list= x_range,name_in_input= "Column")
            movie_list_to_movie_seats_print(movie_code=movie_code,x_pointer=x_pointer)
            y_pointer = book_movie_input(range_list= y_range,name_in_input= "Row")
            movie_list_to_movie_seats_print(movie_code=movie_code,x_pointer=x_pointer,y_pointer=y_pointer)
            seats_value =movie_seats_specify_value(movie_seats=booking_movie_seats, x_axis=x_pointer, y_axis=y_pointer)
            booking_status =book_movie_buy(seats_value= seats_value)
            if booking_status:
                booking_list : list = ccsf.read_list_from_cache(dictionary_cache=booking_data_dict)
                book_id : str = generate_code_id(code_list= booking_list,prefix_generate= "B",code_location= 0,number_of_prefix= 1,prefix_got_digit= False,code_id_digit_count= 4)
                booking_data_list = _booking_data_create(book_id= book_id,user_id= user_id,movie_code= movie_code
                                                         ,booking_date= datetime.datetime.now().strftime('%Y/%m/%d')
                                                         ,booking_or_pay= "1",x_seat= str(x_pointer)
                                                         ,y_seat= str(y_pointer),source= "online")
                ccsf.list_dictionary_update(dictionary= booking_data_dict,key_location= 0,list_to_add= booking_data_list)
                link_seats(movie_seats_csv=movie_seats_csv, booking_data_csv= booking_data_csv)

            if not booking_status: try_again = True
            else: try_again = False

    except Exception as e:
        raise Exception(f"UNKNOWN ERROR,ERROR:{e}")

def book_movie_input(range_list : list,name_in_input : str) -> int:
    while True:
        try:
            pointer : int = int(input(f"Please enter the {name_in_input} number ({range_list[0]} to {range_list[1]}): "))
            if pointer > range_list[1] or pointer < range_list[0]:
                raise IndexError(f"{name_in_input} Should be in {range_list[0]} to {range_list[1]}!")
            return pointer
        except ValueError:
            print(f"{name_in_input} must be a number!")
            pointer = 0
        except IndexError as e:
            print(e)
            pointer = 0

#need to refractor
def book_movie_buy(seats_value : str)-> bool:
    if seats_value == "0":
        user_input = str(input("This seat is available. Are you (S)ure to book? or (C)ancel? "))
        if user_input.lower() == 's':
            print("Booking successful!")
            return True
        elif user_input.lower() == 'c':
            print("Booking cancelled.")
            return False
        else: raise ValueError("Please Enter S(s) or C(c)")
    elif seats_value == "1":
        print("This seat is already booked. Please choose another one.")
        return False
    else:
        print("This is an invalid seat (e.g., an aisle). Please choose another one.")
        return False



def _booking_data_create (book_id : str,user_id : str,movie_code : str,booking_date : str
                         ,booking_or_pay : str,x_seat : str, y_seat : str,source : str) -> list:
    booking_data_list : list = []
    booking_data_list.append(book_id)
    booking_data_list.append(user_id)
    booking_data_list.append(movie_code)
    booking_data_list.append(booking_date)
    booking_data_list.append(booking_or_pay)
    booking_data_list.append(x_seat)
    booking_data_list.append(y_seat)
    booking_data_list.append(source)
    return [booking_data_list]




def movie_list_to_movie_seats_print(movie_code : str,movie_seats_dict : dict=None,x_pointer = -1,y_pointer = -1) -> list:
    if movie_seats_dict is None: movie_seats_dict = ddf.MOVIE_SEATS_DICTIONARY
    movie_seats_list : list = ccsf.read_seats_from_cache(cache_dictionary=movie_seats_dict,code=movie_code)
    print()
    print("-" * int(DEFAULT_WIDTH * 1.8))
    print_movie_seat_as_emojis(movie_seats_list,x_pointer,y_pointer)
    print("-" * int(DEFAULT_WIDTH * 1.8))
    print(f"Movie Code:{movie_code}")
    return movie_seats_list

def check_all_movie_list(movie_list_dict : dict=None,movie_seats_dict : dict=None) -> list:
    if movie_list_dict is None: movie_list_dict = ddf.MOVIE_LIST_DICTIONARY
    if movie_seats_dict is None: movie_seats_dict = ddf.MOVIE_SEATS_DICTIONARY
    movie_list_all : list = ccsf.read_list_from_cache(dictionary_cache=movie_list_dict)
    movie_list_print_with_format(data_list= movie_list_all,movie_seats_dict=movie_seats_dict)
    return code_range_create(code_list= movie_list_all,code_location= 0)


def cancel_booking_operation(user_id : str, booking_data_csv : str, movie_seats_csv : str, movie_list_csv : str, template_seats_csv : str,
                             booking_data_dict : dict = None) -> None:
    if booking_data_dict is None: booking_data_dict = ddf.BOOKING_DATA_DICTIONARY
    booking_code_range : list = check_ticket_bought(customer_code= user_id,booking_data_dict= booking_data_dict,return_booking_code= True)
    while True:
        booking_code_cancel : str = str(input("Please Enter the code that you want to cancel: "))
        if booking_code_cancel not in booking_code_range:
            print("Please enter a valid code!")
            continue
        while True:
            user_command : str = str(input("Are you sure you want to cancel the booking? (y/n)"))
            if user_command.lower() != 'y' and user_command.lower() != 'n':
                print("Please enter a valid command!(y/n)")
            else:
                break
        if user_command.lower() == "n":
            return
        if user_command.lower() == "y":
            ccsf.dictionary_delete(dictionary=booking_data_dict,key_to_delete=booking_code_cancel)
            link_seats(movie_seats_csv= movie_seats_csv,booking_data_csv= booking_data_csv)
            return






#JUST TEST
if __name__ == '__main__':
    init_all_dictionary()
    user_input = str(input("empty"))
    check_all_movie_list()
    # valid_movie_code = check_ticket_bought(customer_code= "C001",return_booking_code= False)
    # user_input = str(input("Please enter the code: "))
    # booking_to_movie_list_print(movie_code_list= valid_movie_code,movie_code= user_input)
    #book_movie_operation(movie_code= "003",movie_seats_csv= "movie_seat.csv",booking_data_csv= "booking_data.csv",
    #                     template_seats_csv= "template_seats.csv",user_id= "C001")
    # cancel_booking_operation(user_id= "C001",booking_data_csv= "booking_data.csv",movie_list_csv= "movie_list.csv"
    #                          ,movie_seats_csv= "movie_seat.csv",template_seats_csv= "template_seats.csv")



from main_program.Library.movie_booking_framework import seat_visualizer as sv
from main_program.Library.movie_booking_framework import cinema_services as cnsv
from main_program.Library.cache_framework import data_dictionary_framework as ddf
from main_program.Library.movie_booking_framework import movie_seats_framework as msf
from main_program.Library.movie_booking_framework import id_generator as idg
from main_program.Library.data_communication_framework import cache_csv_sync_framework as ccsf
from main_program.Library.movie_booking_framework import framework_utils as fu
from main_program.Library.payment_framework import payment_framework as pf
import datetime



def check_ticket_bought(customer_code : str,return_booking_code : bool,booking_data_dict : dict) -> list:
    # format: ['B001','C001', '001','2025/8/13','2','3','3','Online']
    booking_header : dict = fu.header_location_get(booking_data_dict["header"])
    booking_list : list = ccsf.read_list_from_cache(dictionary_cache= booking_data_dict)
    booking_list_filtered : list = [row for row in booking_list if row[1]==customer_code]
    booking_code_list : list = []         #format:'B001'
    print(
        f"{'booking_id' : <{fu.DEFAULT_WIDTH}}"
        f"{'User_id': <{fu.DEFAULT_WIDTH}}"
        f"{'Movie Code': <{fu.DEFAULT_WIDTH}}"
        f"{'Booking Date': <{fu.DEFAULT_WIDTH}}"
    )
    print("-" * (fu.DEFAULT_WIDTH * 4 + 1))
    for row in booking_list_filtered:
        if return_booking_code:
            booking_code_list.append(row[booking_header['Book ID']])
        else:
            booking_code_list.append(row[booking_header['Movie Code']])
        print(
            f"{row[0]: <{fu.DEFAULT_WIDTH}}"
            f"{row[1]: <{fu.DEFAULT_WIDTH}}"
            f"{str(row[2]): <{fu.DEFAULT_WIDTH}}"
            f"{str(row[3]): <{fu.DEFAULT_WIDTH}}"
        )
    return booking_code_list

def booking_to_movie_list_print(
        movie_code_list : list,
        movie_code : str,
        movie_list_dict : dict,
        movie_seats_dict : dict,
    ) -> None:
    if movie_code not in movie_code_list:
        raise ValueError("Please enter the valid movie code!")
    else:
        #format: [['002', 'Joker', 'cinema002', '19:00', '22:00']]
        booking_movie_list : list = ccsf.read_list_from_cache(dictionary_cache= movie_list_dict,code= movie_code)
        movie_list_print_with_format(
            data_list= booking_movie_list,
            movie_list_dict= movie_list_dict,
            movie_seats_dict= movie_seats_dict
        )

def movie_list_print_with_format(
        data_list : list,
        movie_list_dict: dict,
        movie_seats_dict: dict
    ) -> None:
    print(f"{'Movie Code': <{fu.DEFAULT_WIDTH}}"
          f"{'Movie Name': <{fu.DEFAULT_WIDTH}}"
          f"{'Cinema Location': <{fu.DEFAULT_WIDTH}}"
          f"{'Start Time': <{fu.DEFAULT_WIDTH}}"
          f"{'End Time': <{fu.DEFAULT_WIDTH}}"
          f"{'Date': <{fu.DEFAULT_WIDTH}}"
          f"{'Price': <{fu.DEFAULT_WIDTH}}"
          f"{'Capacity': <{fu.DEFAULT_WIDTH}}")
    print("-" * (fu.DEFAULT_WIDTH * 8 + 1))
    for row in data_list:
        seat_list_temp : list = ccsf.read_seats_from_cache(cache_dictionary=movie_seats_dict, code=row[0])
        for data in row[0:6]:
            print(f"{data: <{fu.DEFAULT_WIDTH}}", end="")

        print(f"{pf.get_price(movie_list_dict= movie_list_dict,code= row[0] ): <{fu.DEFAULT_WIDTH}}",end= "")
        print(f"{msf.get_capacity(seat_list_temp): <{fu.DEFAULT_WIDTH}}", end ="")
        print()

def code_range_create(code_list : list,code_location : int) -> list:
    code_range_list : list =[]
    for row in code_list:
        code_range_list.append(row[code_location])
    return code_range_list

def book_movie_operation(
        user_id : str,
        code_range : list,
        movie_list_dict:dict,
        booking_data_dict:dict,
        movie_seats_dict:dict,
        customer_data_dict:dict,
    ) -> None:
    movie_code : str = fu.element_input(element_name= "movie code",input_range= code_range)
    book_movie_system(
        movie_code= movie_code,
        user_id= user_id,
        booking_data_dict= booking_data_dict,
        movie_list_dict= movie_list_dict,
        movie_seats_dict= movie_seats_dict,
        customer_data_dict= customer_data_dict,
    )

def book_movie_system(
        movie_code : str,
        user_id : str,
        booking_data_dict : dict,
        movie_list_dict : dict,
        movie_seats_dict : dict,
        customer_data_dict : dict,
    ) -> None:
    try:
        booking_movie_seats = movie_list_to_movie_seats_print(
            movie_code=movie_code,
            movie_seats_dict= movie_seats_dict
        )
        x_range = sv.x_range_calculate(movie_seats=booking_movie_seats)
        y_range = sv.y_range_calculate(movie_seats=booking_movie_seats)
        first_attempt = True
        try_again = False
        while first_attempt or try_again:
            first_attempt = False
            x_pointer = book_movie_input(
                range_list= x_range,
                name_in_input= "Column"
            )
            movie_list_to_movie_seats_print(
                movie_code=movie_code,
                x_pointer=x_pointer,
                movie_seats_dict= movie_seats_dict
            )
            y_pointer = book_movie_input(
                range_list= y_range,
                name_in_input= "Row"
            )
            movie_list_to_movie_seats_print(
                movie_code=movie_code,
                x_pointer=x_pointer,
                y_pointer=y_pointer,
                movie_seats_dict= movie_seats_dict
            )
            seats_value =msf.movie_seats_specify_value(
                movie_seats=booking_movie_seats,
                x_axis=x_pointer,
                y_axis=y_pointer
            )
            booking_status =book_movie_buy(seats_value= seats_value)
            if booking_status:
                try_again = False
                book_price : int = pf.get_price(
                    movie_list_dict= movie_list_dict,
                    code = movie_code
                )
                if not pf.pay_money(
                        customer_id=user_id,
                        price=book_price,
                        customer_dict= customer_data_dict
                ):
                    print ("Purchased Failed,No Enough Money!")
                    return
                booking_list : list = ccsf.read_list_from_cache(dictionary_cache=booking_data_dict)
                book_id : str = idg.generate_code_id(
                    code_list= booking_list,
                    prefix_generate= "B",
                    code_location= 0,
                    number_of_prefix= 1,
                    prefix_got_digit= False,
                    code_id_digit_count= 4
                )
                booking_data_list = _booking_data_create(
                    book_id= book_id,
                    user_id= user_id,
                    movie_code= movie_code,
                    booking_date= datetime.datetime.now().strftime('%Y/%m/%d'),
                    booking_or_pay= "1",
                    x_seat= str(x_pointer),
                    y_seat= str(y_pointer),
                    price= str(book_price),source= "online"
                )
                ccsf.list_dictionary_update(dictionary= booking_data_dict,list_to_add= booking_data_list)

            else: try_again = True

    except Exception as e:
        raise Exception(f"UNKNOWN ERROR,ERROR:{e}")

def book_movie_input(range_list : list,name_in_input : str) -> int:
    while True:
        try:
            pointer : int = int(input(
                f"Please enter the {name_in_input} number "
                f"({range_list[0]} to {range_list[1]}): "
            ))
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
    while True:
        if seats_value == "0":
            user_input = str(input("This seat is available. Are you (S)ure to book? or (C)ancel? "))
            if user_input.lower() == 's':
                print("Booking successful!")
                return True
            elif user_input.lower() == 'c':
                print("Booking cancelled.")
                return False
            else: print("Please Enter S(s) or C(c)")
        elif seats_value == "1":
            print("This seat is already booked. Please choose another one.")
            return False
        else:
            print("This is an invalid seat (e.g., an aisle). Please choose another one.")
            return False



def _booking_data_create (
        book_id : str,
        user_id : str,
        movie_code : str,
        booking_date : str,
        booking_or_pay : str,
        x_seat : str,
        y_seat : str,
        price : str,
        source : str
    ) -> list:
    booking_data_list : list = []
    booking_data_list.append(book_id)
    booking_data_list.append(user_id)
    booking_data_list.append(movie_code)
    booking_data_list.append(booking_date)
    booking_data_list.append(booking_or_pay)
    booking_data_list.append(x_seat)
    booking_data_list.append(y_seat)
    booking_data_list.append(price)
    booking_data_list.append(source)
    return booking_data_list




def movie_list_to_movie_seats_print(
        movie_code : str,
        movie_seats_dict : dict,
        x_pointer = -1,
        y_pointer = -1
    ) -> list:

    movie_seats_list : list = ccsf.read_seats_from_cache(cache_dictionary=movie_seats_dict,code=movie_code)
    print()
    print("-" * int(fu.DEFAULT_WIDTH * 1.8))
    sv.print_movie_seat_as_emojis(movie_seats_list,x_pointer,y_pointer)
    print("-" * int(fu.DEFAULT_WIDTH * 1.8))
    print(f"Movie Code:{movie_code}")
    return movie_seats_list

def check_all_movie_list(movie_list_dict : dict,movie_seats_dict : dict) -> list:
    movie_header_list : list = movie_list_dict["header"]
    header_dict : dict = fu.header_location_get(movie_header_list)
    movie_list_all : list = ccsf.read_list_from_cache(dictionary_cache=movie_list_dict)
    movie_list_print_with_format(
        data_list= movie_list_all,
        movie_list_dict= movie_list_dict,
        movie_seats_dict=movie_seats_dict,
    )
    return code_range_create(code_list= movie_list_all,code_location= header_dict["movie_code"])


def cancel_booking_operation(user_id : str, booking_data_dict : dict,customer_data_dict : dict,booking_code_range : list= None) -> None:
    if booking_code_range is None: booking_code_range : list = check_ticket_bought(
        customer_code= user_id,
        booking_data_dict= booking_data_dict,
        return_booking_code= True
    )
    while True:
        if not booking_code_range:
            print ("You haven't bought any ticket")
            return
        booking_code_cancel : str = fu.element_input(
            element_name= 'code that you want to cancel',
            input_range= booking_code_range
        )
        print("Are you sure you want to cancel the booking? (y/n)")
        user_command : str = fu.element_input(element_name="command",input_range=['Y','y','N','n'])
        if user_command.lower() == "n":
            return
        if user_command.lower() == "y":
            pf.return_money(booking_dict= booking_data_dict,customer_dict= customer_data_dict,booking_id=booking_code_cancel,customer_id=user_id )
            ccsf.dictionary_delete(dictionary=booking_data_dict,key_to_delete=booking_code_cancel)
            cnsv.sync_all()
            return





def customer(customer_id : str,
             booking_data_dict= None,
             movie_list_dict= None,
             movie_seats_dict= None,
             customer_data_dict= None,
    ) -> None:
    if booking_data_dict is None: booking_data_dict = ddf.BOOKING_DATA_DICTIONARY
    if movie_list_dict is None:  movie_list_dict = ddf.MOVIE_LIST_DICTIONARY
    if movie_seats_dict is None: movie_seats_dict = ddf.MOVIE_SEATS_DICTIONARY
    if customer_data_dict is None: customer_data_dict = ddf.CUSTOMER_DATA_DICTIONARY
    cnsv.sync_all()
    print("Welcome to the Movie Booking System!")
    while True:
        match fu.get_operation_choice(
            "Select Your Operation",
            "Check Ticket Bought",
            "Check All Movie",
            'Exit'
        ):
            case "1":
                booking_code_range : list = check_ticket_bought(
                    customer_code=customer_id,
                    return_booking_code=True,
                    booking_data_dict= booking_data_dict,
                )
                match fu.get_operation_choice("Select Your Operation",'Cancel Booking','Exit'):
                    case "1":
                        cancel_booking_operation(
                            user_id= customer_id,
                            booking_data_dict= booking_data_dict,
                            customer_data_dict= customer_data_dict,
                            booking_code_range= booking_code_range,
                        )
                    case '2':
                        pass
            case "2":
                code_range = check_all_movie_list(
                    movie_list_dict= movie_list_dict,
                    movie_seats_dict= movie_seats_dict,
                )
                match fu.get_operation_choice("Select Your Operation",'book movie','exit'):
                    case "1":
                        book_movie_operation(
                            user_id= customer_id,
                            code_range= code_range,
                            movie_list_dict= movie_list_dict,
                            booking_data_dict= booking_data_dict,
                            movie_seats_dict= movie_seats_dict,
                            customer_data_dict= customer_data_dict,
                        )
                    case "2":
                        pass
            case "3":
                break
        fu.empty_input("Press Enter to continue...")
        try:
            cnsv.sync_all()
        except ValueError as e:
            if "schedule" in e.args[0] or "Sort" in e.args[0]:
                pass



#JUST TEST
if __name__ == '__main__':
    ddf.init_all_dictionary()
    customer(customer_id = "C001")
    #user_input = str(input("empty"))
    #check_all_movie_list()
    # valid_movie_code = check_ticket_bought(customer_code= "C001",return_booking_code= False)
    # user_input = str(input("Please enter the code: "))
    # booking_to_movie_list_print(movie_code_list= valid_movie_code,movie_code= user_input)
    #book_movie_operation(movie_code= "003",movie_seats_csv= "movie_seat.csv",booking_data_csv= "booking_data.csv",
    #                     template_seats_csv= "cinema_seats.csv",user_id= "C001")
    # cancel_booking_operation(user_id= "C001",booking_data_csv= "booking_data.csv",movie_list_csv= "movie_list.csv"
    #                          ,movie_seats_csv= "movie_seat.csv",template_seats_csv= "cinema_seats.csv")


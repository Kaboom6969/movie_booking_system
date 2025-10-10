from main_program.Library.data_communication_framework import cache_csv_sync_framework as ccsf
from main_program.Library.cache_framework import data_dictionary_framework as ddf
from main_program.Library.movie_booking_framework import id_generator as idg
from main_program.Library.movie_booking_framework import valid_checker as vc
from main_program.Library.movie_booking_framework import framework_utils as fu
from main_program.Library.movie_booking_framework import cinema_services as cnsv
from main_program.Library.movie_booking_framework.framework_utils import empty_input
from main_program.Library.movie_booking_framework.movie_seats_framework import get_capacity



def movie_list_print_with_format(
        data_list: list,
        DEFAULT_WIDTH: int = 30,
        movie_seats_dict: dict = None
) -> None:
    if movie_seats_dict is None: movie_seats_dict = ddf.MOVIE_SEATS_DICTIONARY
    print(
        f"{'Movie Code': <{DEFAULT_WIDTH}}"
        f"{'Movie Name': <{DEFAULT_WIDTH}}"
        f"{'Cinema Location': <{DEFAULT_WIDTH}}"
        f"{'Start Time': <{DEFAULT_WIDTH}}"
        f"{'End Time': <{DEFAULT_WIDTH}}"
        f"{'Date': <{DEFAULT_WIDTH}}"
        f"{'Price': <{DEFAULT_WIDTH}}"
        f"{'Capacity': <{DEFAULT_WIDTH}}"
    )
    print("-" * (DEFAULT_WIDTH * 8 + 1))
    for row in data_list:
        seat_list_temp: list = ccsf.read_seats_from_cache(cache_dictionary=movie_seats_dict, code=row[0])
        for data in row:
            print(f"{data: <{DEFAULT_WIDTH}}", end="")
        print(f"{get_capacity(seat_list_temp): <{DEFAULT_WIDTH}}", end ="")
        print()

def add_movie_operation (
        cinema_seats_dict:dict=None,
        movie_list_dict:dict=None,
        movie_seats_dict:dict=None,
        cinema_device_dict:dict=None
) -> None:
    if cinema_seats_dict is None: cinema_seats_dict = ddf.CINEMA_SEATS_DICTIONARY
    if movie_list_dict is None: movie_list_dict= ddf.MOVIE_LIST_DICTIONARY
    if movie_seats_dict is None: movie_seats_dict = ddf.MOVIE_SEATS_DICTIONARY
    if cinema_device_dict is None: cinema_device_dict = ddf.CINEMA_DEVICE_DICTIONARY
    movie_code_list = fu.get_code_range(movie_list_dict)
    cinema_code_range_filtered = sorted(list(set(fu.get_code_range(cinema_seats_dict))))
    movie_list_header: list = movie_list_dict["header"]
    movie_code = idg.generate_code_id(
        code_list=movie_code_list,
        prefix_generate="",
        code_location=movie_list_dict["code_location"],
        number_of_prefix=0,
        prefix_got_digit= False,
        code_id_digit_count=4
    )
    added_movie_list: list = [movie_code]
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
    movie_list_header: list = movie_list_dict["header"]
    movie_code_range: list = fu.get_code_range(movie_list_dict)
    movie_code_to_delete = fu.element_input(element_name=movie_list_header[0],input_range= movie_code_range)
    movie_list_print_with_format(
        data_list= [
            ccsf.read_list_from_cache(
            dictionary_cache= movie_list_dict,
            code=movie_code_to_delete
            )
        ]
    )
    print (f"Are You Sure You Want Delete Movie Code: {movie_code_to_delete}?")
    user_operation:str = fu.element_input(element_name= "command (Y/N)",input_range= ["Y","y","N","n"])
    if user_operation.lower() == "y":
        ccsf.dictionary_delete(dictionary=movie_list_dict,key_to_delete=movie_code_to_delete)
        # This is just for test,after compile,the sync all function will be placed at the bottom of manager()
    if user_operation.lower() == "n":
        return

def modify_movie_operation(
        movie_list_dict:dict=None,
        movie_seats_dict:dict=None,
        cinema_device_dict:dict=None,
        cinema_seats_dict:dict=None
) -> None:
    if movie_list_dict is None: movie_list_dict= ddf.MOVIE_LIST_DICTIONARY
    if movie_seats_dict is None: movie_seats_dict = ddf.MOVIE_SEATS_DICTIONARY
    if cinema_device_dict is None: cinema_device_dict = ddf.CINEMA_DEVICE_DICTIONARY
    if cinema_seats_dict is None: cinema_seats_dict = ddf.CINEMA_SEATS_DICTIONARY
    movie_list_header: list = movie_list_dict["header"]
    movie_code_range: list = fu.get_code_range(movie_list_dict)
    cinema_code_range_filtered = sorted(list(set(fu.get_code_range(cinema_seats_dict))))
    movie_code_to_modify = fu.element_input(element_name=movie_list_header[0],input_range= movie_code_range)
    movie_list_print_with_format(
        data_list= [
            ccsf.read_list_from_cache(
                dictionary_cache= movie_list_dict,
                code=movie_code_to_modify
            )
        ]
    )
    print (f"Are You Sure You Want Modify Movie Code: {movie_code_to_modify}?")
    user_operation: str = fu.element_input(element_name="command (Y/N)", input_range=["Y", "y", "N", "n"])
    if user_operation.lower() == "y":
        movie_list_specify: list = ccsf.read_list_from_cache(dictionary_cache= movie_list_dict,code=movie_code_to_modify)
        selected_modify,header_to_modify = fu.element_input(
            element_name= "data that you want to modify",
            input_range= movie_list_header[1:],
            return_range_index=True
        )
        if "time" in selected_modify: data_to_modify = fu.element_input(
            element_name= selected_modify,
            valid_check_func= vc.time_valid_check
        )
        elif "date" in selected_modify: data_to_modify = fu.element_input(
            element_name= selected_modify,
            valid_check_func= vc.date_valid_check
        )
        elif "CINEMA" in selected_modify: data_to_modify = fu.element_input(
            element_name= selected_modify,
            input_range=cinema_code_range_filtered
        )
        elif "price" in selected_modify: data_to_modify = fu.element_input(
            element_name= selected_modify,
            valid_check_func=vc.number_valid_check
        )
        elif "discount" in selected_modify:
            discount_percent_range: list =[str(i).join("%") for i in range(0,101)]
            data_to_modify = fu.element_input(element_name= selected_modify,input_range= discount_percent_range)
        else: data_to_modify = fu.element_input(element_name= selected_modify)
        movie_list_specify[header_to_modify + 1] = data_to_modify
        ccsf.list_dictionary_update(dictionary=movie_list_dict,list_to_add=movie_list_specify)
    if user_operation.lower() == "n":
        return

def total_and_average_money_earn (booking_data_list: list,booking_data_header_location: dict) -> tuple[int,float]:
    total_money = 0
    for row in booking_data_list:
        total_money += int(row[booking_data_header_location["price"]])
    average_money: float = total_money/len(booking_data_list)
    return total_money,average_money

def total_booking_count (booking_data_list: list) -> int:
    return len(booking_data_list)

def highest_movie_code_booking (booking_data_list: list, booking_data_header_location: dict) -> str:
    movie_code_booking: dict = {}
    for row in booking_data_list:
        if movie_code_booking.get(row[booking_data_header_location["Movie Code"]]) is None:
            movie_code_booking[row[booking_data_header_location["Movie Code"]]] = 0
        movie_code_booking[row[booking_data_header_location["Movie Code"]]] += 1
    movie_code_highest: str = max(movie_code_booking,key=movie_code_booking.get)
    return movie_code_highest

def booking_data_source_count (source: str,booking_data_list: list,booking_data_header_location: dict) -> int:
    source_count: int = 0
    for row in booking_data_list:
        if row[booking_data_header_location["Source"]] == source: source_count += 1
    return source_count

def survey_generate(booking_data_dict: dict= None) -> None:
    if booking_data_dict is None: booking_data_dict = ddf.BOOKING_DATA_DICTIONARY
    booking_data_header_location: dict = fu.header_location_get(booking_data_dict["header"])
    booking_data_list: list = ddf.read_list_from_cache(dictionary_cache=booking_data_dict)
    STARTER_WIDTH = 4
    CONTENT_WIDTH = 25
    SURVEY_WIDTH = 100
    TBC: str = f"{'':<{STARTER_WIDTH}}{'Total Booking Count:':<{CONTENT_WIDTH}}"
    OBC: str = f"{'':<{STARTER_WIDTH}}{'Online Booking Count:':<{CONTENT_WIDTH}}"
    CBC: str = f"{'':<{STARTER_WIDTH}}{'Clerk Booking Count:':<{CONTENT_WIDTH}}"
    TME: str = f"{'':<{STARTER_WIDTH}}{'Total Money Earn:':<{CONTENT_WIDTH}}"
    AME: str = f"{'':<{STARTER_WIDTH}}{'Average Money Earn:':<{CONTENT_WIDTH}}"
    MCBS: str = f"{'':<{STARTER_WIDTH}}{'Movie Code Best Seller:':<{CONTENT_WIDTH}}"
    total_booking = total_booking_count(booking_data_list=booking_data_list)
    online_booking_count = booking_data_source_count(
        source= "online",
        booking_data_list= booking_data_list,
        booking_data_header_location= booking_data_header_location
    )
    clerk_booking_count = booking_data_source_count(
        source= "Clerk",
        booking_data_list= booking_data_list,
        booking_data_header_location= booking_data_header_location
    )
    total_money,average_money = total_and_average_money_earn(
        booking_data_list= booking_data_list,
        booking_data_header_location= booking_data_header_location
    )
    highest_movie_code_sell = highest_movie_code_booking(
        booking_data_list= booking_data_list,
        booking_data_header_location= booking_data_header_location
    )
    print('+','-'*(SURVEY_WIDTH - 2),'+')
    print(f'|{TBC}{total_booking: <{SURVEY_WIDTH - len(TBC)}}|')
    print(f'|{OBC}{online_booking_count: <{SURVEY_WIDTH - len(OBC)}}|')
    print(f'|{CBC}{clerk_booking_count: <{SURVEY_WIDTH - len(CBC)}}|')
    print(f'|{TME}{total_money: <{SURVEY_WIDTH - len(TME)}}|')
    print(f'|{AME}{average_money: <{SURVEY_WIDTH - len(AME)}}|')
    print(f'|{MCBS}{highest_movie_code_sell: <{SURVEY_WIDTH - len(MCBS)}}|')
    print('+', '-' *(SURVEY_WIDTH - 2), '+')

def set_discount (movie_list_dict : dict,discount_rate: int,movie_code: str="all") -> None:
    movie_list_header_location : dict = fu.header_location_get(
        header_list= movie_list_dict["header"],
        dict_version= True
    )
    if movie_code == "all":
        for key in movie_list_dict.keys():
            if key in ["header", "base file name", "code_location"]: continue
            movie_list_dict[key][movie_list_header_location["discount"]] = discount_rate
    else:
        movie_list_dict[movie_code][movie_list_header_location["discount"]] = discount_rate


def set_discount_operation(movie_list_dict : dict = None) -> None:

    def temp_func_for_percent(discount) -> tuple[bool,str]:
        if 0 > int(discount) > 100: return False,"1 - 100"
        return True,""


    if movie_list_dict is None: movie_list_dict=ddf.MOVIE_LIST_DICTIONARY
    match fu.get_operation_choice(
        "Discount Operation",
        "Set Specify Movie Code",
        "Set All"
    ):
        case '1':
            movie_code = fu.element_input(element_name= "Movie Code",input_range=list(movie_list_dict.keys()))
            discount_rate = fu.element_input(element_name= "Discount Rate",valid_check_func= temp_func_for_percent)
            set_discount(
                movie_list_dict=movie_list_dict,
                discount_rate=int(discount_rate),
                movie_code=movie_code
            )
        case '2':
            discount_rate = fu.element_input(element_name= "Discount Rate",valid_check_func= temp_func_for_percent)
            set_discount(
                movie_list_dict=movie_list_dict,
                discount_rate=int(discount_rate)
            )

def manager(manager_id : str) -> None:
    while True:
        print("Welcome to Movie Booking System")
        match fu.get_operation_choice(
            'Select Your Operation',
            'Add Movie',
            'Delete Movie',
            'Modify Movie',
            'Set Discount',
            'Generate Survey',
            'Exit'
        ):
            case "1":
                add_movie_operation()
            case "2":
                delete_movie_operation()
            case "3":
                modify_movie_operation()
            case "4":
                set_discount_operation()
            case "5":
                survey_generate()
            case "6":
                break
            case _:
                raise ValueError(
                    "case '_' isn't callable in normal progress!\n"
                    "Please Check your element_input parameters!"
                )
        fu.empty_input(message="Press Enter to continue...")
        try:
            cnsv.sync_all()
        except ValueError as e:
            if "schedule" in e.args[0] or "Sort" in e.args[0]:
                error_message = e.args[0]
                conflict_data = e.args[1]
                print(error_message)
                print(f"conflict schedule:{conflict_data}\n")
                match fu.get_operation_choice(
                    'Please enter Your Operation',
                    'Manual Sort',
                    'Auto Sort(Recommended)',
                    'Discard this change'
                ):
                    case "1":
                        modify_movie_operation()
                    case "2":
                        auto_sort_status,still_conflict_data = cnsv.schedule_auto_sort(
                            schedule_conflict_list= conflict_data
                        )
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

        


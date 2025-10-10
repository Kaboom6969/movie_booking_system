from datetime import datetime

from main_program.Library.movie_booking_framework import seat_visualizer as sv
from main_program.Library.movie_booking_framework import cinema_services as cnsv
from main_program.Library.movie_booking_framework import id_generator as idg
from main_program.Library.movie_booking_framework.framework_utils import header_location_get
from main_program.Library.payment_framework import payment_framework as pf
from main_program.Library.movie_booking_framework import movie_seats_framework as msf
from main_program.Library.system_login_framework.login_system import *
from main_program.Library.data_communication_framework import cache_csv_sync_framework as ccsf
from main_program.Library.cache_framework import data_dictionary_framework as ddf
from main_program.Library.movie_booking_framework import framework_utils as fu


def get_Data_Directory_path(path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.normpath(os.path.join(base_dir, "..", "..", "Data/" + path))
    return data_path




def get_and_print_booking_data(input_movie_code, booking_data_dict: dict = None):
    if booking_data_dict is None: booking_data_dict = ddf.BOOKING_DATA_DICTIONARY
    booking_data_list = ccsf.read_list_from_cache(dictionary_cache=booking_data_dict)
    # header = [Book ID,User ID,Movie Code,Date,(1:booking 2:paid),seat(x-axis),seat(y-axis),Source]
    header: list = booking_data_dict.get("header")
    print(
        f"{header[0]:<10}{header[1]:<10}{header[2]:<13}"
        f"{header[3]:<13}{header[4]:<21}{header[5]:<15}"
        f"{header[6]:<15}{header[7]:<15}{header[8]:<15}"
    )
    filtered_list = []
    for row in booking_data_list:
        booking_id, user_id, movie_code, date, status, x_axis, y_axis, price, source = row
        if input_movie_code == movie_code:
            print(
                f"{booking_id:<10}{user_id:<10}{movie_code:<13}"
                f"{date:<13}{status:<21}{x_axis:<15}"
                f"{y_axis:<15}{price:<15}{source:<15}"
            )
            filtered_list.append(row)
    return filtered_list


def select_movie(movie_list):
    while True:
        print("\n")
        print(movie_list)
        # 输入代码
        input_movie_code = input("Please enter your movie code: \n")
        for movie in movie_list:
            if movie[0] == input_movie_code:
                return input_movie_code
        else:
            print("Please enter valid movie code")


def generate_seat_axis(column, row):
    return f"{column},{row}"


def check_booking_full(movie_seat_list):
    capacity = msf.get_capacity(movie_seat_list)
    if capacity == 0:
        return True
    return False


def select_seat(movie_seat_list):
    booking_full = check_booking_full(movie_seat_list)
    if booking_full:
        print("Booking is full")
        return
    while True:
        while True:
            sv.print_movie_seat_as_emojis(movie_seat_list)
            try:
                print(f"\nrow should be between 1 and {len(movie_seat_list)}")
                row = int(input("Please enter the row number: "))  # y_axis
                if row < 1 or row > len(movie_seat_list):
                    print("Please enter a valid row number")
                else:
                    sv.print_movie_seat_as_emojis(movie_seat_list, -1, row)
                    break
            except ValueError as e:
                print(e)
        while True:
            try:
                print(f"\ncolumn should be between 1 and {len(movie_seat_list[0])}")
                column = int(input("Please enter the column number: "))
                if column < 1 or column > len(movie_seat_list[0]):
                    print("Please enter a valid row number")  # x_axis
                else:
                    sv.print_movie_seat_as_emojis(movie_seat_list, column, row)
                    break
            except ValueError as e:
                print(e)

        if not sv.movie_seats_pointer_valid_check(movie_seat_list, column, row):
            print(f"Invalid seat, please try again")
            continue
        try:
            seat_value = msf.movie_seats_specify_value(movie_seat_list, column, row)
        except IndexError as e:
            print(e)
            continue
        if seat_value == '-1':
            sv.print_movie_seat_as_emojis(movie_seat_list, column, row)
            print("Invalid seat, please try again")
        elif seat_value == '1':
            sv.print_movie_seat_as_emojis(movie_seat_list, column, row)
            print("This seat is already taken. Please enter another one")
        else:
            return column, row


def booking(
        movie_seat_list,
        input_movie_code,
        user_id: str = None,
        customer_id: str = None,
        booking_method: str = '1',
        booking_data_dict: dict = None,
        movie_seats_dict: dict = None,
        movie_list_dict: dict = None,
        customer_dict: dict = None
):
    if booking_data_dict is None: booking_data_dict = ddf.BOOKING_DATA_DICTIONARY
    if movie_seats_dict is None: movie_seats_dict = ddf.MOVIE_SEATS_DICTIONARY
    if movie_list_dict is None: movie_list_dict = ddf.MOVIE_LIST_DICTIONARY
    if customer_dict is None: customer_dict = ddf.CUSTOMER_DATA_DICTIONARY
    column, row = select_seat(movie_seat_list=movie_seat_list)
    today = datetime.today().strftime('%Y/%m/%d')
    booking_data_list: list = ccsf.read_list_from_cache(booking_data_dict)
    book_price: int = pf.get_price(movie_list_dict=movie_list_dict, code=input_movie_code)
    if customer_id is not None:
        purchased_status = pf.pay_money(customer_dict=customer_dict, customer_id=customer_id, price=book_price)
        if not purchased_status:
            print("Purchased Failed")
            return
    booking_id = idg.generate_code_id(
        code_list=booking_data_list,
        prefix_generate="B",
        code_location=0,
        number_of_prefix=1,
        prefix_got_digit=False,
        code_id_digit_count=4
    )
    book_price = pf.get_price(movie_list_dict=movie_list_dict, code=input_movie_code)
    data_row = [booking_id, user_id, input_movie_code, today, 2, column, row, book_price, 'Clerk']
    ccsf.list_dictionary_update(dictionary=booking_data_dict, list_to_add=data_row)
    print("Purchased successfully")


def handle_booking(movie_seats_csv, booking_data_csv, customer_csv, movie_seat_list,
                   input_movie_code, user_id):
    while True:
        try:
            choice = fu.get_operation_choice("Please Select Your Choice", 'cash', 'account balance', 'quit')
            if choice == '1':
                path = fu.get_path(movie_seats_csv)
                booking(movie_seat_list=movie_seat_list, input_movie_code=input_movie_code, user_id=user_id)
                break
            elif choice == '2':
                path = fu.get_path(customer_csv)
                customer_id = login(path)
                if customer_id is not None:
                    booking(
                        movie_seat_list=movie_seat_list,
                        input_movie_code=input_movie_code,
                        user_id=user_id,
                        customer_id=customer_id,
                        booking_method=choice
                    )
                    break
            elif choice == '3':
                break
        except ValueError as e:
            print(e)


def checking_movie(input_movie_code: str, movie_seats_dict: dict = None):
    if movie_seats_dict is None: movie_seats_dict = ddf.MOVIE_SEATS_DICTIONARY
    movie_seat_list = ccsf.read_seats_from_cache(cache_dictionary=movie_seats_dict, code=input_movie_code)
    sv.print_movie_seat_as_emojis(movie_seat_list)
    capacity = msf.get_capacity(movie_seat_list)
    print(f"\n This movie seat capacity is {capacity}")


def check_booking_id(booking_data_2d_list, input_booking_id):
    for booking_data in booking_data_2d_list:
        if input_booking_id == booking_data[0]:
            return input_booking_id
    return None


def get_user_seat_axis(booking_data_list, input_booking_id):
    for booking_data in booking_data_list:
        if input_booking_id == booking_data[0]:
            return booking_data[5], booking_data[6]
    return None

def get_customer_id(booking_data_list, input_booking_id):
    for booking_data in booking_data_list:
        if input_booking_id == booking_data[0]:
            return booking_data[1]
    return None

def get_user_booking_axis_and_booking_id(booking_data_list):
    while True:
        input_booking_id = input('Please enter your booking id (press Enter to cancel): \n')
        if input_booking_id.strip() == '':
            break
        booking_id = check_booking_id(booking_data_list, input_booking_id)
        if booking_id is not None:
            column, row = get_user_seat_axis(booking_data_list, input_booking_id)  # x_axis  # y_axis
            return column, row, booking_id
        else:
            print("Please enter valid booking id")
            continue

    return None, None, None


def check_booking_data(input_movie_code, booking_data_dict: dict = None):
    if booking_data_dict is None: booking_data_dict = ddf.BOOKING_DATA_DICTIONARY
    booking_data_list: list = ccsf.read_list_from_cache(dictionary_cache=booking_data_dict)
    for row in booking_data_list:
        if input_movie_code == row[2]:
            return True
    print("No Booking Data Found!")
    return False


def modify_booking_data(
        booking_id,
        column,
        row,
        code_location=0,
        booking_data_dict=None
):
    if booking_data_dict is None: booking_data_dict = ddf.BOOKING_DATA_DICTIONARY
    original_row: list = ccsf.read_list_from_cache(dictionary_cache=booking_data_dict, code=booking_id)
    original_row[5] = str(column)
    original_row[6] = str(row)
    original_row[8] = 'Clerk'
    updated_list: list = original_row
    ccsf.list_dictionary_update(dictionary=booking_data_dict, list_to_add=updated_list)


def modify_booking(
        movie_seat_list,
        input_movie_code,
        user_id,
        booking_data_dict=None,
        movie_seats_dict=None,
        customer_dict=None
):
    if booking_data_dict is None: booking_data_dict = ddf.BOOKING_DATA_DICTIONARY
    if movie_seats_dict is None: movie_seats_dict = ddf.MOVIE_SEATS_DICTIONARY
    if customer_dict is None:customer_dict = ddf.CUSTOMER_DATA_DICTIONARY
    booking_data_exist = check_booking_data(input_movie_code)
    if booking_data_exist:
        while True:
            booking_data_list = get_and_print_booking_data(input_movie_code)
            column, row, booking_id = get_user_booking_axis_and_booking_id(booking_data_list)
            if booking_id is None:
                break
            customer_id = get_customer_id(booking_data_list, booking_id)
            choice = fu.get_operation_choice(
                'Please enter your choice',
                'cancel booking',
                'modify booking',
                'quit'
            )
            # cancel booking(1), modify booking(2), quit(3)
            if choice == '1':
                start_with_c = user_id_start_with_c(customer_id)
                if start_with_c:
                    pf.return_money(booking_data_dict, customer_dict, booking_id, customer_id)
                    print('Your money has been returned')
                ccsf.dictionary_delete(dictionary=booking_data_dict, key_to_delete=booking_id)
                print('Cancel booking successfully')
                break
            elif choice == '2':
                column, row = select_seat(movie_seat_list=movie_seat_list)
                modify_booking_data(booking_id=booking_id, column=column, row=row)
                print("Modify successfully")
                break
            elif choice == 3:
                break
        cnsv.sync_all()


def modify_customer_seat(movie_seat_list):
    sv.print_movie_seat_as_emojis(movie_seat_list)


def get_movie_list_data(movie_2d_list: list, input_movie_code: str) -> list:
    movie_data_list = []
    for data in movie_2d_list:
        if data[0] == input_movie_code:
            movie_data_list = data
    return movie_data_list


def generate_receipt_text(movie_list_data, booking_data_dict, booking_id):
    movie_name = movie_list_data[1]
    cinema = movie_list_data[2]
    start = movie_list_data[3]
    end = movie_list_data[4]
    movie_date = movie_list_data[5]
    movie_price = movie_list_data[6]

    user_id = booking_data_dict[booking_id][1]
    booking_date = booking_data_dict[booking_id][3]
    column = booking_data_dict[booking_id][5]
    row = booking_data_dict[booking_id][6]
    movie_price_discount = booking_data_dict[booking_id][7]

    discount = round(get_discount(discount_price=movie_price_discount,original_price=movie_price),2) * 100

    receipt = f"""
========================================
              MOVIE RECEIPT
========================================
Booking ID     : {booking_id}
User ID        : {user_id}
Booking Date   : {booking_date}
----------------------------------------
Movie Name     : {movie_name}
Cinema         : {cinema}
Date           : {movie_date}
Start Time     : {start}
End Time       : {end}
Seat           : [{column},{row}]
----------------------------------------
Original Price : RM {movie_price}
Discount       : {discount} %
Final Price    : {movie_price_discount}
========================================
"""
    return receipt

def print_booking_data(booking_data_dict: dict = None):
    if booking_data_dict is None: booking_data_dict = ddf.BOOKING_DATA_DICTIONARY
    booking_data_list = ccsf.read_list_from_cache(dictionary_cache=booking_data_dict)
    # header = [Book ID,User ID,Movie Code,Date,(1:booking 2:paid),seat(x-axis),seat(y-axis),Source]
    header: list = booking_data_dict.get("header")
    print(
        f"{header[0]:<10}{header[1]:<10}{header[2]:<13}"
        f"{header[3]:<13}{header[4]:<21}{header[5]:<15}"
        f"{header[6]:<15}{header[7]:<15}{header[8]:<15}"
    )
    filtered_list = []
    for row in booking_data_list:
        booking_id, user_id, movie_code, date, status, x_axis, y_axis, price, source = row
        print(
            f"{booking_id:<10}{user_id:<10}{movie_code:<13}"
            f"{date:<13}{status:<21}{x_axis:<15}"
            f"{y_axis:<15}{price:<15}{source:<15}"
        )
        filtered_list.append(row)#[['B0001', 'C001', '0001', '2025/10/08', '1', '1', '1', '20', 'online'], ['B0002', 'K001', '0001', '2025/10/08', '2', '2', '2', '20', 'Clerk']]
    return filtered_list

def get_discount(original_price: str,discount_price: str) -> float:
    return 1 - int(discount_price) / int(original_price)

def generate_receipt(movie_list_dict: dict = None,booking_data_dict: dict = None,customer_data_dict: dict = None,):
    if movie_list_dict is None: movie_list_dict = ddf.MOVIE_LIST_DICTIONARY
    if booking_data_dict is None: booking_list_dict = ddf.BOOKING_DATA_DICTIONARY
    if customer_data_dict is None: customer_list_dict = ddf.CUSTOMER_DATA_DICTIONARY
    #get movie list
    movie_2d_list = ccsf.read_list_from_cache(dictionary_cache=movie_list_dict)
    #booking_data_exist = check_booking_data(input_movie_code)
    booking_data_2d_list = print_booking_data()
    while True:
        booking_id = input('Please enter your booking id: \n')
        booking_id = check_booking_id(booking_data_2d_list, booking_id)
        if booking_id is not None:
            break
        else:
            print("Invalid booking id, please try again")
    #if booking_data_exist:
    booking_data_dict: dict = {row[0]: row for row in booking_data_2d_list}
    print(booking_data_dict)
    user_movie_code = booking_data_dict[booking_id][2]
    movie_list_data = get_movie_list_data(movie_2d_list, user_movie_code)

    get_receipt = generate_receipt_text(movie_list_data, booking_data_dict, booking_id)
    print(get_receipt)


def clerk(user_id):
    cnsv.sync_all()
    while True:
        choice = fu.get_operation_choice(
            'Please enter your choice',
            'booking',
            'cancel or modify booking',
            'check movie seats',
            'print receipt',
            'quit'
        )
        if choice == '4':
            generate_receipt()
            input('Press enter to continue')
        if choice == '5':
            break

        # get movie list
        movie_list = ccsf.read_list_from_cache(dictionary_cache=ddf.MOVIE_LIST_DICTIONARY)
        # get user movie input
        input_movie_code = select_movie(movie_list)
        # get movie seat list
        movie_seat_list = ccsf.read_seats_from_cache(
            cache_dictionary=ddf.MOVIE_SEATS_DICTIONARY,
            code=input_movie_code)
        if choice == '1':
            handle_booking(
                movie_seats_csv="movie_seat.csv",
                booking_data_csv="booking_data.csv",
                customer_csv="customer.csv",
                movie_seat_list=movie_seat_list,
                input_movie_code=input_movie_code,
                user_id=user_id
            )
            input('Press enter to continue')
        elif choice == '2':
            modify_booking(
                movie_seat_list=movie_seat_list,
                input_movie_code=input_movie_code,
                user_id=user_id
            )
            input('Press enter to continue')
        elif choice == '3':
            checking_movie(input_movie_code=input_movie_code)
            input('Press enter to continue')
        cnsv.sync_all()

def user_id_start_with_c(user_id:str) -> bool:
    return bool(user_id.startswith('C') and user_id[1:].isdigit())

# 取消或修改booking
# 查看电影列表
# 打印订单3

def main():
    clerk(user_id='K001')



if __name__ == '__main__':
    ddf.init_all_dictionary()
    main()

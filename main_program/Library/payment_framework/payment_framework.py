from main_program.Library.movie_booking_framework import framework_utils as fu
from main_program.Library.cache_framework import data_dictionary_framework as ddf
from main_program.Library.data_communication_framework import  cache_csv_sync_framework as ccsf
def pay_money(customer_id:str,price:int,customer_dict: dict) -> bool:
    content_list = []
    customer_header_location : dict = fu.header_location_get(customer_dict["header"])
    customer_balance = int(customer_dict[customer_id][customer_header_location["user_balance"] - 1])
    if price > customer_balance:
        #balance not enough
        return False
    else:
        customer_balance -= price
        customer_dict[customer_id][customer_header_location["user_balance"] - 1] = customer_balance
        ccsf.list_cache_write_to_csv(list_csv=customer_dict["base file name"],list_dictionary_cache=customer_dict)
        return True

def return_money(booking_dict: dict,customer_dict: dict,booking_id:str,customer_id:str) -> bool:
    booking_header_location = fu.header_location_get(booking_dict["header"])
    customer_header_location = fu.header_location_get(customer_dict["header"])
    customer_balance = int(customer_dict[customer_id][customer_header_location['user_balance'] - 1])
    price = int(booking_dict[booking_id][booking_header_location['price'] - 1])
    customer_balance += price
    customer_dict[customer_id][customer_header_location["user_balance"] - 1] = customer_balance
    ccsf.list_cache_write_to_csv(list_csv=customer_dict["base file name"], list_dictionary_cache=customer_dict)
    return True

def get_price(movie_list_dict: dict,code : str) -> int:
    movie_header_list : list = movie_list_dict["header"]
    movie_header_location_dict : dict = fu.header_location_get(movie_header_list)
    movie_list_specify : list = ddf.read_list_from_cache(dictionary_cache= movie_list_dict,code= code)
    movie_price_location = movie_header_location_dict["original price"]
    movie_discount_location = movie_header_location_dict["discount"]
    movie_original_price : int = int(movie_list_specify[movie_price_location])
    movie_discount : float = float(movie_list_specify[movie_discount_location])
    movie_real_price : float = movie_original_price * (1 - movie_discount/100)
    return round(movie_real_price)
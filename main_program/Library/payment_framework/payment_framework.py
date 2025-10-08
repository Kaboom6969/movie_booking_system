from main_program.Library.movie_booking_framework import framework_utils as fu
from main_program.Library.cache_framework import data_dictionary_framework as ddf
def pay_money(customer_csv: str,customer_id:str,price:int) -> bool:
    customer_csv_path = fu.get_path(customer_csv)
    content_list = []
    with open(customer_csv_path,'r', newline="") as r:
        header = r.readline()
        content = r.read().strip().split('\n')
        for row_data in content:
            content_list.append(row_data.split(','))
    for list_data in content_list:
        if list_data[0] == customer_id:
            customer_balance = int(list_data[3])
            if price > customer_balance:
                #balance not enough
                return False
            else:
                customer_balance = customer_balance - price
                list_data[3] = str(customer_balance)
                with open(customer_csv_path, 'w', newline="") as w:
                    w.write(header)
                    for i in content_list:
                        line = ",".join(x.strip() for x in i)
                        w.write(line + "\n")
                    #payment successful
                    return True
    raise ValueError("Invalid customer_id")

def get_price(movie_list_dict: dict,code : str) -> int:
    movie_header_list : list = movie_list_dict["header"]
    movie_header_location_dict : dict = fu.header_location_get(movie_header_list)
    movie_list_specify : list = ddf.read_list_from_cache(dictionary_cache= movie_list_dict,code= code)
    movie_price_location = movie_header_location_dict["original price"]
    movie_discount_location = movie_header_location_dict["discount"]
    movie_original_price : int = int(movie_list_specify[movie_price_location])
    movie_discount : float = float(movie_list_specify[movie_discount_location].strip("%"))
    movie_real_price : float = movie_original_price * (1 - movie_discount/100)
    return round(movie_real_price)

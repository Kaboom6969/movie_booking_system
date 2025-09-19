from main_program.Library.movie_booking_framework.framework_utils import get_path
def pay_money(customer_csv: str,customer_id:str,price:int) -> bool:
    customer_csv_path = get_path(customer_csv)
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


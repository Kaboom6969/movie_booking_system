from main_program.Library.cache_framework import data_dictionary_framework as ddf
from main_program.Library.data_communication_framework import cache_csv_sync_framework as ccsf
from main_program.Library.movie_booking_framework import cinema_services as cnsv, cinema_services
from main_program.Library.system_login_framework import login_system as ls
from main_program.Library.role import customer as CTM
from main_program.Library.role import clerk as CLK
from main_program.Library.role import manager as MNG
from main_program.Library.role import technician as TNC
#testinggggggggggggggggggggggggggg
if __name__ == '__main__':
    ddf.init_all_dictionary()
    while True:
        ls.role(
            customer_data= "customer.csv",
            clerk_data= "clerk.csv",
            manager_data= "manager.csv",
            technician_data= "technician.csv",
            customer_function= CTM.customer,
            clerk_function= CLK.clerk,
            manager_function= MNG.manager,
            technician_function= TNC.technician
        )

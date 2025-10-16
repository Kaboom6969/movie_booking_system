#This One is to make sure it can open in VSC (no need to manual set the source root)
#Yup this one is fully made by AI (this one only)
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

#The main Progress
from main_program.Library.movie_booking_framework import framework_utils as fu
from main_program.Library.cache_framework import data_dictionary_framework as ddf
from main_program.Library.data_communication_framework import cache_csv_sync_framework as ccsf
from main_program.Library.movie_booking_framework import cinema_services as cnsv, cinema_services
from main_program.Library.system_login_framework import login_system as ls
from main_program.Library.role import customer as CTM
from main_program.Library.role import clerk as CLK
from main_program.Library.role import manager as MNG
from main_program.Library.role import technician as TNC

CUSTOMER_CSV = fu.get_path("customer.csv")
CLERK_CSV = fu.get_path("clerk.csv")
MANAGER_CSV = fu.get_path("manager.csv")
TECHNICIAN_CSV = fu.get_path("technician.csv")
if __name__ == '__main__':
    ddf.init_all_dictionary()
    cnsv.sync_all()
    ls.role(
        customer_data= CUSTOMER_CSV,
        clerk_data= CLERK_CSV,
        manager_data= MANAGER_CSV,
        technician_data= TECHNICIAN_CSV,
        customer_function= CTM.customer,
        clerk_function= CLK.clerk,
        manager_function= MNG.manager,
        technician_function= TNC.technician
    )


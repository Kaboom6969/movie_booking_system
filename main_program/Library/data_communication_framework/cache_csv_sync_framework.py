from main_program.Library.cache_framework.data_dictionary_framework import *


def seats_cache_write_to_csv (seats_csv : str,seats_dictionary_cache : dict,mt_code_dictionary_cache : dict) -> None:
    seats_csv_path = mlf.get_path(seats_csv)
    seats_csv_temp_path = seats_csv_path + ".temp"
    header_text = seats_dictionary_cache.get("header")
    if seats_csv != seats_dictionary_cache.get("base file name"):
        raise ValueError(f"The file name:{seats_csv} is not same with base file name:{seats_dictionary_cache.get('base file name')}!")
    with open(seats_csv_temp_path,"w") as s_csv_w:
        s_csv_w.write(msf.list_to_str_line(header_text))
        for data_seats_code,seats_data in seats_dictionary_cache.items():
            if data_seats_code in ["header","base file name"]: continue
            longest_length : int = len(msf.find_longest_list(seats_data))
            template_code = mt_code_dictionary_cache.get(data_seats_code) #if didn't find key,it will show None
            if template_code is None: raise ValueError("template_code not found,the dictionary is not sync!")
            s_csv_w.write(f"CODE,{data_seats_code},{template_code}{"," * (longest_length - 2)}\n")
            s_csv_w.write(msf.list_to_str_line(msf.header_create(header_text="START",
                                                                 movie_seats_length= longest_length + 1, append_thing="-2")))
            for row in seats_data:
                s_csv_w.write("DATA," + msf.list_to_str_line(row)) # this is alr got '\n'
            s_csv_w.write(msf.list_to_str_line(msf.header_create(header_text="END",
                                                                 movie_seats_length= longest_length + 1, append_thing="-2")))
    msf.overwrite_file(overwrited_file_csv= seats_csv,original_file_csv= seats_csv + ".temp")

def list_cache_write_to_csv (list_csv : str,list_dictionary_cache : dict) -> None:
    list_csv_path = mlf.get_path(list_csv)
    list_csv_temp_path = list_csv_path + ".temp"
    code_location = list_dictionary_cache.get("code_location")
    header = list_dictionary_cache.get("header")
    if list_csv != list_dictionary_cache["base file name"]:
        raise ValueError(f"The file name:{list_csv} is not same with base file name:{list_dictionary_cache.get('base file name')}!")
    with open(list_csv_temp_path,"w") as l_csv_w:
        l_csv_w.write(mlf.list_to_str_line(header))
        for key,value in list_dictionary_cache.items():
            if key in ["header","code_location","base file name"]: continue
            value_copy = value.copy()
            value_copy.insert(code_location,key)
            l_csv_w.write(msf.list_to_str_line(value_copy))
    mlf.overwrite_file(overwrited_file_csv= list_csv,original_file_csv= list_csv + ".temp")









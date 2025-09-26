import os
import warnings

TARGET_DIRECTORY = "Data"
# turn the string with ',' to list
# "hello,test,data,data" -> ["hello","test","data","data]
def str_line_to_list(line: str) -> list:
    #strip the data (remove '\n' or ' ') and split it with ','
    return line.strip().split(',')

# turn the list to string
# ["hello","test","data","data] -> "hello,test,data,data"
def list_to_str_line(data_list: list,blank_need:bool=True) -> str:
    #join ',' in the gap of list,and put '\n',because it usually is convert to a row of file
    return ','.join(map(str,data_list)) +('\n' if blank_need else '')


#overwrite file (ususally is use for temp file overwrite to original file)
def overwrite_file(overwrited_file_csv: str, original_file_csv: str, delete_after_overwrite: bool = True) -> None:
    try:
        #get the overwrited file path (prevent FileNOtFoundError)
        overwrited_file_csv_path : str = get_path(overwrited_file_csv)
        #get the file that is overwriting path (prevent FileNOtFoundError)
        original_file_csv_path : str = get_path(original_file_csv)
        #open the file that is overwriting with read mode and open the overwrited file with write mode)
        #step:
        #1) read data from the file that is overwriting
        #2) write the data to the overwritted file
        with open(original_file_csv_path, 'r', newline='') as ori_file_r, open(overwrited_file_csv_path, 'w',
                                                                               newline='') as overwrited_file_w:
            #write the data to the overwritted file
            for line in ori_file_r:
                overwrited_file_w.write(line)
    #if file not found (your type your file name wrong)
    except FileNotFoundError:
        #show error
        raise FileNotFoundError(
            f"OVERWRITE FILE FAILED! NO FILE FOUND! OVERWRITED FILE:{overwrited_file_csv}\nORIGINAL FILE:{original_file_csv}")
    # don't care any situation,the action in below must be done
    finally:
        #if you want to delete the file after overwriting (use for temp file)
        if delete_after_overwrite:
            try:
                #check the file for overwriting got .temp or not
                if original_file_csv.endswith(".temp"):
                    #if got,shows that it is a temp file, can delete
                    os.remove(original_file_csv_path)
                else:
                    #if don't got,warn the user and don't delete the file
                    warnings.warn("The original File is not .temp File!\nYou should not delete it!")
            #if cannot found the file,don't care
            except FileNotFoundError:
                pass

#this is the function for founding the folder or file root
def _find_project_root(target_directory : str) -> str:
    # shows the root now (the folder that your program run)
    current_directory = os.path.dirname(os.path.abspath(__file__))
    while True:
        #if the target folder or file is in the current folder
        if target_directory in os.listdir(current_directory):
            #join the folder and target folder or file and return
            #example if C:/test/nihao got "target" file or folder
            #it will return C:/test/nihao/target
            return os.path.join(current_directory, target_directory)
        #if don't have,got to upper folder
        #Example C:/test/nihao -> C:/test
        parent_directory = os.path.dirname(current_directory)
        #if cannot go upper
        #Example C: -> C:
        if parent_directory == current_directory:
            #cannot find the file
            raise FileNotFoundError(f"Cannot Find File!")
        current_directory = parent_directory

#this is the function to get the path of file
#Example get_path("test.txt")
#it will return C:/nihao/test/omg/test.txt
def get_path(file) -> str:
    #detect the file parameter is path or not
    if os.path.isabs(file):
        #if it is the path,warn user and return the original file
        warnings.warn("Path Is Using in get_path Function! (Should be file)")
        return file
    #the data root is "DATA"
    base_directory = _find_project_root(target_directory= TARGET_DIRECTORY)
    #and just join the DATA root and file parameter
    movie_code_csv_path = os.path.join(base_directory, file)
    return movie_code_csv_path

#turn one dimension list to two dimension list
def one_dimension_list_to_two_dimension_list (any_dimension_list : list) -> list:
    new_list : list = []
    try:
        #if the list is one dimension list
        if not isinstance(any_dimension_list[0], list):
            #turn it into two dimension list
            new_list = [any_dimension_list]
        else:
            #don't convert it (it is two dimension list)
            new_list = any_dimension_list
    except IndexError as e:
        #if the list is empty list,it will got error,just skip it
        if "range" in str(e):
            pass
        #if not,show the error
        else:
            raise IndexError (f"List Convert Error! Error:{e}")
    return new_list

#yup this function just only for device column count
#if i have time,i will turn this function to universal function (done in 25/09/2025)
def keyword_count_for_list (any_dimension_list : list,keyword : str) -> int:
    two_dimension_list = one_dimension_list_to_two_dimension_list(any_dimension_list)
    count : int = 0
    for row in two_dimension_list:
        for element in row:
            #if "status" keyword is in item,it shows that the item is device column
            if keyword in element:
                count += 1
                continue
    return count

# ['hello','hellokeyword','hi_keyword']
# to
# 【‘hello','hello','hi_']
def keyword_erase_for_list (any_dimension_list : list,keyword : str) -> list:
    two_dimension_list = one_dimension_list_to_two_dimension_list(any_dimension_list)
    list_erased : list = []
    for row in two_dimension_list:
        one_dimension_list : list = []
        for element in row:
            if keyword in element:
                element = element.replace(keyword, "")
            one_dimension_list.append(element)
        list_erased.append(one_dimension_list)
    if len(list_erased) == 1: return list_erased[0]
    return list_erased


# ['hello','hellokeyword','hi_keyword']
# to
#['hellokeyword','hi_keyword']
def keyword_only_for_list (any_dimension_list : list,keyword : str) -> list:
    two_dimension_list = one_dimension_list_to_two_dimension_list(any_dimension_list)
    list_keyword_only : list = []
    for row in two_dimension_list:
        one_dimension_list : list = []
        for element in row:
            if keyword not in element: continue
            one_dimension_list.append(element)
        list_keyword_only.append(one_dimension_list)
    if len(list_keyword_only) == 1: return list_keyword_only[0]
    return list_keyword_only

def keyword_find_for_list (one_dimension_list : list,keyword : str) -> int:
    for index,element in enumerate(one_dimension_list):
        if keyword in element:
            return index
    return -1


#yup,just convert the data to list
#for example
#the_list = data_convert_to_list ("x","ok","zzzz")
#the_list = ["x","ok","zzzz"]
def data_convert_to_list (*args):
    target_list : list = []
    #unpack the args and use for loop to append the inside item of args
    for item in args:
        target_list.append(item)
    #return the list
    return target_list

if __name__ == "__main__":
    list_test : list = ["idk_status","header","nihao_status","wtf_status","end"]
    print(keyword_erase_for_list(list_test,"status"))


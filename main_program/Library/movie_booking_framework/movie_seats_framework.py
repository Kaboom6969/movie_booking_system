import csv #From python standard library
import warnings #From python standard library
import os #From python standard library
import re #From python standard library
from movie_list_framework import read_movie_list_csv

TARGET_DIRECTORY = "Data"

#Read seat data for a specific movie from a CSV file into a 2D list
def read_movie_seats_csv(movie_seats_csv: str, movie_seats: list, movie_code: str,skip_valid_check : bool = False) -> None:
    list_found = False
    start_status = False
    try:
        if not skip_valid_check:
            _movie_seats_csv_valid_check(movie_seats_csv=movie_seats_csv)
    except ValueError as e:
        raise e
    try:
        movie_seats_csv_path = _get_path(movie_seats_csv)
        with open(movie_seats_csv_path, 'r') as ms_csv_r:
            next(ms_csv_r)
            for line in ms_csv_r:
                if not line.strip(): continue
                row = parse_csv_line(line)

                if row and row[0] == "CODE" and row[1] == movie_code:
                    list_found = True
                    continue

                if row[0] == "START" and list_found:
                    start_status = True
                    continue
                if row[0] == "END" and list_found:
                    break
                if start_status and list_found:
                    movie_seats.append(row[1:])
            if not list_found:
                raise IndexError("Your Movie Seat List is Empty! Cannot Found the movie code!")

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found!\nYour file name is {movie_seats_csv}.\nPlease Check The Name!")
    except IndexError as e:
        raise e


#Update seat data for a specific movie_code in the CSV file
def update_movie_seats_csv (movie_seats_csv : str, movie_seats: list, movie_code : str,skip_valid_check : bool = False) -> None:
    try:
        if not skip_valid_check:
            _movie_seats_csv_valid_check(movie_seats_csv= movie_seats_csv)
            _movie_seats_valid_check(movie_seats_list=movie_seats)
    except ValueError as e:
        raise ValueError(f"Update Movie Seats Failed! Movie Seat List ERROR!\n {e}")
    try:
        movie_seats_csv_path = _get_path(movie_seats_csv)
        movie_seats_csv_temp_path = os.path.dirname(movie_seats_csv_path)
        with (open(movie_seats_csv_path, 'r', newline='') as ms_csv_r,
              open(os.path.join(movie_seats_csv_temp_path, f"{movie_seats_csv}.temp"), "w", newline='') as ms_csv_w):
                movie_seats_writer = csv.writer(ms_csv_w)        #Create writer for temporary file
                movie_seats_reader = csv.reader(ms_csv_r)        #Create reader for CSV file
                list_found_all_times = False                    #Track if movie_code was ever found
                list_found = False                              #Track if currently processing target movie_code
                start_status = False                            #Track if in START-END section
                skip_status = False                             #skip status for skipping old data
                for row in movie_seats_reader:

                    if row and row[0] == "CODE" and row[1] == movie_code:                                #Found movie_code
                        list_found = True
                        list_found_all_times = True
                        movie_seats_writer.writerow(row)
                        continue

                    if list_found and row and row[0] == "START":
                        start_status = True
                        start_header : list = _header_create(header_text="START",movie_seats_length= len(movie_seats[0]) + 1, append_thing= "-2")
                        movie_seats_writer.writerow(start_header)

                    if start_status:

                        for i in range(0,len(movie_seats)):
                            movie_seats_writer.writerow(["",*movie_seats[i][0:]])     #Write row with empty first column

                        end_header : list = _header_create(header_text="END",movie_seats_length= len(movie_seats[0]) + 1,append_thing= "-2")
                        movie_seats_writer.writerow(end_header)
                        start_status = False
                        skip_status = True
                        continue

                    if list_found and row and row[0] == "END":     #Found END marker
                        skip_status = False
                        list_found = False
                        continue
                    elif skip_status:
                        continue

                    movie_seats_writer.writerow(row)            #Copy other rows to temporary file
                if list_found_all_times == False:               #Movie_code not found
                    raise ValueError("Movie Code Does Not Exist! You Should Use add_movie_seats_csv function")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Update Movie Seats Failed! \nCannot Find the File!"
                                f"\nFile name: {movie_seats_csv}")
    except ValueError as e:
        raise ValueError(f"Update Movie Seats Failed!\n{e}")

    _overwrite_file(overwrited_file_csv= movie_seats_csv, original_file_csv=f"{movie_seats_csv}.temp")   #Overwrite original file

#Add a new seat table for a movie_code to the CSV file
def add_movie_seats_csv (movie_seats_csv : str, movie_seats : list, movie_code : str, template_code : str,skip_valid_check : bool = False) -> None:
    try:
        if not skip_valid_check:
            _movie_seats_valid_check(movie_seats_list=movie_seats)
            _movie_seats_csv_valid_check(movie_seats_csv=movie_seats_csv)
    except ValueError as e:
        raise ValueError (f"Add Movie Seats Failed! Movie Seat List ERROR! {e}")
    movie_seats_csv_path = _get_path(movie_seats_csv)
    movie_seats_csv_temp_path = os.path.dirname(movie_seats_csv_path)
    try:
        with (open(movie_seats_csv_path, 'r', newline='') as ms_csv_r,
              open(os.path.join(movie_seats_csv_temp_path, f"{movie_seats_csv}.temp"), "w", newline='') as ms_csv_w):
            movie_seat_reader = csv.reader(ms_csv_r)    #Create reader for CSV file
            movie_seat_writer = csv.writer(ms_csv_w)    #Create writer for temporary file
            for row in movie_seat_reader:       #Copy existing content
                    movie_seat_writer.writerow(row)
                    if row and row[0] == "CODE" and row[1] == movie_code:    #Check if movie_code already exists
                        raise ValueError ("Movie Code Already Exists! You Should Use update_movie_seats_csv function!")
        #Create headers for CODE, START, and END rows
            longest_row_length = len(find_longest_list(movie_seats))
            code_header : list = _header_create(header_text = "CODE", movie_seats_length= longest_row_length + 1, append_thing="")
            code_header[1] = movie_code
            code_header[2] = template_code
            start_header : list = _header_create(header_text = "START", movie_seats_length = longest_row_length + 1, append_thing="-2")
            movie_seat_writer.writerow(code_header)       #Write movie_code row
            movie_seat_writer.writerow(start_header)            #Write START row
            for row in movie_seats:                              #Write seat data
                movie_seat_writer.writerow(["",*row])           #Add empty first column [""...
            end_header : list = _header_create(header_text = "END", movie_seats_length = longest_row_length + 1, append_thing="-2")
            movie_seat_writer.writerow(end_header)              #Write END row

        _overwrite_file(overwrited_file_csv= movie_seats_csv, original_file_csv=f"{movie_seats_csv}.temp")     #Overwrite original file
    except ValueError as e:
        raise ValueError(f"Add Movie Seats Failed!\n{e}")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Update Movie Seats Failed!\nCannot Find the File!\n"
                                    f"File name: {movie_seats_csv}\nFile path: {movie_seats_csv_path})")
    except Exception as e:
        raise Exception(f"Add Movie Seats Failed\nUnknown Error!\n{e}")


def delete_movie_seats_csv (movie_seats_csv : str, movie_code : str,skip_valid_check : bool = False) -> None:
    try:
        if not skip_valid_check:
            _movie_seats_csv_valid_check(movie_seats_csv)
    except ValueError as e:
        raise ValueError(f"Delete Movie Seats Failed!\n{e}")
    try:
        movie_seats_csv_path = _get_path(movie_seats_csv)
        movie_seats_csv_TEMP_path = os.path.dirname(movie_seats_csv_path)
        with (open(movie_seats_csv_path, 'r', newline ='') as ms_csv_r ,
              open(os.path.join(movie_seats_csv_TEMP_path,f"{movie_seats_csv}.temp"), "w", newline='') as ms_csv_w):
            movie_seat_reader = csv.reader(ms_csv_r)
            movie_seat_writer = csv.writer(ms_csv_w)
            list_found_all_times = False
            list_found = False
            delete_count = 0
            for row in movie_seat_reader:
                if row and row[0] == "CODE" and row[1] == movie_code:
                    list_found = True
                    list_found_all_times = True
                    continue
                elif list_found and row and row[0] == "END":
                    list_found = False
                    delete_count += 1
                    continue
                elif list_found: continue
                movie_seat_writer.writerow(row)
            if list_found_all_times == False:
                raise KeyError(f"Cannot Find The Movie Code! Movie Code : {movie_code}")
            if delete_count > 1:
                warnings.warn(f"delete_movie_seats_csv function delete {delete_count} times.")
        _overwrite_file(overwrited_file_csv=movie_seats_csv, original_file_csv=f"{movie_seats_csv}.temp")

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Update Movie Seats Failed!\nCannot Find the File!\nFile name:{movie_seats_csv}")
    except KeyError as e:
        raise KeyError(f"Delete Movie Seats Failed!\n{e}")

def generate_movie_seats (x_axis : int, y_axis : int, fill_number : int) -> list:
    if x_axis > 11:
        raise ValueError("x_axis must be less than 11")
    seat_list_temp : list = []
    for i in range (0,y_axis):
        seat_list_temp.append([])
        for j in range (0,x_axis):
            seat_list_temp[i].append(str(fill_number))
    return seat_list_temp

def _movie_seats_valid_check (movie_seats_list : list) -> None:
    try:
        if not movie_seats_list:
            raise ValueError("Movie Seat List is Empty!")
        if not all(isinstance(row, list) for row in movie_seats_list):
            raise ValueError("Movie Seat List is not 2D List!")
        valid_movie_state : list = ["0","1","-1"]
        for i, row in enumerate(movie_seats_list):    # Iterate through rows
            if not row:                              # Check for empty row
                raise ValueError(f"Row {i + 1} is empty")
            for j, state in enumerate(row):  # Iterate through columns
                if state not in valid_movie_state:  # Check for invalid state
                    raise ValueError(f"Invalid state '{state}' found at row {i + 1}, column {j + 1}."
                                     f" Valid states are {valid_movie_state}")
    except ValueError as e:
        raise ValueError(f"Error:{e}")


def _movie_seats_csv_valid_check (movie_seats_csv : str) -> None:
    movie_seats_csv_path = _get_path(movie_seats_csv)
    try:
        with open(movie_seats_csv_path,'r',newline ='') as ms_csv_r:
            movie_seats_reader = csv.reader(ms_csv_r)
            CODE_status = False
            START_status = False
            END_status = False
            line_count = 0
            for row in movie_seats_reader:
                line_count += 1
                if not row: raise ValueError(f"GOT BLANK IN THE FILE!\nFile name:{movie_seats_csv}\nFile path:{movie_seats_csv_path}\nLine:{line_count}")
                if row[0] == "CODE":
                    CODE_status = True
                    if not re.match(pattern = r"\d{3}",string = row[1]):
                        raise ValueError(f"MOVIE CODE IS INVALID\nFile name:{movie_seats_csv}\nFile path:{movie_seats_csv_path}\n"
                                     f"Line:{line_count}\nThis Row: {row}")
                    if "TEMPLATE" not in row[2]:
                        raise ValueError(f"TEMPLATE CODE IS INVALID!\nFile name:{movie_seats_csv}\nFile path:{movie_seats_csv_path}\n"
                                     f"Line:{line_count}\nThis Row: {row}")
                if row[0] == "START": START_status = True
                if row[0] == "END": END_status = True

                if START_status and not CODE_status:
                    raise ValueError(f"MOVIE_CODE DIDN'T FOUND!\nFile name:{movie_seats_csv}\nFile path:{movie_seats_csv_path}\n"
                                     f"Line:{line_count}\nThis Row: {row[0]}\nLAST Row:{row_head_temp}")
                if END_status and not START_status:
                    raise ValueError(f"START HEADER DIDN'T FOUND!\nFile name:{movie_seats_csv}\nFile path:{movie_seats_csv_path}\nLine:{line_count}")
                if CODE_status and START_status and END_status:
                    CODE_status = False
                    START_status = False
                    END_status = False
                row_head_temp = row[0]
            if START_status and CODE_status: raise ValueError (f"END HEADER LOST!\nFile name:{movie_seats_csv}"
                                                   f"\nFile path:{movie_seats_csv_path}\nLine:{line_count}")
            if CODE_status: raise ValueError(f"START HEADER AND END HEADER LOST!\nFile name:{movie_seats_csv}"
                                                   f"\nFile path:{movie_seats_csv_path}\nLine:{line_count}")
            if START_status or END_status or CODE_status:
                raise ValueError(f"FORMAT ERROR! COULD NOT PINPOINT THE EXACT ISSUE. PLEASE REVIEW YOUR FILE!\nFile name:{movie_seats_csv}\nFile path:{movie_seats_csv_path}")
    except ValueError as e:
        raise e
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File '{movie_seats_csv}' not found!File path:{movie_seats_csv_path}")

def movie_seats_csv_whole_init (movie_seats_csv : str,template_seats_csv : str) -> None:
    try:
        _movie_seats_csv_valid_check(movie_seats_csv)
    except Exception as e:
        raise Exception(f"INIT FAILED! ERROR:{e}")
    movie_seats_csv_path = _get_path(movie_seats_csv)
    movie_code_array : list = []
    template_code_array : list = []
    with open(movie_seats_csv_path,'r',newline ='') as ms_csv_r:
        next(ms_csv_r)
        for line in ms_csv_r:
            if not line.strip(): continue
            row = parse_csv_line(line)
            if row[0] == "CODE":
                movie_code_array.append(row[1])
                template_code_array.append(row[2])
    if len(movie_code_array) != len(template_code_array):
        raise ValueError("The number of movie code and template code should be same! Please check the file!")
    for movie_code,template_code in zip(movie_code_array,template_code_array):
        movie_seats_init(movie_seats_csv= movie_seats_csv,template_seats_csv= template_seats_csv,movie_code= movie_code,template_code= template_code)



def movie_seats_init(movie_seats_csv : str, template_seats_csv : str, movie_code : str,template_code : str) -> None:
    template_seats : list = []
    read_movie_seats_csv(movie_seats_csv= template_seats_csv,movie_seats= template_seats,movie_code= template_code,skip_valid_check= True)
    update_movie_seats_csv(movie_seats_csv= movie_seats_csv,movie_seats= template_seats,movie_code= movie_code)

def get_movie_code_x_y_value_list (booking_data_array : list,movie_code_location : int, x_seats_location : int, y_seats_location : int) -> list:
    if any(isinstance(element, (list,tuple)) for element in booking_data_array):
        raise TypeError (f"booking_data_array: {booking_data_array} must be a array (no 2d list allowed)")
    mvcode_x_y_list : list = []
    mvcode_x_y_list.append(booking_data_array[movie_code_location])
    mvcode_x_y_list.append(int(booking_data_array[x_seats_location]))
    mvcode_x_y_list.append(int(booking_data_array[y_seats_location]))
    return mvcode_x_y_list
##############################################################################################################################################################
def get_capacity(movie_seats : list) -> int:
    _movie_seats_valid_check(movie_seats_list= movie_seats)
    capacity = 0
    for row in movie_seats:
        for element in row:
            if element == "0" : capacity += 1
    return capacity

def movie_seats_pointer_valid_check(movie_seats : list,x_pointer : int,y_pointer : int) -> bool:
    try:
        if not movie_seats: raise ValueError(f"{movie_seats} is empty!")
        point_value : str = movie_seats[len(movie_seats) - y_pointer][x_pointer - 1]
        return True
    except IndexError:
        return False
    except ValueError as e:
        raise e

def movie_seats_specify_value(movie_seats : list,x_axis : int,y_axis : int) -> str:
    if not movie_seats_pointer_valid_check(movie_seats= movie_seats,x_pointer= x_axis,y_pointer= y_axis):
        raise IndexError(f"x_axis:{x_axis} or y_axis:{y_axis} is out of range of {movie_seats}!")
    return movie_seats[len(movie_seats) - y_axis][x_axis - 1]

############################################################################################################################################################

def parse_csv_line(line: str) -> list:
    return line.strip().split(',')
def format_csv_line(data_list: list) -> str:
    return ','.join(map(str, data_list)) + '\n'



############################################################################################################################################################
#Functions for low-level file operations
#Overwrite target file with contents of a temporary file
def _overwrite_file (overwrited_file_csv : str, original_file_csv : str, delete_after_overwrite : bool = True) -> None:
        try:
            overwrited_file_csv_path = _get_path(overwrited_file_csv)
            original_file_csv_path = _get_path(original_file_csv)
            with open(original_file_csv_path, 'r', newline='') as ori_file_r, open(overwrited_file_csv_path, 'w', newline='') as overwrited_file_w:
                ori_file_reader = csv.reader(ori_file_r)                #Create reader for source file
                overwrited_file_writer = csv.writer(overwrited_file_w)  #Create writer for target file
                for row in ori_file_reader:                             #Copy each row
                    overwrited_file_writer.writerow(row)
        except FileNotFoundError:
            raise FileNotFoundError(f"OVERWRITE FILE FAILED! NO FILE FOUND! OVERWRITED FILE:{overwrited_file_csv}\nORIGINAL FILE:{original_file_csv}")
        finally:
            if delete_after_overwrite:
                try:
                    if original_file_csv.endswith(".temp"):
                        os.remove(original_file_csv_path)
                    else:
                        warnings.warn("The original File is not .temp File!\nYou should not delete it!")
                except FileNotFoundError:
                    pass



#Generate a header row for CSV (e.g., movie_code, START, END)
def _header_create (header_text : str , movie_seats_length : int , append_thing :str) -> list:
    header : list = []
    header.append(header_text)                  #Add header text
    for i in range(0,movie_seats_length - 1):   #Fill remaining columns
        header.append(append_thing)
    return header
###############################################################################################################################################################
#Fill all seats in the seat list with a specified value
def fill_movie_seats_list (movie_seat_list : list, fill_number : int) -> None:
    try:
        _movie_seats_valid_check(movie_seats_list=movie_seat_list)
    except ValueError as e:
        raise ValueError (f"Fill Movie Seats Failed! Movie Seat List ERROR! {e}")
    for i in range (0,len(movie_seat_list)):
        for j in range (0,len(movie_seat_list[0])):
            movie_seat_list[i][j] = str(fill_number)

#Modify the state of a specific seat
def modify_movie_seats_list(movie_seat_list: list, x_axis: int, y_axis: int, target_number: int) -> None:
    try:
        _movie_seats_valid_check(movie_seats_list=movie_seat_list)
    except ValueError as e:
        raise ValueError (f"Modify Movie Seats Failed! Movie Seat List ERROR! {e}")
    if not movie_seat_list:                                 #Check if list is empty
        raise IndexError("Your Movie Seat List is Empty!")
    if x_axis < 1 or x_axis > len(movie_seat_list[0]):      #Validate x_axis
        raise IndexError(f"x_axis should be between 1 and {len(movie_seat_list[0])}\nYour x_axis is {x_axis}")
    if y_axis < 1 or y_axis > len(movie_seat_list):         #Validate y_axis
        raise IndexError(f"y_axis should be between 1 and {len(movie_seat_list)}\nYour y_axis is {y_axis}")
    movie_seat_list[len(movie_seat_list) - y_axis][x_axis - 1] = str(target_number)     #Modify specified seat

##########################################################################################################################
#Functions for file path resolution
def _find_project_root(target_directory : str) -> str:
    current_directory = os.path.dirname(os.path.abspath(__file__))
    while True:
        if target_directory in os.listdir(current_directory):
            return os.path.join(current_directory, target_directory)
        parent_directory = os.path.dirname(current_directory)
        if parent_directory == current_directory:
            raise FileNotFoundError(f"Cannot Find File!")
        current_directory = parent_directory

def _get_path(file) -> str:
    if os.path.isabs(file):
        warnings.warn("Path Is Using in get_path Function! (Should be file)")
        return file
    base_directory = _find_project_root(target_directory= TARGET_DIRECTORY)
    movie_code_csv_path = os.path.join(base_directory, file)
    return movie_code_csv_path
###########################################################################################################################
#Print seat list as text
def print_movie_seat (movie_seats : list) -> None:
    try:
        _movie_seats_valid_check(movie_seats_list=movie_seats)
    except ValueError as e:
        raise ValueError (f"Print Movie Seats Failed! Movie Seat List ERROR! {e}")
    for main_list in movie_seats:
        print()
        for second_list in main_list:
            print(second_list,end= " ")

#Print seat list as emojis
def print_movie_seat_as_emojis (movie_seats : list,x_pointer : int = -1,y_pointer : int = -1) -> None:
    try:
        _movie_seats_valid_check(movie_seats_list=movie_seats)
    except ValueError as e:
        raise ValueError (f"Print Movie Seats Failed (Emoji)! Movie Seat List ERROR! {e}")
    movie_seats_temp = [row[:] for row in movie_seats]
    if y_pointer > 0:
        movie_seats_temp = _y_location_add(movie_seats= movie_seats_temp,y_pointer= y_pointer)
    if x_pointer > 0:
        movie_seats_temp = _x_location_add(movie_seats= movie_seats_temp,x_pointer= x_pointer)
    for index,main_list in enumerate(movie_seats_temp):
        for second_list in main_list:
            if second_list == "0":
                print("🈳",end=" ")
            elif second_list == "1":
                print("👨",end=" ")
            elif second_list == "-1":
                print("❌",end=" ")
            elif second_list == "2":
                print("　",end="　")
            elif second_list == "3":
                print("⬆️",end=" ")
            elif second_list == "4":
                print("⬅️",end=" ")
            elif second_list == "5":
                print("🎯",end=" ")
        print()

def _x_location_add(movie_seats : list,x_pointer : int) -> list:
    max_width = x_range_calculate(movie_seats)[1]
    if x_pointer > max_width:
        raise IndexError(f"{x_pointer} is out of range of {movie_seats}!")
    movie_seats_with_x_location : list = movie_seats
    x_location_head : list = []
    for index in range(max_width):
        if index == x_pointer - 1:
            x_location_head.append("3")
        else:
            x_location_head.append("2")
    movie_seats_with_x_location.append(x_location_head)
    return movie_seats_with_x_location

def _y_location_add(movie_seats : list,y_pointer : int) -> list:
    if y_pointer > y_range_calculate(movie_seats)[1]:
        raise IndexError(f"{y_pointer} is out of range of {movie_seats}!")
    movie_seats_with_y_location : list = []
    for index,row in enumerate(movie_seats):
        row_as_list = list(row)
        if (len(movie_seats) - index) == y_pointer:
            row_as_list.extend(["4"])
            movie_seats_with_y_location.append(row_as_list)
        else:
            row_as_list.extend(["2"])
            movie_seats_with_y_location.append(row_as_list)
    return movie_seats_with_y_location

######################################################################################################################

def x_range_calculate(movie_seats : list) -> list:
    x_max = len(find_longest_list(nested_list= movie_seats))
    x_min = 1
    return [x_min,x_max]

def y_range_calculate(movie_seats : list) -> list:
    if not movie_seats: raise ValueError(f"{movie_seats} is empty!")
    y_max = len(movie_seats)
    y_min = 1
    return [y_min,y_max]

def find_longest_list(nested_list : list) -> list:
    if not nested_list: raise ValueError(f"{nested_list} is empty!")
    longest_list : list = []
    largest_element_count : int = 0
    for row in nested_list:
        element_count : int = len(row)
        if element_count > largest_element_count:
            largest_element_count = element_count
            longest_list = row
    return longest_list
############################################################################################################################
#higher level fucntion
def link_seats (movie_seats_csv : str, booking_data_csv : str,template_seats_csv : str,book_movie_code_location : int = 2, book_x_seats_location : int = 5, book_y_seats_location : int = 6) -> None:

    booking_data_list : list = []
    movie_seats_csv_whole_init(movie_seats_csv= movie_seats_csv,template_seats_csv= template_seats_csv)
    read_movie_list_csv(movie_list_csv= booking_data_csv,movie_list=booking_data_list)
    for row in booking_data_list:
        #[movie_code,x_axis,y_axis]
        mvcode_x_y_list : list = get_movie_code_x_y_value_list(booking_data_array= row,
                                                               movie_code_location= book_movie_code_location,
                                                               x_seats_location= book_x_seats_location,
                                                               y_seats_location= book_y_seats_location)
        movie_seats : list = []
        read_movie_seats_csv(movie_seats_csv= movie_seats_csv,movie_seats= movie_seats,movie_code= mvcode_x_y_list[0])
        if movie_seats_specify_value(movie_seats=movie_seats,x_axis=mvcode_x_y_list[1],y_axis=mvcode_x_y_list[2]) ==  "-1":
            raise ValueError(f"This movie seat is unvailable(-1)!You should check your booking data file!\n"
                             f"movie_seats: {movie_seats}\nx_axis: {mvcode_x_y_list[1]}\ny_axis: {mvcode_x_y_list[2]}")
        modify_movie_seats_list(movie_seat_list=movie_seats,x_axis=mvcode_x_y_list[1],y_axis=mvcode_x_y_list[2],target_number= 1)
        update_movie_seats_csv(movie_seats_csv= movie_seats_csv,movie_seats=movie_seats,movie_code= mvcode_x_y_list[0])

############################################################################################################################
    #作为library时不会被启用，仅有亲自运行此文件才会运行（用来测试用）
if __name__ == '__main__':
    movie_seats : list = []
    read_movie_seats_csv(movie_seats_csv= "movie_seat.csv",movie_seats= movie_seats,movie_code="001")
    fill_movie_seats_list(movie_seat_list= movie_seats,fill_number= 0)
    update_movie_seats_csv(movie_seats_csv="movie_seat.csv",movie_seats= movie_seats,movie_code="001")


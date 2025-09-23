from .framework_utils import *
from .valid_checker import movie_seats_valid_check,movie_seats_csv_valid_check,movie_seats_pointer_valid_check




#Read seat data for a specific movie from a CSV file into a 2D list
def read_movie_seats_csv(movie_seats_csv: str, movie_seats: list, movie_code: str,skip_valid_check : bool = False) -> None:
    list_found = False
    start_status = False
    try:
        if not skip_valid_check:
            movie_seats_csv_valid_check(movie_seats_csv=movie_seats_csv)
    except ValueError as e:
        raise e
    try:
        movie_seats_csv_path = get_path(movie_seats_csv)
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

def read_movie_seats_csv_raw_data(movie_seats_csv: str,skip_check : bool = False) -> list:
    raw_data : list = []
    if not skip_check:movie_seats_csv_valid_check(movie_seats_csv= movie_seats_csv)
    movie_seats_csv_path = get_path(movie_seats_csv)
    try:
        with open(movie_seats_csv_path, 'r') as ms_csv_r:
            for lines in ms_csv_r:
                row = parse_csv_line(lines)
                raw_data.append(row)
    except FileNotFoundError:
        raise FileNotFoundError(f"READ RAW DATA FAILED!\nFILE:{movie_seats_csv} IS NOT FOUND!")
    return raw_data



#Update seat data for a specific movie_code in the CSV file
def update_movie_seats_csv (movie_seats_csv : str,movie_seats: list, movie_code : str,skip_valid_check : bool = False) -> None:
    try:
        if not skip_valid_check:
            movie_seats_csv_valid_check(movie_seats_csv= movie_seats_csv)
            movie_seats_valid_check(movie_seats_list=movie_seats)
    except ValueError as e:
        raise ValueError(f"Update Movie Seats Failed! Movie Seat List ERROR!\n {e}")
    try:
        movie_seats_csv_path = get_path(movie_seats_csv)
        movie_seats_csv_temp_path = os.path.dirname(movie_seats_csv_path)
        with (open(movie_seats_csv_path, 'r', newline='') as ms_csv_r,
              open(os.path.join(movie_seats_csv_temp_path, f"{movie_seats_csv}.temp"), "w", newline='') as ms_csv_w):
            list_found_all_times = False  # Track if movie_code was ever found
            list_found = False  # Track if currently processing target movie_code
            start_status = False  # Track if in START-END section
            skip_status = False  # skip status for skipping old data
            for lines in ms_csv_r:
                row = parse_csv_line(lines)

                if row and row[0] == "CODE" and row[1] == movie_code:                                #Found movie_code
                    list_found = True
                    list_found_all_times = True
                    ms_csv_w.write(format_csv_line(row))
                    continue

                if list_found and row and row[0] == "START":
                    start_status = True
                    start_header : list = header_create(header_text="START", movie_seats_length=len(movie_seats[0]) + 1, append_thing="-2")
                    ms_csv_w.write(format_csv_line(start_header))

                if start_status:

                    for i in range(0,len(movie_seats)):
                        ms_csv_w.write(format_csv_line(["DATA",*movie_seats[i][0:]]))     #Write row with empty first column

                    end_header : list = header_create(header_text="END", movie_seats_length=len(movie_seats[0]) + 1, append_thing="-2")
                    ms_csv_w.write(format_csv_line(end_header))
                    start_status = False
                    skip_status = True
                    continue

                if list_found and row and row[0] == "END":     #Found END marker
                    skip_status = False
                    list_found = False
                    continue
                elif skip_status:
                    continue

                ms_csv_w.write(format_csv_line(row))            #Copy other rows to temporary file
            if list_found_all_times == False:               #Movie_code not found
                raise ValueError("Movie Code Does Not Exist! You Should Use add_movie_seats_csv function")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Update Movie Seats Failed! \nCannot Find the File!"
                                f"\nFile name: {movie_seats_csv}")
    except ValueError as e:
        raise ValueError(f"Update Movie Seats Failed!\n{e}")
    overwrite_file(overwrited_file_csv= movie_seats_csv, original_file_csv=f"{movie_seats_csv}.temp")   #Overwrite original file

#Add a new seat table for a movie_code to the CSV file
def add_movie_seats_csv (movie_seats_csv : str, movie_seats : list, movie_code : str, template_code : str,skip_valid_check : bool = False) -> None:
    try:
        if not skip_valid_check:
            movie_seats_valid_check(movie_seats_list=movie_seats)
            movie_seats_csv_valid_check(movie_seats_csv=movie_seats_csv)
    except ValueError as e:
        raise ValueError (f"Add Movie Seats Failed! Movie Seat List ERROR! {e}")
    movie_seats_csv_path = get_path(movie_seats_csv)
    movie_seats_csv_temp_path = os.path.dirname(movie_seats_csv_path)
    try:
        with (open(movie_seats_csv_path, 'r', newline='') as ms_csv_r,
              open(os.path.join(movie_seats_csv_temp_path, f"{movie_seats_csv}.temp"), "w", newline='') as ms_csv_w):
            for lines in ms_csv_r:
                row = parse_csv_line(lines)
                ms_csv_w.write(format_csv_line(row))
                if row and row[0] == "CODE" and row[1] == movie_code:    #Check if movie_code already exists
                    raise ValueError ("Movie Code Already Exists! You Should Use update_movie_seats_csv function!")
        #Create headers for CODE, START, and END rows
            longest_row_length = len(find_longest_list(movie_seats))
            code_header : list = header_create(header_text ="CODE", movie_seats_length=longest_row_length + 1, append_thing="")
            code_header[1] = movie_code
            code_header[2] = template_code
            start_header : list = header_create(header_text ="START", movie_seats_length =longest_row_length + 1, append_thing="-2")
            ms_csv_w.write(format_csv_line(code_header))       #Write movie_code row
            ms_csv_w.write(format_csv_line(start_header))           #Write START row
            for row in movie_seats:                              #Write seat data
                ms_csv_w.write(format_csv_line(["DATA",*row]))           #Add empty first column [""...
            end_header : list = header_create(header_text ="END", movie_seats_length =longest_row_length + 1, append_thing="-2")
            ms_csv_w.write(format_csv_line(end_header))              #Write END row

        overwrite_file(overwrited_file_csv= movie_seats_csv, original_file_csv=f"{movie_seats_csv}.temp")     #Overwrite original file
    except ValueError as e:
        raise ValueError(f"Add Movie Seats Failed!\n{e}")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Update Movie Seats Failed!\nCannot Find the File!\n"
                                    f"File name: {movie_seats_csv}\nFile path: {movie_seats_csv_path})")
    except Exception as e:
        raise Exception(f"Add Movie Seats Failed\nUnknown Error!\n{e}")


def seats_code_catcher (movie_seats_raw_data : list,movie_code_location : int = 1) -> list:
    movie_seats_code_list : list = []
    code_status = False
    for row in movie_seats_raw_data:
        if row and row[0] == "CODE":
            code_status = True
            movie_seats_code_list.append(row[movie_code_location])
    if not code_status:
        raise ValueError("Cannot find any movie code! 'CODE' is not found!")
    return movie_seats_code_list


def delete_movie_seats_csv (movie_seats_csv : str, movie_code : str,skip_valid_check : bool = False) -> None:
    try:
        if not skip_valid_check:
            movie_seats_csv_valid_check(movie_seats_csv)
    except ValueError as e:
        raise ValueError(f"Delete Movie Seats Failed!\n{e}")
    try:
        movie_seats_csv_path = get_path(movie_seats_csv)
        movie_seats_csv_TEMP_path = os.path.dirname(movie_seats_csv_path)
        with (open(movie_seats_csv_path, 'r', newline ='') as ms_csv_r ,
              open(os.path.join(movie_seats_csv_TEMP_path,f"{movie_seats_csv}.temp"), "w", newline='') as ms_csv_w):
            list_found_all_times = False
            list_found = False
            delete_count = 0
            for lines in ms_csv_r:
                row = parse_csv_line(lines)
                if row and row[0] == "CODE" and row[1] == movie_code:
                    list_found = True
                    list_found_all_times = True
                    continue
                elif list_found and row and row[0] == "END":
                    list_found = False
                    delete_count += 1
                    continue
                elif list_found: continue
                ms_csv_w.write(format_csv_line(row))
            if list_found_all_times == False:
                raise KeyError(f"Cannot Find The Movie Code! Movie Code : {movie_code}")
            if delete_count > 1:
                warnings.warn(f"delete_movie_seats_csv function delete {delete_count} times.")
        overwrite_file(overwrited_file_csv=movie_seats_csv, original_file_csv=f"{movie_seats_csv}.temp")

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







##############################################################################################################################################################
def get_capacity(movie_seats : list) -> int:
    movie_seats_valid_check(movie_seats_list= movie_seats)
    capacity = 0
    for row in movie_seats:
        for element in row:
            if element == "0" : capacity += 1
    return capacity



def movie_seats_specify_value(movie_seats : list,x_axis : int,y_axis : int) -> str:
    if not movie_seats_pointer_valid_check(movie_seats= movie_seats,x_pointer= x_axis,y_pointer= y_axis):
        raise IndexError(f"x_axis:{x_axis} or y_axis:{y_axis} is out of range of {movie_seats}!")
    return movie_seats[len(movie_seats) - y_axis][x_axis - 1]



def header_create (header_text : str, movie_seats_length : int, append_thing :str) -> list:
    header : list = []
    header.append(header_text)                  #Add header text
    for i in range(0,movie_seats_length - 1):   #Fill remaining columns
        header.append(append_thing)
    return header

#Fill all seats in the seat list with a specified value
def fill_movie_seats_list (movie_seat_list : list, fill_number : int) -> None:
    try:
        movie_seats_valid_check(movie_seats_list=movie_seat_list)
    except ValueError as e:
        raise ValueError (f"Fill Movie Seats Failed! Movie Seat List ERROR! {e}")
    for i in range (0,len(movie_seat_list)):
        for j in range (0,len(movie_seat_list[0])):
            movie_seat_list[i][j] = str(fill_number)

#Modify the state of a specific seat
def modify_movie_seats_list(movie_seat_list: list, x_axis: int, y_axis: int, target_number: int) -> None:
    try:
        movie_seats_valid_check(movie_seats_list=movie_seat_list)
    except ValueError as e:
        raise ValueError (f"Modify Movie Seats Failed! Movie Seat List ERROR! {e}")
    if not movie_seat_list:                                 #Check if list is empty
        raise IndexError("Your Movie Seat List is Empty!")
    if x_axis < 1 or x_axis > len(movie_seat_list[0]):      #Validate x_axis
        raise IndexError(f"x_axis should be between 1 and {len(movie_seat_list[0])}\nYour x_axis is {x_axis}")
    if y_axis < 1 or y_axis > len(movie_seat_list):         #Validate y_axis
        raise IndexError(f"y_axis should be between 1 and {len(movie_seat_list)}\nYour y_axis is {y_axis}")
    movie_seat_list[len(movie_seat_list) - y_axis][x_axis - 1] = str(target_number)     #Modify specified seat


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

    #作为library时不会被启用，仅有亲自运行此文件才会运行（用来测试用）
if __name__ == '__main__':
    movie_seats : list = []
    read_movie_seats_csv(movie_seats_csv= "movie_seat.csv",movie_seats= movie_seats,movie_code="001")
    fill_movie_seats_list(movie_seat_list= movie_seats,fill_number= 0)
    update_movie_seats_csv(movie_seats_csv="movie_seat.csv",movie_seats= movie_seats,movie_code="001")
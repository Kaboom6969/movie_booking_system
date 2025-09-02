import csv #From python standard library
import warnings #From python standard library




#Read seat data for a specific movie from a CSV file into a 2D list
def read_movie_seats_csv (movie_seats_csv : csv,movie_seat :list,movie_code : str) -> None:
    list_found = False      #Flag to track if movie_code is found
    start_status = False    #Flag tso track if in seat data section (between START and END)
    try:
        with open(movie_seats_csv, 'r', newline='') as ms_csv_r:
            movie_seat_reader = csv.reader(ms_csv_r)
            next(movie_seat_reader)         #Skip header row (movie_code,y0,y1,...)
            for row in movie_seat_reader:
                if row[0] == movie_code:    #Found matching movie_code
                    list_found = True
                    continue
                if row[0] == "START" and list_found:    #Found START marker, start reading
                    start_status = True
                    continue
                if row[0] == "END" and list_found:      #Found END marker, stop reading
                    break
                if start_status and list_found:         #Reading...
                    movie_seat.append(row[1:])          #Append seat data (skip first column)
            if list_found and start_status == False:    #Found movie_code but no START (usually file writing error)
                raise IndexError("Your Movie Seat List is Empty! Found the movie code but START is not Found!")
            elif list_found == False:                   #Movie_code not found
                raise IndexError("Your Movie Seat List is Empty! Cannot Found the movie code!")

    except FileNotFoundError:
        raise FileNotFoundError (f"File not found!\nYour file name is {movie_seats_csv}.\nPlease Check The Name!")

#Overwrite target file with contents of a temporary file
def _overwrite_file (overwrited_file : csv,original_file : csv) -> None:
        with open(original_file, 'r', newline='') as ori_file_r, open(overwrited_file, 'w', newline='') as overwrited_file_w:
            oni_file_reader = csv.reader(ori_file_r)                #Create reader for source file
            overwrited_file_writer = csv.writer(overwrited_file_w)  #Create writer for target file
            for row in oni_file_reader:                             #Copy each row
                overwrited_file_writer.writerow(row)

#Update seat data for a specific movie_code in the CSV file
def update_movie_seats_csv (movie_seats_csv : csv, movie_seat: list, movie_code : str) -> None:
    with open(movie_seats_csv, 'r', newline='') as ms_csv_r, open(f"{movie_seats_csv}.temp","w", newline='') as ms_csv_w:
            movie_seat_writer = csv.writer(ms_csv_w)        #Create writer for temporary file
            movie_seat_reader = csv.reader(ms_csv_r)        #Create reader for CSV file
            list_found_all_times = False                    #Track if movie_code was ever found
            list_found = False                              #Track if currently processing target movie_code
            start_status = False                            #Track if in START-END section
            count = 0                                       #Counter for writing movie_seat rows (got bug but use first)
            for row in movie_seat_reader:
                if list_found and start_status and row and row[0] == "END":     #Found END marker
                    start_status = False
                    list_found = False
                if list_found and start_status:                                 #In START-END section, write new seat data
                    movie_seat_writer.writerow(["",*movie_seat[count][0:]])     #Write row with empty first column
                    count += 1
                    continue
                if row and row[0] == movie_code:                                #Found movie_code
                    list_found = True
                    list_found_all_times = True
                if list_found and row and row[0] == "START": start_status = True#Writing...
                movie_seat_writer.writerow(row)             #Copy other rows to temporary file
            if list_found_all_times == False:               #Movie_code not found
                raise ValueError("Movie Code Does Not Exist! You Should Use add_movie_seats_csv function")

    _overwrite_file(overwrited_file = movie_seats_csv, original_file = f"{movie_seats_csv}.temp")   #Overwrite original file

#Add a new seat table for a movie_code to the CSV file
def add_movie_seats_csv (movie_seat_csv : csv, movie_seat : list, movie_code : str) -> None:
    with (open(movie_seat_csv,'r',newline= '') as ms_csv_r ,
          open(f"{movie_seat_csv}.temp","w", newline='') as ms_csv_w):
        movie_seat_reader = csv.reader(ms_csv_r)    #Create reader for CSV file
        movie_seat_writer = csv.writer(ms_csv_w)    #Create writer for temporary file
        for row in movie_seat_reader:       #Copy existing content
            try:
                movie_seat_writer.writerow(row)
                if row and row[0] == movie_code:    #Check if movie_code already exists
                    raise ValueError ("Movie Code Already Exists! You Should Use write_movie_seats_csv function!")
            except ValueError as e:
                raise e
        #Create headers for movie_code, START, and END rows
        movie_code_header : list = _header_create(header_text = movie_code , movie_seats_length= len(movie_seat[0]) + 1, append_thing= "")
        start_header : list = _header_create(header_text = "START" , movie_seats_length = len(movie_seat[0]) + 1 , append_thing= "-2")
        movie_seat_writer.writerow(movie_code_header)       #Write movie_code row
        movie_seat_writer.writerow(start_header)            #Write START row
        for row in movie_seat:                              #Write seat data
            movie_seat_writer.writerow(["",*row])           #Add empty first column [""...
        end_header : list = _header_create(header_text = "END" , movie_seats_length = len(movie_seat[0]) + 1 , append_thing= "-2")
        movie_seat_writer.writerow(end_header)              #Write END row

    _overwrite_file(overwrited_file= "movie_seat.csv", original_file= f"{movie_seat_csv}.temp")     #Overwrite original file

def delete_movie_seats_csv (movie_seat_csv : csv, movie_code : str) -> None:
    try:
        with (open(movie_seat_csv,'r',newline = '') as ms_csv_r ,
        open(f"{movie_seat_csv}.temp","w", newline='') as ms_csv_w):
            movie_seat_reader = csv.reader(ms_csv_r)
            movie_seat_writer = csv.writer(ms_csv_w)
            list_found_all_times = False
            list_found = False
            end_status = False
            delete_count = 0
            for row in movie_seat_reader:
                if row and row[0] == movie_code:
                    list_found = True
                    list_found_all_times = True
                    continue
                elif list_found and row and row[0] == "END":
                    end_status = True
                    list_found = False
                    delete_count += 1
                    continue
                elif list_found: continue
                movie_seat_writer.writerow(row)
            if list_found_all_times == False:
                raise KeyError(f"Cannot Find The Movie Code! Movie Code : {movie_code}")
            if delete_count > 1:
                warnings.warn(f"delete_movie_seats_csv function delete {delete_count} times.")

        _overwrite_file(overwrited_file=movie_seat_csv, original_file=f"{movie_seat_csv}.temp")

    except FileNotFoundError as e:
        raise FileNotFoundError(f"Cannot Find File {movie_seat_csv}!")


#Generate a header row for CSV (e.g., movie_code, START, END)
def _header_create (header_text : str , movie_seats_length : int , append_thing :str) -> list:
    header : list = []
    header.append(header_text)                  #Add header text
    for i in range(0,movie_seats_length - 1):   #Fill remaining columns
        header.append(append_thing)
    return header

#Fill all seats in the seat list with a specified value
def fill_movie_seats_list (movie_seat_list : list, fill_number : int) -> None:
    for i in range (0,len(movie_seat_list)):
        for j in range (0,len(movie_seat_list[0])):
            movie_seat_list[i][j] = str(fill_number)

#Modify the state of a specific seat
def modify_movie_seat(movie_seat_list: list, x_axis: int, y_axis: int, target_number: int) -> None:
    if not movie_seat_list:                                 #Check if list is empty
        raise IndexError("Your Movie Seat List is Empty!")
    if x_axis < 1 or x_axis > len(movie_seat_list[0]):      #Validate x_axis
        raise IndexError(f"x_axis should be between 1 and {len(movie_seat_list[0])}\nYour x_axis is {x_axis}")
    if y_axis < 1 or y_axis > len(movie_seat_list):         #Validate y_axis
        raise IndexError(f"y_axis should be between 1 and {len(movie_seat_list)}\nYour y_axis is {y_axis}")
    movie_seat_list[len(movie_seat_list) - y_axis][x_axis - 1] = str(target_number)     #Modify specified seat



#Print seat list as text
def print_movie_seats_list (movie_seat_list : list) -> None:
    for main_list in movie_seat_list:
        print()
        for second_list in main_list:
            print(second_list,end= " ")

#Print seat list as emojis
def print_movie_seats_list_as_emojis (movie_seat_list : list) -> None:
    for main_list in movie_seat_list:
        print()
        for second_list in main_list:
            if second_list == "0":
                print("🈳",end=" ")
            elif second_list == "1":
                print("👨",end=" ")
            elif second_list == "-1":
                print("❌",end=" ")


#作为library时不会被启用，仅有亲自运行此文件才会运行（用来测试用）
if __name__ == '__main__':
    movie_seats_list_global : list = []
    #read_movie_seats_csv (movie_seats_csv="movie_seat.csv",movie_seat=movie_seats_list_global,movie_code="002")
    #fill_movie_seats_list (movie_seat_list=movie_seats_list_global, fill_number=1)
    #print (movie_seats_list_global)
    #update_movie_seats_csv(movie_seats_csv="movie_seat.csv",movie_seat= movie_seats_list_global,movie_code="002")
    #add_movie_seats_csv(movie_seat_csv= "movie_seat.csv", movie_seat= movie_seats_l-ist_global, movie_code="004")
    # modify_movie_seat(movie_seat_list=movie_seat_list_global, x_axis = 1,y_axis =2,target_number = -1)
    # print_movie_seats_list(movie_seat_list= movie_seat_list_global)
    # print_movie_seats_list_as_emojis(movie_seat_list= movie_seats_list_global)
    #delete_movie_seats_csv(movie_seat_csv="movie_seat.csv", movie_code="002")



import csv #From python standard library
import os #From python standard library
from itertools import count


#读取csv档案到某一个二维数组（自己决定）用来把储存的座位表拉出来处理
def read_movie_seats_csv (movie_seats_csv : csv,movie_seat :list,movie_code : str) -> None:
    list_found = False
    start_status = False
    try:
        with open(movie_seats_csv, 'r', newline='') as ms_csv_r:
            movie_seat_reader = csv.reader(ms_csv_r)
            next(movie_seat_reader)
            for row in movie_seat_reader:
                if row[0] == movie_code:
                    list_found = True
                    continue
                if row[0] == "START" and list_found:
                    start_status = True
                    continue
                if row[0] == "END" and list_found:
                    break
                if start_status and list_found:
                    movie_seat.append(row[1:])
            if list_found and start_status == False:
                raise IndexError("Your Movie Seat List is Empty! Found the movie code but START is not Found!")
            elif list_found == False:
                raise IndexError("Your Movie Seat List is Empty! Cannot Found the movie code!")

    except FileNotFoundError:
        raise FileNotFoundError (f"File not found!\nYour file name is {movie_seats_csv}.\nPlease Check The Name!")

def _overwrite_file (overwrited_file : csv,original_file : csv) -> None:
        with open(original_file, 'r', newline='') as ori_file_r, open(overwrited_file, 'w', newline='') as overwrited_file_w:
            oni_file_reader = csv.reader(ori_file_r)
            overwrited_file_writer = csv.writer(overwrited_file_w)
            for row in oni_file_reader:
                overwrited_file_writer.writerow(row)

def write_movie_seats_csv (movie_seats_csv : csv, movie_seat: list, movie_code : str) -> None:
    with open(movie_seats_csv, 'r', newline='') as ms_csv_r, open(f"{movie_seats_csv}.temp","w", newline='') as ms_csv_w:
            movie_seat_writer = csv.writer(ms_csv_w)
            movie_seat_reader = csv.reader(ms_csv_r)
            list_found_all_times = False
            list_found = False
            start_status = False
            count = 0
            for row in movie_seat_reader:
                if list_found and start_status and row and row[0] == "END":
                    start_status = False
                    list_found = False
                if list_found and start_status:
                    movie_seat_writer.writerow(["",*movie_seat[count][0:]])
                    count += 1
                    continue
                if row and row[0] == movie_code:
                    list_found = True
                    list_found_all_times = True
                if list_found and row and row[0] == "START":
                    start_status = True
                movie_seat_writer.writerow(row)
            if list_found_all_times == False:
                raise ValueError("Movie Code Does Not Exist! You Should Use add_movie_seats_csv function")

    _overwrite_file(overwrited_file = movie_seats_csv, original_file = f"{movie_seats_csv}.temp")

def add_movie_seats_csv (movie_seat_csv : csv, movie_seat : list, movie_code : str) -> None:
    with open(movie_seat_csv,'r',newline= '') as ms_csv_r ,open(f"{movie_seat_csv}.temp","w", newline='') as ms_csv_w:
        movie_seat_reader = csv.reader(ms_csv_r)
        movie_seat_writer = csv.writer(ms_csv_w)
        for row in movie_seat_reader:
            try:
                movie_seat_writer.writerow(row)
                if row and row[0] == movie_code:
                    raise ValueError ("Movie Code Already Exists! You Should Use write_movie_seats_csv function!")
            except ValueError as e:
                raise e
        movie_code_header : list = _header_create(header_text = movie_code , movie_seats_length= len(movie_seat[0]) + 1, append_thing= "")
        start_header : list = _header_create(header_text = "START" , movie_seats_length = len(movie_seat[0]) + 1 , append_thing= "-2")
        movie_seat_writer.writerow(movie_code_header)
        movie_seat_writer.writerow(start_header)
        for row in movie_seat:
            movie_seat_writer.writerow(["",*row])
        end_header : list = _header_create(header_text = "END" , movie_seats_length = len(movie_seat[0]) + 1 , append_thing= "-2")
        movie_seat_writer.writerow(end_header)

    _overwrite_file(overwrited_file= "movie_seat.csv", original_file= f"{movie_seat_csv}.temp")


def _header_create (header_text : str , movie_seats_length : int , append_thing :str) -> list:
    header : list = []
    header.append(header_text)
    for i in range(0,movie_seats_length - 1):
        header.append(append_thing)
    return header




def fill_movie_seats_list (movie_seat_list : list, fill_number : int) -> None:
    for i in range (0,len(movie_seat_list)):
        for j in range (0,len(movie_seat_list[0])):
            movie_seat_list[i][j] = str(fill_number)

def modify_movie_seat(movie_seat_list: list, x_axis: int, y_axis: int, target_number: int) -> None:
    if not movie_seat_list:
        raise IndexError("Your Movie Seat List is Empty!")
    if x_axis < 1 or x_axis > len(movie_seat_list[0]):
        raise IndexError(f"x_axis should be between 1 and {len(movie_seat_list[0])}\nYour x_axis is {x_axis}")
    if y_axis < 1 or y_axis > len(movie_seat_list):
        raise IndexError(f"y_axis should be between 1 and {len(movie_seat_list)}\nYour y_axis is {y_axis}")
    movie_seat_list[len(movie_seat_list) - y_axis][x_axis - 1] = str(target_number)




def print_movie_seats_list (movie_seat_list : list) -> None:
    for main_list in movie_seat_list:
        print()
        for second_list in main_list:
            print(second_list,end= " ")

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
    read_movie_seats_csv (movie_seats_csv="movie_seat.csv",movie_seat=movie_seats_list_global,movie_code="002")
    fill_movie_seats_list (movie_seat_list=movie_seats_list_global, fill_number=1)
    print (movie_seats_list_global)
    write_movie_seats_csv(movie_seats_csv="movie_seat.csv",movie_seat= movie_seats_list_global,movie_code="002")
    add_movie_seats_csv(movie_seat_csv= "movie_seat.csv", movie_seat= movie_seats_list_global, movie_code="004")
        # modify_movie_seat(movie_seat_list=movie_seat_list_global, x_axis = 1,y_axis =2,target_number = -1)
        # print_movie_seats_list(movie_seat_list= movie_seat_list_global)
        # print_movie_seats_list_as_emojis(movie_seat_list= movie_seats_list_global)



from .framework_utils import *
import re

def movie_seats_valid_check (movie_seats_list : list) -> None:
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

def movie_seats_csv_valid_check (movie_seats_csv : str) -> None:
    movie_seats_csv_path = get_path(movie_seats_csv)
    try:
        with open(movie_seats_csv_path,'r',newline ='') as ms_csv_r:
            CODE_status = False
            START_status = False
            END_status = False
            DATA_status = False
            line_count = 0
            for lines in ms_csv_r:
                row = str_line_to_list(lines)
                line_count += 1
                if not row: raise ValueError(f"GOT BLANK IN THE FILE!\nFile name:{movie_seats_csv}\nFile path:{movie_seats_csv_path}\nLine:{line_count}")
                if row[0] == "CODE":
                    CODE_status = True
                    if not re.match(pattern = r"\d{4}",string = row[1]):
                        raise ValueError(f"MOVIE CODE IS INVALID\nFile name:{movie_seats_csv}\nFile path:{movie_seats_csv_path}\n"
                                     f"Line:{line_count}\nThis Row: {row}")
                    if "TEMPLATE" not in row[2]:
                        raise ValueError(f"TEMPLATE CODE IS INVALID!\nFile name:{movie_seats_csv}\nFile path:{movie_seats_csv_path}\n"
                                     f"Line:{line_count}\nThis Row: {row}")
                if row[0] == "START": START_status = True
                if row[0] == "DATA" : DATA_status = True
                if row[0] == "END": END_status = True
                if DATA_status and not START_status:
                    raise ValueError(f"START or END DIDN'T FOUND!\nFile name:{movie_seats_csv}\nFile path:{movie_seats_csv_path}\n"
                                     f"Line:{line_count}\nThis Row: {row[0]}\nLAST Row:{row_head_temp}")
                if START_status and not CODE_status:
                    raise ValueError(f"MOVIE_CODE DIDN'T FOUND!\nFile name:{movie_seats_csv}\nFile path:{movie_seats_csv_path}\n"
                                     f"Line:{line_count}\nThis Row: {row[0]}\nLAST Row:{row_head_temp}")
                if END_status and not START_status:
                    raise ValueError(f"START HEADER DIDN'T FOUND!\nFile name:{movie_seats_csv}\nFile path:{movie_seats_csv_path}\nLine:{line_count}")
                if CODE_status and START_status and END_status and DATA_status:
                    CODE_status = False
                    START_status = False
                    END_status = False
                    DATA_status = False
                row_head_temp = row[0]
            if START_status and CODE_status: raise ValueError (f"END HEADER LOST!\nFile name:{movie_seats_csv}"
                                                   f"\nFile path:{movie_seats_csv_path}\nLine:{line_count}")
            if CODE_status: raise ValueError(f"START HEADER AND END HEADER LOST!\nFile name:{movie_seats_csv}"
                                                   f"\nFile path:{movie_seats_csv_path}\nLine:{line_count}")
            if DATA_status: raise ValueError(f"END HEADER LOST!\nFile name:{movie_seats_csv}"
                                                   f"\nFile path:{movie_seats_csv_path}\nLine:{line_count}")
            if START_status or END_status or CODE_status:
                raise ValueError(f"FORMAT ERROR! COULD NOT PINPOINT THE EXACT ISSUE. PLEASE REVIEW YOUR FILE!\nFile name:{movie_seats_csv}\nFile path:{movie_seats_csv_path}")
    except ValueError as e:
        raise e
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File '{movie_seats_csv}' not found!File path:{movie_seats_csv_path}")

def movie_seats_pointer_valid_check(movie_seats : list,x_pointer : int,y_pointer : int) -> bool:
    try:
        if not movie_seats: raise ValueError(f"{movie_seats} is empty!")
        point_value : str = movie_seats[len(movie_seats) - y_pointer][x_pointer - 1]
        return True
    except IndexError:
        return False
    except ValueError as e:
        raise e


def date_valid_check(date : str) -> tuple[bool, str]:
    date_format : str = "YYYY/MM/DD"
    def leap_year_check(year : int) -> bool:
        if year % 4 == 0 and year % 100 != 0: return True
        if year % 400 == 0: return True
        return False

    date_list : list = date.split('/')
    if len(date_list) != 3 : return False,date_format
    for element in date_list:
        if not element.isdigit(): return False,date_format
    if len(date_list[0]) != 4: return False,date_format
    if len(date_list[1]) != 2: return False, date_format
    if len(date_list[2]) != 2: return False, date_format

    year = int(date_list[0])
    month = int(date_list[1])
    day = int(date_list[2])

    month_30_day : list =[4,6,9,11]
    if month > 12 or month <= 0: return False,date_format
    if day > 31 or day <= 0: return False,date_format
    if month in month_30_day and day > 30:return False,date_format
    if month == 2 and not leap_year_check(year) and day > 28: return False,date_format
    if month == 2 and leap_year_check(year) and day > 29: return False,date_format
    return True,""

def time_valid_check(time : str) -> tuple[bool, str]:
    time_format : str = "HH:MM"
    time_list : list = time.split(':')
    if len(time_list) != 2 : return False,time_format
    for element in time_list:
        if not element.isdigit(): return False,time_format
    if len(time_list[0]) != 2 or len(time_list[1]) != 2: return False,time_format
    hour = int(time_list[0])
    minute = int(time_list[1])
    if hour > 23: return False,time_format
    if minute > 59: return False,time_format
    return True,""

def number_valid_check(number : str) -> tuple[bool, str]:
    number_format : str = "Number"
    if not number.isdigit(): return False,number_format
    return True,""
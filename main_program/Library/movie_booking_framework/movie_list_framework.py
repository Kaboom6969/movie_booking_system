import csv
import os
import re
import warnings
from movie_booking_system.main_program.Library.movie_booking_framework.movie_seats_framework import _get_path,_overwrite_file,parse_csv_line


def read_movie_list_csv (movie_list_csv : str,movie_list : list,movie_code : str = "all") ->None:
    try:
        movie_list_csv_path = _get_path(movie_list_csv)
        with open(movie_list_csv_path , 'r' , newline= '') as mv_csvfile:
            movie_list_reader = csv.reader(mv_csvfile)
            next(movie_list_reader)
            if movie_code == "all":
                for row in movie_list_reader:
                    movie_list.append(row)
                if movie_code == "":
                    raise ValueError("Movie Not Found! Please Check Your File!")
            else:
                list_found = False
                for row in movie_list_reader:
                    if row[0] == movie_code:
                        list_found = True
                        movie_list.append(row)
                if list_found == False:
                    raise ValueError("Movie Code Not Found! Please Check Your File!")
    except  FileNotFoundError:
        raise FileNotFoundError(f"File Not Found!\nYour File Name is {movie_list_csv}.\nPLease Check Your File! ")
    except ValueError as e:
        raise e

def update_movie_list_csv (movie_list_csv : str,movie_list : list,movie_code : str = "all") ->None:
    movie_list_csv_path = _get_path(movie_list_csv)
    movie_list_csv_temp_path = os.path.dirname(movie_list_csv_path)
    with (open(movie_list_csv_path , 'r' , newline= '') as mvl_csv_r,
          open(os.path.join(movie_list_csv_temp_path,f"{movie_list_csv}.temp"),'w',newline= '') as mvl_csv_w):
        movie_list_reader = csv.reader(mvl_csv_r)
        movie_list_writer = csv.writer(mvl_csv_w)
        movie_list_dict : dict = {row[0] : row for row in movie_list}
        if movie_code == "all":
            movie_list_writer.writerow(next(movie_list_reader))
            for row in movie_list_reader:
                if row[0] in movie_list_dict:
                    movie_list_writer.writerow(movie_list_dict[row[0]])
                    del movie_list_dict[row[0]]
                    continue
                movie_list_writer.writerow(row)
        elif not re.fullmatch(pattern= r"\d{3}",text= movie_code):
            raise ValueError("Movie code must be a three-digit number!")
        else:
            try:
                movie_list_writer.writerow(next(movie_list_reader))
                movie_list_specify : list  = movie_list_dict[movie_code]
                for row in movie_list_reader:
                    if row[0] == movie_list_specify[0]:
                        movie_list_writer.writerow(movie_list_specify)
                        continue
                    movie_list_writer.writerow(row)
            except KeyError:
                raise IndexError("Movie Code is not in the list!")

    _overwrite_file(overwrited_file_csv=movie_list_csv, original_file_csv=f"{movie_list_csv}.temp")

def add_movie_list_csv (movie_list_csv : str,movie_list : list,movie_code : str) -> None:
    try:
        if movie_code == "all": raise ValueError("'all' isn't supported in this function!")
        movie_list_dict : dict = {row[0]:row for row in movie_list}
        movie_list_for_add : list =[]
        code_list_matcher = 0
        for row in movie_list_dict:
            if row == movie_code:
                if code_list_matcher == 0:movie_list_for_add.append(movie_list_dict[row])
                code_list_matcher += 1
        if code_list_matcher == 0: raise ValueError(f"Movie Code is not matched in {movie_list}!")
        if code_list_matcher > 1: warnings.warn(f"More than 2 Movie Code Founded in {movie_list}! System will use the First one")
        movie_list_csv_path: str = _get_path(movie_list_csv)
        movie_list_csv_temp_path : str = os.path.dirname(movie_list_csv_path)
        with (open(movie_list_csv_path , 'r' , newline= '') as mvl_csv_r,
              open(os.path.join(movie_list_csv_temp_path,f"{movie_list_csv}.temp"),'w',newline= '') as mvl_csv_w):
            movie_list_reader = csv.reader(mvl_csv_r)
            movie_list_writer = csv.writer(mvl_csv_w)
            for row in movie_list_reader:
                movie_list_writer.writerow(row)
                if row[0] == movie_code:
                    raise ValueError(f"Movie Code Repeat! You Should Use update_movie_list_csv function!")
            movie_list_writer.writerows(movie_list_for_add)

    except FileNotFoundError as e:
        raise FileNotFoundError(f"ADD MOVIE FAILED! ERROR:{e}")
    except ValueError as e:
        raise ValueError(f"ADD MOVIE FAILED! ERROR:{e}")
    except Exception as e:
        raise Exception(f"ADD MOVIE FAILED! UNKNOWN ERROR:{e}")

def delete_movie_list_csv (movie_list_csv : str,movie_code : str) -> None:
    movie_list_csv_path = _get_path(movie_list_csv)
    movie_list_csv_temp_path = os.path.dirname(movie_list_csv_path)
    with (open(movie_list_csv_path,'r') as mvl_csv_r,
          open(os.path.join(movie_list_csv_temp_path,f"{movie_list_csv}.temp"),'w') as mvl_csv_w):
        code_csv_matcher = 0
        for line in mvl_csv_r:
            if not line.strip(): continue
            row = parse_csv_line(line)
            if row[0] == movie_code:
                code_csv_matcher += 1
            else:
                mvl_csv_w.write(line)
        if code_csv_matcher == 0:
            raise ValueError(f"Didn't find the movie code:{movie_code} in {movie_list_csv}!")
        if code_csv_matcher > 1:
            warnings.warn(f"Found more than 2 movie code:{movie_code} in {movie_list_csv},system will delete all!")
    _overwrite_file(overwrited_file_csv=movie_list_csv, original_file_csv=f"{movie_list_csv}.temp")









if __name__ == '__main__':
    try:
        movie_list_global: list = []
        read_movie_list_csv(movie_list_csv= "movie_list.csv", movie_list= movie_list_global, movie_code="002")
        # print(movie_list_global)
        update_movie_list_csv(movie_list_csv= "movie_list_2_test.csv", movie_list= movie_list_global)

    except ValueError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)





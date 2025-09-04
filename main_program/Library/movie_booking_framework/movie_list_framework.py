import csv
import os
from _movie_seats_framework_ import _get_path,_overwrite_file
def read_movie_list_csv (movie_list_csv : str,movie_list : list,movie_code : str = "all") ->None:
    try:
        movie_list_csv_path = _get_path(movie_list_csv)
        with open(movie_list_csv_path , 'r' , newline= '') as mv_csvfile:
            movie_list_reader = csv.reader(mv_csvfile)
            next(movie_list_reader)
            if movie_code == "all":
                for row in movie_list_reader:
                    movie_list.append(row)
                if movie_code == []:
                    raise ValueError("Movie Not Found! Please Check Your File!")
            else:
                list_found = False
                for row in movie_list_reader:
                    if row[0] == movie_code and list_found == True:
                        raise ValueError("Movie Code Repeat! Please Check Your File!")
                    elif row[0] == movie_code:
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
        if movie_code == "all":
            for csv_row in movie_list_reader:
                for list_row in movie_list:
                    if csv_row[0] == list_row[0]:
                        movie_list_writer.writerow(list_row)
                        continue
                movie_list_writer.writerow(csv_row)





if __name__ == '__main__':
    try:
        movie_list_global : list = []
        read_movie_list_csv(movie_list_csv= "movie_list.csv", movie_list= movie_list_global, movie_code="002")
        print(movie_list_global)

    except ValueError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)





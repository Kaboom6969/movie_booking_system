from .framework_utils import *


def read_movie_list_csv(movie_list_csv: str, movie_list: list, movie_code: str = "all", movie_mode: bool = True,
                        code_location: int = 0) -> None:
    try:
        movie_list_csv_path = get_path(movie_list_csv)
        with open(movie_list_csv_path, 'r') as mv_csvfile:
            next(mv_csvfile)
            if movie_code == "all":
                for line in mv_csvfile:
                    if not line.strip(): continue
                    row = parse_csv_line(line)
                    movie_list.append(row)
                if not movie_code:
                    raise ValueError("Code is empty! Please Check Your movie_code parameter!")
            else:
                list_found = False
                for line in mv_csvfile:
                    if not line.strip(): continue
                    row = parse_csv_line(line)
                    if row[code_location] == movie_code and list_found == True and movie_mode == True:
                        raise ValueError("Code Repeat! Please Check Your File!")
                    elif row[code_location] == movie_code:
                        list_found = True
                        movie_list.append(row)
                if list_found == False:
                    raise ValueError("Code Not Found! Please Check Your File!")
    except FileNotFoundError:
        raise FileNotFoundError(f"File Not Found!\nYour File Name is {movie_list_csv}.\nPLease Check Your File! ")
    except ValueError as e:
        raise e


def update_movie_list_csv(movie_list_csv: str, movie_list: list, movie_code: str = "all",
                          code_location: int = 0) -> None:
    movie_list_csv_path = get_path(movie_list_csv)
    movie_list_csv_temp_path = os.path.dirname(movie_list_csv_path)

    try:
        with (open(movie_list_csv_path, 'r') as mvl_csv_r,
                open(os.path.join(movie_list_csv_temp_path, f"{movie_list_csv}.temp"), 'w') as mvl_csv_w):
            movie_list_dict: dict = {row[code_location]: row for row in movie_list}
            header_line = next(mvl_csv_r)
            mvl_csv_w.write(header_line)
            if movie_code == "all":
                for line in mvl_csv_r:
                    if not line.strip(): continue
                    row = parse_csv_line(line)
                    if row[code_location] in movie_list_dict:
                        line_to_write = format_csv_line(movie_list_dict[row[code_location]])
                        mvl_csv_w.write(line_to_write)
                        del movie_list_dict[row[code_location]]
                    else:
                        mvl_csv_w.write(line)
            else:
                try:
                    movie_list_specify: list = movie_list_dict[movie_code]
                    for line in mvl_csv_r:
                        if not line.strip(): continue
                        row = parse_csv_line(line)
                        if row[code_location] == movie_list_specify[code_location]:
                            line_to_write = format_csv_line(movie_list_specify)
                            mvl_csv_w.write(line_to_write)
                        else:
                            mvl_csv_w.write(line)
                except KeyError:
                    raise IndexError("Movie Code is not in the list!")
    except Exception as e:
        raise Exception(f"UPDATE LIST ERROR!ERROR:{e}")
    overwrite_file(overwrited_file_csv=movie_list_csv, original_file_csv=f"{movie_list_csv}.temp")

def add_movie_list_csv(movie_list_csv: str, movie_list: list, movie_code: str, code_location: int = 0) -> None:
    try:
        if movie_code == "all": raise ValueError("'all' isn't supported in this function!")
        movie_list_dict: dict = {row[code_location]: row for row in movie_list}
        movie_list_for_add: list = []
        code_list_matcher = 0
        for row_key in movie_list_dict:
            if row_key == movie_code:
                if code_list_matcher == 0: movie_list_for_add.append(movie_list_dict[row_key])
                code_list_matcher += 1
        if code_list_matcher == 0: raise ValueError(f"Movie Code is not matched in {movie_list}!")
        if code_list_matcher > 1: warnings.warn(f"More than 2 Movie Code Founded in {movie_list}! System will use the First one")
        movie_list_csv_path: str = get_path(movie_list_csv)
        movie_list_csv_temp_path: str = os.path.dirname(movie_list_csv_path)
        with (open(movie_list_csv_path, 'r') as mvl_csv_r,
                open(os.path.join(movie_list_csv_temp_path, f"{movie_list_csv}.temp"), 'w') as mvl_csv_w):
            for line in mvl_csv_r:
                mvl_csv_w.write(line)
                if not line.strip(): continue
                row = parse_csv_line(line)
                if row[code_location] == movie_code:
                    raise ValueError(f"Movie Code Repeat! You Should Use update_movie_list_csv function!")
            for row_to_add in movie_list_for_add:
                line_to_write = format_csv_line(row_to_add)
                mvl_csv_w.write(line_to_write)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"ADD MOVIE FAILED! ERROR:{e}")
    except ValueError as e:
        raise ValueError(f"ADD MOVIE FAILED! ERROR:{e}")
    except Exception as e:
        raise Exception(f"ADD MOVIE FAILED! UNKNOWN ERROR:{e}")
    overwrite_file(overwrited_file_csv=movie_list_csv, original_file_csv=f"{movie_list_csv}.temp")

def delete_movie_list_csv (movie_list_csv : str,movie_code : str,code_location : int = 0) -> None:
    movie_list_csv_path = get_path(movie_list_csv)
    movie_list_csv_temp_path = os.path.dirname(movie_list_csv_path)
    with (open(movie_list_csv_path,'r') as mvl_csv_r,
          open(os.path.join(movie_list_csv_temp_path,f"{movie_list_csv}.temp"),'w') as mvl_csv_w):
        code_csv_matcher = 0
        for line in mvl_csv_r:
            if not line.strip(): continue
            row = parse_csv_line(line)
            if row[code_location] == movie_code:
                code_csv_matcher += 1
            else:
                mvl_csv_w.write(line)
        if code_csv_matcher == 0:
            raise ValueError(f"Didn't find the movie code:{movie_code} in {movie_list_csv}!")
        if code_csv_matcher > 1:
            warnings.warn(f"Found more than 2 movie code:{movie_code} in {movie_list_csv},system will delete all!")
    overwrite_file(overwrited_file_csv=movie_list_csv, original_file_csv=f"{movie_list_csv}.temp")










if __name__ == '__main__':
    pass




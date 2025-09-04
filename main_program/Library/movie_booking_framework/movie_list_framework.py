import csv
import movie_seats_framework

def read_movie_list_csv (movie_list_csv : csv,movie_list : list,movie_code : str) ->None:
    try:
        with open(movie_list_csv , 'r' , newline= '') as mv_csvfile:
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
    except  FileNotFoundError as e:
        raise FileNotFoundError(f"File Not Found!\nYour File Name is {movie_list_csv}.\nPLease Check Your File! ")
    except ValueError as e:
        raise e




if __name__ == '__main__':
    try:
        movie_list_global : list = []
        read_movie_list_csv(movie_list_csv= "movie_list.csv", movie_list= movie_list_global, movie_code="002")
        print(movie_list_global)

    except ValueError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)





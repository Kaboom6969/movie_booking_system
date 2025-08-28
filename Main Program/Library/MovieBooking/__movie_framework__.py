import csv
movie_seat_list_global =[]
def read_movie_seats_list (movie_seats_csv : csv,movie_code : str) -> list:
    list_found = False
    start_status = False
    movie_seat_list = []
    try:
        with open(movie_seats_csv, newline='') as csvfile:
            movie_seat_reader = csv.reader(csvfile)
            next(movie_seat_reader)
            for row in movie_seat_reader:
                if row[0] == movie_code:
                    list_found = True
                    continue
                if row[0] == "START" and list_found:
                    start_status = True
                    continue
                if row[0] == "END" and list_found:
                    start_status = False
                    break
                if start_status and list_found:
                    movie_seat_list.append(row[1:])
    except FileNotFoundError:
        raise FileNotFoundError (f"File not found!\nYour file name is {movie_seats_csv}.\nPlease Check The Name!")
    return movie_seat_list

def modify_movie_seat (movie_seat_list : list, x_axis : int, y_axis :int,target_number : int) -> None:
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


if __name__ == '__main__':
    try:
        movie_seat_list_global = read_movie_seats_list ("movie_seat.csv","001")
        modify_movie_seat(movie_seat_list=movie_seat_list_global, x_axis = 1,y_axis =2,target_number = -1)
        print_movie_seats_list(movie_seat_list= movie_seat_list_global)
        print_movie_seats_list_as_emojis(movie_seat_list= movie_seat_list_global)
    except IndexError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)



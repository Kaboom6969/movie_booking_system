from .valid_checker import *

def print_movie_seat (movie_seats : list) -> None:
    try:
        movie_seats_valid_check(movie_seats_list=movie_seats)
    except ValueError as e:
        raise ValueError (f"Print Movie Seats Failed! Movie Seat List ERROR! {e}")
    for main_list in movie_seats:
        print()
        for second_list in main_list:
            print(second_list,end= " ")

#Print seat list as emojis
def print_movie_seat_as_emojis (movie_seats : list,x_pointer : int = -1,y_pointer : int = -1) -> None:
    try:
        movie_seats_valid_check(movie_seats_list=movie_seats)
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



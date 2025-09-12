from movie_booking_system.main_program.Library.movie_booking_framework.movie_list_framework import read_movie_list_csv
from movie_booking_system.main_program.Library.movie_booking_framework.movie_seats_framework import *


def clerk():
    # 订票
    movie_list = []
    read_movie_list_csv(movie_list_csv="movie_list.csv", movie_list=movie_list, movie_code="all")
    while True:
        print(movie_list)
        # 输入代码
        movie_code = input("please enter your movie code: ")
        flag = False
        for movie in movie_list:
            if movie[0] == movie_code:
                flag = True
        if flag:
            break
        else:
            print("please enter valid movie code")

    movie_seat_list = []
    read_movie_seats_csv(movie_seats_csv="movie_seat.csv", movie_seats=movie_seat_list, movie_code='001')
    print_movie_seat_as_emojis(movie_seat_list)
    print("please enter your choice:")
    while True:
        choice  = input("booking(1), cancel or modify booking(2), check movie seats(3), print receipt(4), quit(5)")
        if choice == "1":
            row = int(input("\nPlease enter the row number: "))
            seat = int(input("Please enter the seat number: "))
            if seat < 1 or seat > len(movie_seat_list[0]):      #Validate x_axis
                print(f"seat should be between 1 and {len(movie_seat_list[0])}\nYour seat is {seat}")
            if row < 1 or row > len(movie_seat_list):         #Validate y_axis
                print(f"row should be between 1 and {len(movie_seat_list)}\nYour row is {row}")
            modify_movie_seats_list(movie_seats_list, seat, row, 1)
        elif choice == "2":
            print("cancel")
        elif choice == "3":
            print_movie_seat_as_emojis(movie_seat_list)
        elif choice == "4":
            print("receipt")
        elif choice == "5":
            break
    print_movie_seat_as_emojis(movie_seats_list)



# 取消或修改booking
# 查看电影列表
# 打印订单

def main():
    clerk()


if __name__ == '__main__':
    main()

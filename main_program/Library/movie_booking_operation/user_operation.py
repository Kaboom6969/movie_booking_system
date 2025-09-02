from ..movie_booking_framework import _movie_seats_framework_
#测试用 python -m main_program.Library.movie_booking_operation.user_operation
def delete_movie(movie_seats_csv : str, movie_list_csv : str) -> None:
    movie_code_input = str(input("Enter Movie Code That You Want To Delete: "))
    _movie_seats_framework_.delete_movie_seats_csv(movie_seats_csv= movie_seats_csv, movie_code=movie_code_input)
    #这里还要再删除movie list，只是我还没做那个函数

if __name__ == '__main__':
    delete_movie("MOVIE_SEATS_TEST.csv","NOTHING.CSV")
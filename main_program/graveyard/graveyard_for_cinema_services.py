# def link_seats (movie_seats_csv : str, booking_data_csv : str,template_seats_csv : str,
#                 book_movie_code_location : int = 2, book_x_seats_location : int = 5, book_y_seats_location : int = 6,) -> None:
#     booking_data_list : list = []
#     #First init the seats file (all the data of seats clear)
#     movie_seats_csv_whole_init(movie_seats_csv= movie_seats_csv,template_seats_csv= template_seats_csv)
#     #read the booking data
#     #read_movie_list_csv(movie_list_csv= booking_data_csv,movie_list=booking_data_list)
#     for row in booking_data_list:
#         #get the data of booking (movie code,x,y) from booking data list)
#         #[movie_code,x_axis,y_axis]
#         mvcode_x_y_list : list = get_movie_code_x_y_value_list(booking_data_array= row,
#                                                                movie_code_location= book_movie_code_location,
#                                                                x_seats_location= book_x_seats_location,
#                                                                y_seats_location= book_y_seats_location)
#         current_movie_seats : list = []
#         #read the current movie seats (from the mvcode_x_y_list)
#         read_movie_seats_csv(movie_seats_csv= movie_seats_csv,movie_seats= current_movie_seats,movie_code= mvcode_x_y_list[0])
#         # detect the actually seat is available or not
#         if movie_seats_specify_value(movie_seats=current_movie_seats,x_axis=mvcode_x_y_list[1],y_axis=mvcode_x_y_list[2]) ==  "-1":
#             #this usually happen in manager change the template code of movie seats
#             raise ValueError(f"This movie seat is unvailable(-1)!You should check your booking data file!\n"
#                              f"movie_seats: {current_movie_seats}\nx_axis: {mvcode_x_y_list[1]}\ny_axis: {mvcode_x_y_list[2]}")
#         # if no problem,modify the actual seat
#         modify_movie_seats_list(movie_seat_list=current_movie_seats,x_axis=mvcode_x_y_list[1],y_axis=mvcode_x_y_list[2],target_number= 1)
#         # update it to the movie seats csv
#         update_movie_seats_csv(movie_seats_csv= movie_seats_csv,movie_seats=current_movie_seats,movie_code= mvcode_x_y_list[0])

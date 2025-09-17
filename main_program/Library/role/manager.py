import os
import csv
from datetime import datetime

#13/9/2025: validate time format
def input_time(prompt="Enter time (HH:MM):"):
    while True:
        t = input(prompt)
        try:
            datetime.strptime(t,"%H:%M")
            return t
        except ValueError:
            print("Invalid format. Please enter like 18:00")

# Generate the next movie ID automatically
def generate_movieid(movie_list_csv:str) -> str:
    with open(movie_list_csv,"r") as f:
        lines = f.readlines()
        if len(lines) <=1:    #Only have header
            return "001"
        else:
            last_line = lines[-1].strip().split(",")
            last_id=int(f"{last_line[0]}")
            return f"{last_id+1:03d}"     #new id

# display all movie (users can easily check the movie code before making changes)
# add header if file is empty or missing
def List(movie_list_csv:str) -> None:
    header="movie_code,movie_name,cinema_number,movie_time_start,movie_time_end\n"
    try:
        with open(movie_list_csv,"r") as f:
            lines = f.readlines()
            if not lines:  # 文件为空
                with open(movie_list_csv,"w") as fw:
                    fw.write(header)
                print("No movies yet. Added header.")
                return
            else:
                for movie in lines:
                    print(movie)
                    print()
    except FileNotFoundError:
        with open(movie_list_csv, "w") as f:
            f.write(header)
        print("File not found. Created new file with header.")

# Read header and all movie records from the CSV file
def get_data(movie_list_csv : str) ->None :
    movies=[]
    with open(movie_list_csv,"r") as f:
        lines = f.readlines()
        header=lines[0].strip().split(",")
        for line in lines[1:]:
            movies.append(line.strip().split(","))
        return header,movies

# Add a new movie record into the CSV file           
def add(movie_list_csv : str) ->None:
    Add = False
    try:
        codes = generate_movieid(movie_list_csv)
        name = input("Enter the movie name: ")
        cinema = input("Enter the cinema number: ")
        start = input_time("Enter start time (HH:MM): ")
        end  = input_time("Enter end time (HH:MM): ")
        new = f"{codes},{name},{cinema},{start},{end}\n"
        with open(movie_list_csv,"a") as addmovie:
            addmovie.write(new)
        Add = True
    except ValueError:
        print("Invalid input.")
    if Add:
        print("Added successfully!")
    else:
        print("Failed.")

# Update an existing movie record by movie code
def update(movie_list_csv : str) ->None:
    header,movies = get_data(movie_list_csv)
    List()
    code = input("Enter the movie code: ")
    Update = False
    print("""What do u want to update: 
          1.Name
          2.Time
          3.Cinema number
          4.All""")
    try:
        choice2 = int(input("Enter your choice: "))
        for movie in movies:
            if movie[0] == code:
                if choice2 == 1:
                    new_name = input("Enter the new movie name: ")
                    movie[1]= new_name
                elif choice2 == 2:
                    new_start_time = input_time("Enter new start time (HH:MM):")
                    new_end_time =  input_time("Enter new end time (HH:MM):")
                    movie[3] = new_start_time
                    movie[4] = new_end_time
                elif choice2 == 3:
                    new_cinema = input("Enter the new cinema number: ")
                    movie[2] = new_cinema
                elif choice2 == 4:
                    new_name = input("Enter the new movie name: ")
                    new_cinema = input("Enter the new cinema number: ")
                    new_start_time = input_time("Enter new start time (HH:MM):")
                    new_end_time =  input_time("Enter new end time (HH:MM):")
                    movie[1]= new_name
                    movie[2] = new_cinema
                    movie[3]= new_start_time
                    movie[4] = new_end_time
                else:
                    print("Invalid choice.")
            Update = True
    except ValueError:
        print ("Invalid input")
        return
    if Update:
        with open(movie_list_csv,"w") as update:
            update.write(",".join(header)+"\n")
            for movie in movies:
                update.write(",".join(movie)+"\n") 
        print("Updated successfully!")
    else:
        print ("Failed.Code didn't exist.")

# Remove a movie record by movie code
def remove(movie_list_csv : str) ->None:
    header,movies = get_data(movie_list_csv)
    List()
    code = input("Enter the movie code: ")
    Remove = False
    new_movie = []
    for movie in movies:
        if movie[0] == code:
            Remove = True
            continue
        new_movie.append(movie)
    
    if Remove:
        with open(movie_list_csv,"w") as remove:
            remove.write(",".join(header)+"\n")
            for mov in new_movie:
                remove.write(",".join(mov)+"\n")
        print ("Removed successfully!")
    else:
        print ("Failed.Code didn't exist.")

# display the booking list
def list_booking(booking_list_csv:str)->None:
    try:
        with open(booking_list_csv,"r") as f:
            lines = f.readlines()
            if len(lines) <=1 :
                print("No booking found") 
            else:
                for line in lines:
                    print("Booking List:")
                    print(line.strip().split(","))
    except FileNotFoundError:
        print("File doesn't exist.")

# Main menu loop for movie management system
while True:
    print("""Manager Menu:
          1. Add Movie
          2. Update Movie
          3. Remove Movie
          4. List Booking
          5. Quit""")
    choice=int(input("Enter your choice:"))
    if choice == 1:
        add()
    elif choice == 2:
        update()
    elif choice == 3:
        remove()
    elif choice == 4:
        list_booking()
    elif choice == 5:
        break
    else:
        print("Invalid choice.")


        


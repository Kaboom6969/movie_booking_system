import csv
import os
from movie_booking_system.main_program.Library.movie_booking_framework.movie_list_framework import *


#这个是利用movie_booking框架的例子，（请将后续的函数都修改至适配此框架）
def view_upcoming_movies(file_name : str,movie_code_column_location : int = 1):
    movie_list : list = []
    read_movie_list_csv (movie_list_csv= file_name,movie_list= movie_list,code_location= 0)
    print("Upcoming Movie:")
    for row in movie_list:
        print(f"Movie Code: {row[movie_code_column_location]}")


def report_issue():
    movie_code = input("please enter movie code: ")
    issue_type = input("Update (aircond, speaker, projector) Status: ")
    status_input = input("Change equipment status? (0:good, 1:breakdown, 2:under maintainence): ")
    try:
        status = int(status_input)
        if status not in [0, 1, 2]:
            raise ValueError (f"Status: {status} should be 0 or 1 or 2")
    except ValueError as e:
        print(f"Invalid Input,{e}")
        return

    if issue_type == "aircond":
        update_equipment_status(movie_code, status, 0, 0)
    elif issue_type == "speaker":
        update_equipment_status(movie_code, 0, status, 0)
    elif issue_type == "projector":
        update_equipment_status(movie_code, 0, 0, status)
    else:
        print("invalid issue type")


def check_equipment_status(file_name):
    csv_path = get_path(file_name)
    try:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            print("Equipment Status:")
            for row in reader:
                status_map = {'0': 'good', '1': 'Breakdown', '2': 'Under Maintenance'}
                aircond = status_map.get(row['aircond_status'], 'unknown')
                speaker = status_map.get(row['speaker_status'], 'unknown')
                projector = status_map.get(row['projector_status'], 'unknown')
                print(
                    f"Tech: {row['tech_code']}, Movie: {row['movie_code']}, aircond: {aircond}, speaker: {speaker}, projector: {projector}")
    except FileNotFoundError:
        raise FileNotFoundError(f"File:{file_name} not found")


def update_equipment_status(movie_code, aircond_status, speaker_status, projector_status,file_name):
    csv_path = get_path(file_name)
    rows = []
    found = False
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            if row['movie_code'] == movie_code:
                row['aircond_status'] = str(aircond_status)
                row['speaker_status'] = str(speaker_status)
                row['projector_status'] = str(projector_status)
                found = True
            rows.append(row)
    if not found:
        print(f"can't find movie_code: {movie_code}")
        return
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print("Status updated successfully")


if __name__ == "__main__":
    # view_upcoming_movies("cinema_device_list.csv")
    # check_equipment_status("cinema_device_list.csv")
    # update_equipment_status('001', 0, 0, 0,"cinema_device_list.csv")
    report_issue()
# CHANGELOG

# Clerk
### Added
## [1.1.0] - 2025-09-12
- Initial booking system (basic version, still needs improvement).
## [1.1.0] - 2025-09-13
- added some booking system data.
## [1.1.0] - 2025-09-13
- added column `booking_id` 
## [1.1.0] - 2025-09-15
### Changed
- Refactored seat booking flow to use `movie_seats_pointer_valid_check` for coordinate validation
- Removed manual row/column boundary checks for cleaner logic
- Simplified seat validation process with `movie_seats_specify_value`
## [1.1.0] - 2025-09-15
### Added
- `get_user_choice()` function for robust menu input handling.
- `select_movie()` function to validate and select movies cleanly.
- `checking_movie()` function to display seat map and capacity.
### Changed
- Refactored `clerk()` by extracting sub-functions for better readability and maintainability.
- Updated `generate_booking_id()` logic:
  - Fixed issue where booking IDs could increment incorrectly by +N.
  - Now starts from `B001` when no bookings exist.
  - Handles empty rows and invalid IDs gracefully.
### Fixed
- Improved error handling for invalid seat input and out-of-range choices.
- Prevented crashes when parsing booking IDs with unexpected values.
### Added 
- - added column `Seat(x-axis,y-axis)` 
## [1.1.0] - 2025-09-15
### Added
- `delete_user_booking_data`
- New function to delete a booking row from booking_data.csv by booking_id.
- `get_user_booking_axis_and_booking_id`
- New function to return (column, row, booking_id) based on user input, removing the need for global variables.
### Change
- modify_booking_data
- Added cancel booking feature (choice == 1):
- Frees the seat (modify_movie_seats_list → 0).
- Updates seat CSV file.
- Deletes the corresponding booking record.
- Added quit option (choice == 3).
- Placeholder for modify booking feature (choice == 2).
- Explicitly converts column and row to integers before modifying seat data to prevent type errors. 
  - Add column `Source`
### Fixed
- Fixed a bug in modify_booking_data where column / row were strings, causing TypeError.
## [1.1.0] - 2025-09-16
### Added
- `check_booking_full`
- New function to check movie_seat is full or not
- `check_booking_data`
- New function to check booking_data.csv exist or hot
## [1.1.0] - 2025-09-17
### Changed
- Replaced manual seat update (`modify_movie_seats_list` + `update_movie_seats_csv`)
  with `link_seats` to ensure seat and booking data synchronization.
## [1.1.1] - 2025-09-17
### Added
- Implemented booking cancellation feature (users can cancel an existing booking).
- Implemented booking modification feature (users can change their booked seat).
## [1.1.1] - 2025-09-18
### Fixed
- Fixed a bug out of index in `select_seat`
## [1.1.1] - 2025-09-18
### Fixed
- Fixed a bug in `select_seat` where entering a column value could cause "out of index".
- Fixed a bug in `modify_input_data` where updating data would raise an error.

## [1.1.1] - 2025-09-18
### Added
- Implemented `generate_receipt` function, generates a receipt based on user input booking ID.

### Fixed
- Prevented invalid seat access by centralizing validation logic
- Reduced redundant error handling and unnecessary global variable usage
- Fixed a bug where the header was not displayed when using the modify and cancel functions.

## [1.2.0] - 2025-09-24
### Added
- refactor most function in `clerk.py` so all the function is now support cache based system


# Customer
## [1.0.0] - 2025-09-13
### Added
- added `check_ticket_bought` function (still in test)
## [1.0.1] - 2025-09-13
### Added
- added `booking_to_movie_print` function
### Changed
- now `check_ticket_bought` is ok to use
## [1.1.0] - 2025-09-14
### Added
- **Added `check_all_movie_list` function**: Customers can now view a list of all available movies.
- **Added `movie_list_to_movie_seats_print` function**: Allows customers to view the emoji seating map for a specific movie by entering its code.
- **Added "Show Seat Capacity" feature**: All movie listings now dynamically calculate and display the number of available seats (`Capacity`) for each movie.
- **Added `movie_list_print_with_format` helper function**: The logic for printing formatted movie lists has been extracted into a separate, reusable module.
- **Added `code_range_create` helper function**: A utility function to extract a specific column of data from a 2D list, improving code reusability.

### Changed
- **Refactored `booking_to_movie_print`**: The function has been renamed to `booking_to_movie_list_print`, and its core printing logic was moved to the new `movie_list_print_with_format` function for a cleaner code structure.
- **Updated `check_ticket_bought`**: The function can now handle the new `booking_data.csv` format which includes a `Booking ID`, by using the `code_location=1` parameter to correctly locate the `customer_code`.

### Special
- Just let you guys see how Spaghetti Code looks like (in `book_movie`) (in 1.1.0 a)

## [1.2.0] - 2025-09-15
### Added
-  Added `_booking_data_create` function (b version)
- add user_id show in `check_ticket_bought` (d version)
### Changed
- **Refactored the booking process**: The monolithic booking function has been broken down into three smaller, single-responsibility functions (`book_movie_operation`, `book_movie_input`, `book_movie_buy`). This greatly improves code readability, maintainability, and reusability.
- `book_movie_operation` now acts as a high-level coordinator for the booking flow.
- `book_movie_input` is now a reusable utility that handles robust user input and validation for coordinates.
- `book_movie_buy` now encapsulates all logic related to confirming and finalizing the purchase.
- now `book_movie_operation` will add the booking record to booking_data.csv (b version) (abandon)
- now `book_movie_buy` will not change the movie_seats by writing the csv file (link_seats can do all) (c version)
- change the var name in `book_movie_operation` (movie_seats -> booking_movie_seats) (c version)

## [1.2.1] - 2025-09-22
### Added
- now `cancel_booking_operation` is done!
- add `link_seats` for `book_movie_operation`
### Changed
- `check_ticket_bought` now will return book_id and not user_id

## [1.3.0] - 2025-09-24
### Added
- refactor most function in `customer.py` so all the function is now support cache based system
### Changed
- change the DEFAULT_WIDTH from 20 to 30


# Technician
## [1.0.0] - 2025-09-19
### Added
- just a base
- add a csv file for technician (a version)
### Changed
- add parameter for `update_equipment_status` and `view_upcoming_movies` (a version)
- Add a more detailed error directory for `report_issue` (b version)
- refractor `view_upcoming_movies`,let it use the `movie_list_framework`'s function (c version)
- change the name (technicians.csv -> cinema_device_list.csv (d version)
### Fixed
- fix the bug that `update_equipment_status` cannot find the file (a version)
- add a comment for `techinician.py` (c version)

## [1.1.0] - 2025-09-26
## Main
- refactor all the function so the function is more dynamic and support cache based system
### Added
- add a function `movie_list_print_technician_ver`
### Changed
- `report_issue` function is now cache based and more dynamic 
- `update_status` function is now cache based and more dynamic 
- `check_equipment_status` function is now cache based and more dynamic
- `view_upcoming_movies` is now cache based and can really get the upcoming movie (the date before today will not show)

# Manager
## [1.0.0] - 2025-09-19
### Added
- just a base

## [1.1.0] - 2025-09-27
### Added
- added `add_movie_operation` function (more dynamic) (will be split to small function i think?)
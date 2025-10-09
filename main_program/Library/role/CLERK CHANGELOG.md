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

## [1.2.1] - 2025-10-09
### Changed
- Replaced seat update mechanism from CSV write-based to in-memory dictionary update.
- Added new function update_seat_value_in_cache in central_cache_system_framework.py.
- Updated booking() logic to use update_seat_value_in_cache instead of update_movie_seats_csv.
- Seat status now updates instantly after booking without reloading or writing files.

### Added
Added optional real-time seat refresh display after successful booking.
`msf.print_seats(movie_seats_dict[input_movie_code])`
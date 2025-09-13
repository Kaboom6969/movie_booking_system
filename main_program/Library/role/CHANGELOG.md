# CHANGELOG

## Clerk
### Added
## [1.1.0] - 2025-09-12
- Initial booking system (basic version, still needs improvement).
## [1.1.0] - 2025-09-13
- added some booking system data.
## [1.1.0] - 2025-09-13
- added column `booking_id` 

## Customer
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

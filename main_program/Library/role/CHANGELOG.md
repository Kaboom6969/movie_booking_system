# CHANGELOG

## Clerk
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

### Fixed
- Prevented invalid seat access by centralizing validation logic
- Reduced redundant error handling and unnecessary global variable usage

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

### Special
- Just let you guys see how Spaghetti Code looks like (in `book_movie`) (in 1.1.0 a)

## [1.2.0] - 2025-09-15
### Changed
- **Refactored the booking process**: The monolithic booking function has been broken down into three smaller, single-responsibility functions (`book_movie_operation`, `book_movie_input`, `book_movie_buy`). This greatly improves code readability, maintainability, and reusability.
  - `book_movie_operation` now acts as a high-level coordinator for the booking flow.
  - `book_movie_input` is now a reusable utility that handles robust user input and validation for coordinates.
  - `book_movie_buy` now encapsulates all logic related to confirming and finalizing the purchase.

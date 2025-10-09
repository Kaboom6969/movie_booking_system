# CHANGELOG
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

## [1.3.1] -2025-10-07
### Added
- add a wrap function `customer` for this file
- add `pay_money` for `book_movie_system` (b version)
### Changed
- small refactor in `check_ticket_bought` function (change the index to dynamic) (a version)
- `cancel_booking_operation` now is using `fu.element_input` instead of print and input (a version)
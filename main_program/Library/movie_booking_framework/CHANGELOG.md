# ChangeLog

## [1.11] - 2025-09-01
### Changed
- Modified `read_movie_seats_list_csv`. Now, the CSV file to be read must be passed as a parameter to the function, and it no longer returns any value.
- `overwrite_file` is now a private function (`_overwrite_file`) and is prohibited from being referenced externally!
### Fixed
- `write_movie_seats_list_csv` can now directly write data to the CSV file without needing an additional call to `overwrite_file` (as it has been encapsulated within the function), reducing complexity.

## [1.12] - 2025-09-01
### Added
- Added `read_movie_list_csv` function to the movie_list_framework package for reading the movie_list CSV file.
### Changed
- Renamed `read_movie_seats_list_csv` to `read_movie_seats_csv` for clarity and to avoid confusion.
- Separated the movie_list_framework and movie_seats_framework into two distinct packages for better organization.

## [1.12.1] - 2025-09-01
### Added
- Add the ``CHANGELOG.md`` to review every commit

## [1.13.0] - 2025-09-02
### Added
- Added `add_movie_seats_csv`, which now allows you to directly append to the movie seat list. (`write_movie_seats_csv` overwrites the file).
- Added `header_create`, a private function for generating the header data (such as movie codes, START, and END) for the CSV file. This function is not intended for external use.
### Changed
- Renamed `write_movie_seats_list_csv` to `write_movie_seats_csv` for clarity and to avoid confusion.
- `write_movie_seats_csv` now includes error reporting for when the movie code does not exist.
### Fixed
- Fixed an issue where the number of columns would gradually decrease each time `write_movie_seats_csv` was used to overwrite the file.

## [1.13.1] - 2025-09-02
### Changed
- Added comments to __movie_seats_framework__.py for improved readability.
- Renamed `write_movie_seats_csv` to `update_movie_seats_csv` to better reflect its function.

## [1.14.0] - 2025-09-03
### Added
- Added the `delete_movie_seats_csv` function, which now allows you to delete the seat list for a specific movie code (with error checking).
- Added `generate_movie_seats`, allowing you to create a seat table of any size!
- Added `movie_seats_valid_check` as an internal function to validate seat list states ("0", "1", "-1") and structure.
### Changed
- Partially refactored `update_movie_seats_csv` to support updating the CSV file with seat tables of any size! (Previously, the function only supported updates with seat lists matching the size of the existing CSV seat table.)
- Integrated `movie_seats_valid_check` with `ValueError` propagation in `read_movie_seats_csv`, `update_movie_seats_csv`, `add_movie_seats_csv`, `fill_movie_seats_list`, and `modify_movie_seat` to enhance input validation and error reporting.
- Improved data integrity for movie seat operations by ensuring invalid seat states are caught before CSV file modifications.

## [1.15.0] -2025-09-03
### Added
- Added a `get_path` function to improve file handling; file locations are now determined by a global constant at the top of the file, so files aren't restricted to the local directory.
- Added a `find_project_root` function to locate the target directory.
### Changed
- Updated the file-finding method in the `delete_movie_seats_csv` function for greater flexibility. (Other functions are being updated progressively.)
- Moved the location of some packages.

## [1.15.1] -2025-09-04 to 2025-09-14
## Added
- Added a `_movie_seats_csv_valid_check` function to check the format integrity of CSV files.
- add the `add_movie_list_csv` fucntion!
- add the `delete_movie_list_csv` function
### Changed
- Improved the error handling for functions within `movie_seats_framework` to generate more detailed error reports.
- Updated all the file-finding method in the fucntion in `_movie_seats_framework_`.
- update the function of `read_movie_seats_csv`,now it doesn't need csv library
- Now the `read_movie_list_csv` got two mode,choose movie mode for detect repeated code,choose another mode for no detect
- Now all the function in `movie_list_framework` can choose the code location (default 0)
### Fixed
- Just fixed the bug that `update_movie_seats_csv` will warning path even you use the file name and not path
- fix the bug that `update_movie_seats_csv` will change all the seats even they are not been selected by movie_code
- now this framework will delete the temp file by itself(if it is not temp file, it will warn and don't delete

## [1.15.2] -2025-09-14
### Added
- Add `get_capacity` function to get capacity (a version)
- Added `x_range_calculate` function (h version)
- Added `y_range_calculate` function (h version)
- Added `find_longest_list` function (h version)
- Added `movie_seats_pointer_valid_check` function (j version)
- Added `movie_seats_specify_value` function (j version)
- Just add the 🎯 for ` print_movie_seat_as_emojis` (k version)
### Changed
- Remove csv library from `movie_list_framework.py` (e version)
- Now The `print_movie_seat_as_emojis` function can draw pointer! (first version)
- Now `read_movie_list_csv` function didn't need the csv library (b version)
- Now `update_movie_list_csv` function didn't need the csv library (c version)
- Now `add_movie_list_csv` function didn't need the csv library (d version)
- Refactor pointer logic in `print_movie_seat_as_emojis` to be independent,now you can draw x_pointer or y_pointer alone! (g version)

### Fixed
- Add valid check for `get_capacity` (f version)
- Add boundary checks and align jagged arrays (though theoretically shouldn't exist) (i version)

## [1.15.3] -2025-09-16
### Added
- Add `get_biggest_number_of_code` function,now you can find the biggest number of the code_list! (first version)
- Add `_get_biggest_number_of_list` function (first version)
- Add `_list_str_number_to_int_number` function (first version)
- Add `_detect_got_digit` function (first version)

### Changed
- Now `get_biggest_number_of_code` will not read the csv file (and csv file is not parameter anymore),it will receive the parameter list (a version)
- change `_movie_seats_csv_valid_check`'s re.fullmatch to re.match (a version)

## [1.16.0] - 2025-09-17
### Added
- **Added High-Level API `link_seats`**: This new top-level function automates the entire business logic of synchronizing booking records with the seat map. It first initializes all movie seats from templates and then updates them to a "booked" state (`1`) based on the data in `booking_data.csv`.
- **Added `movie_seats_csv_whole_init` and `movie_seats_init` functions**: These functions work together to initialize or reset all seat maps in `movie_seat.csv` according to their corresponding templates from `template_seats.csv`.
- **Added `get_movie_code_x_y_value_list` utility function**: A helper function to safely extract and parse `movie_code`, `x_axis`, and `y_axis` from a single booking data row.
- **Added `skip_valid_check` parameter**: Introduced an optional `skip_valid_check` boolean parameter to major functions (`read`, `update`, `add`, `delete`) to bypass CSV validation for improved performance in controlled scenarios.
### Changed
- **Cross-Framework Integration**: The framework now imports and utilizes `read_movie_list_csv` from `movie_list_framework` to handle booking data, demonstrating enhanced modular collaboration.
- **Improved Error Handling**: The `link_seats` function now includes validation to prevent booking on an unavailable seat (state `-1`), raising a `ValueError` for data integrity.

### Fixed
- **Fixed circular import `read_movie_list_csv` import from movie_seats_framework.py
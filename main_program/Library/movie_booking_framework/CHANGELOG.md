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
## [1.15.1] -2025-09-04
### Changed
- Updated all the file-finding method in the fucntion in `_movie_seats_framework_`.

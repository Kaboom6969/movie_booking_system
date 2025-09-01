# ChangeLog
## [1.11] - 2025-09-01
### Changed
- Modified read_movie_seats_list_csv(...). Now, the CSV file to be read must be passed as a parameter to the function, and it no longer returns any value.
- overwrite_file(...) is now a private function (_overwrite_file(...)) and is prohibited from being referenced externally!
### Fixed
- write_movie_seats_list_csv(...) can now directly write data to the CSV file without needing an additional call to overwrite_file(...) (as it has been encapsulated within the function), reducing complexity.
## [1.12] - 2025-09-01
### Added
- Added read_movie_list_csv(...) function to the movie_list_framework package for reading the movie_list CSV file.
### Changed
- Renamed read_movie_seats_list_csv(...) to read_movie_seats_csv(...) for clarity and to avoid confusion.
- Separated the movie_list_framework and movie_seats_framework into two distinct packages for better organization.
## [1.12.1] - 2025-09-01
### Added
- Add the CHANGELOG.md to review every commit
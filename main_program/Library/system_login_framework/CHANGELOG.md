# CHANGELOG
## [1.0.0] - 2025-09-01
### Added
- Add a system_login_framework folder
## [1.1.0] - 2025-09-02
- Add main file for login framework (need to fix).
## [1.1.0] - 2025-09-02
- Add main file for login framework (need to fix).

### Changed
- Modified `login()` to return user ID instead of just True/False.
### Fixed
- Resolved an issue where `FileNotFoundException` occurred when the system attempted to access user data files (e.g., customer.csv, clerk.csv, etc.) before they were created. The program now automatically generates missing files to prevent runtime errors.


## [1.1.1] - 2025-09-18
### Added
- Added `role_prefix` parameter to the `register` function, allowing customization of role ID prefixes.
### Changed
- Removed `csv.reader` and `csv.writer`; replaced with custom file reader and writer.
### Fixed
- Fixed `get_data_directory` returning an incorrect path.

## [1.1.1] - 2025-09-19
### Added
- Added get_column_count function to retrieve the number of columns from the header.
- Added has_balance_column parameter to the write_data function to allow writing balance data.
### Changed
- Updated file reading to start from the second row (skip header).
### Fixed
- Fixed check_data and check_user_name causing 'Index out of range' errors during data iteration.
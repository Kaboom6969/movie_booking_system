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
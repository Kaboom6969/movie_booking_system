# CHANGELOG

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

## [1.1.1] - 2025-10-06
### Added
- add `technician` function (wrap function)

## [2.0.0] - 2025-10-08
### Information
- This is the final version (if no exceptions)
- now all function of technician is done!
### Added
- add `update_issue_status_operation` function
- finish `confirm_equipment_status` funciton
- add `check_equipment_status_operation`(high level function to operate `check_equipment_status`)
### Changed
- change the name from `report_issue` to `report_issue_operation`
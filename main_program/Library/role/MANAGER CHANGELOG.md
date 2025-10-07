# CHANGELOG
# Manager
## [1.0.0] - 2025-09-19
### Added
- just a base

## [1.1.0] - 2025-09-27
### Added
- added `add_movie_operation` function (more dynamic) (will be split to small function i think?)

## [1.1.1] - 2025-09-27
### Added
- added `element_input` function
- refactor `add_movie_operation` function with using `element_input` function and not just while loop

## [1.2.0] - 2025-09-28
### Added
- add `delete_movie_operation` function (more dynamic)

## [1.2.1] - 2025-09-30
### Added
- added `modify_movie_operation` function
### Changed
- moved `element_input` to `framework_utils.py`
- now `sync_all` is replace `sync_file` function (more stronger) (a version)

## [1.2.2] - 2025-10-03
### Added
- using the universal `fu.get_operation_choice` instead of the repeat print and element input (b version)
### Changed
- add `manager` function (Encapsulation all the operation)
- add more limit when adding movie (a version)
- moved `get_code_range` fucntion to framework_utils.py (c version)
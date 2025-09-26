# ChangeLog

## [1.0.0] -2025-09-23
### Added
- add CRUD operation for this framework
- split the `data_dictionary_framework.py` to this framework
- add `TEMPLATE_SEATS_DICTIONARY` (a version)
### Changed
- now the function will raise error if cache update fail

## [1.0.1] -2025-09-24
### Added
- add more information for the dictionary (file name,header...)
- add a new cache(dictionary) `MOVIE_DEVICE_CODE_DICTIONARY` (a version)
- add `primary_foreign_key_dictionary_init` function (a version)
- add `seats_code_catcher_from_cache` function (a version)
### Fixed
- fix the bug that `dictionary_update_with_dict` wouldn't update the data permanently (b version)
- now the `read_list_from_cache` will return one dimension list if the movie code is specific (if movie code is all still return two dimension list) (c version)

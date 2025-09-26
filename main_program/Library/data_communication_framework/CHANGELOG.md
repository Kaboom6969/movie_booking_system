# Changelog
## [1.0.0] -2025-09-23
### Added
- add the CRUD for the movie seats and movie list
- just change the name from (`seat_dictionary_create`) to (`seat_dictionary_init`)
- now the sync function it will raise error, while any operation file (IO or memory) (the xxx_sync function is just transition strategy)

## [1.1.0] -2025-09-24
### Added
- add `read_seats_from_cache` function
- add `seats_cache_write_to_csv` function
- add `list_cache_write_to_csv` function
- ready to refactor the system
### Changed
- delete all the sync function (b version)

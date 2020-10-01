# Change Log

## Unreleased
### Improvements

- 2020-08-20 - Added get_segment() helper that detects the current page
    - Updated files(s): app/home/routes.py

- 2020-06-22 - Guard Flask links with quotes
    - Sample href="{{ url_for('base_blueprint.login') }}"
    - Impacted files: login.html, register.html, sidebar.html

- 2020-06-22 - Added HEROKU support. Impacted files:
    - runtime.txt - Bump the Python version to 3.6.10
    - README added new section for HEROKU deployment

## [1.0.1] 2020-05-30
### Improvements & Bug Fixes

- Patch #Bug - Return a 403 Error for unauthorized access
- Update Licensing information
- Add CHANGELOG.md to track all changes

## [1.0.0] 2020-02-07
### Initial Release

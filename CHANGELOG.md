# Change Log

## [1.0.17] 2025-04-01
### Changes

- Update RM (minor)

## [1.0.16] 2024-05-18
### Changes

- Updated DOCS (readme)
  - [Custom Development](https://appseed.us/custom-development/) Section
  - [CI/CD Assistance for AWS, DO](https://appseed.us/terms/#section-ci-cd)

## [1.0.15] 2024-03-06
### Changes

- Update [Custom Development](https://appseed.us/custom-development/) Section
  - New Pricing: `$3,999`

## [1.0.14] 2023-10-07
### Changes

- Update Dependencies
- Silent fallback to SQLite

## [1.0.13] 2023-06-22
### Changes

- Print UserID on `index`
  - Via export in controller
  - Via `current_user` in view

## [1.0.12] 2023-03-15
### Changes

- DOCS Update
  - [Volt Dashboard Flask](https://docs.appseed.us/products/flask-dashboards/volt/) - `official help` 
- Links Curation (minor)

## [1.0.11] 2022-12-31
### Changes

- Added page compression for PRODUCTION env
  - `DEBUG=False`

## [1.0.10] 2022-12-31
### Changes

- Deployment-ready for Render (CI/CD)
  - `render.yaml`
  - `build.sh`

## [1.0.9] 2022-12-31
### Changes

- `DB Management` Improvement
  - `Silent fallback` to **SQLite**

## [1.0.8] 2022-09-07
### Improvements

- Added OAuth via Github
- Improved Auth Pages

## [1.0.7] 2022-05-25
### Improvements

- Built with [Volt Dashboard Generator](https://appseed.us/generator/volt-dashboard/)
  - Timestamp: `2022-05-25 22:26`
- Codebase refactoring
- Added CDN Support
  - via `.env` **ASSETS_ROOT**  

## [1.0.6] 2022-01-16
### Improvements

- Bump Flask Codebase to [v2stable.0.1](https://github.com/app-generator/boilerplate-code-flask-dashboard/releases)
- Dependencies update (all packages) 
  - Flask==2.0.2 (latest stable version)
  - flask_wtf==1.0.0
  - jinja2==3.0.3
  - flask-restx==0.5.1
- Forms Update:
  - Replace `TextField` (deprecated) with `StringField`

## Unreleased
### Fixes

- 2021-11-08 - `v1.0.6-rc1`
  - ImportError: cannot import name 'TextField' from 'wtforms'
    - Problem caused by `WTForms-3.0.0`
    - Fix: use **WTForms==2.3.3**
    
## [1.0.5] 2021-09-16
### Improvements & Fixes

- Bump Flask Codebase to [v2.0.0](https://github.com/app-generator/boilerplate-code-flask-dashboard/releases)
  - Dependencies update (all packages)
    - Use Flask==2.0.1 (latest stable version)
  - Better Code formatting
  - Improved Files organization
  - Optimize imports
  - Docker Scripts Update 

## [1.0.4] 2021-08-27
### Improvements

- Bump UI - [Volt Dashboard v1.4.1](https://github.com/themesberg/volt-bootstrap-5-dashboard/releases) 
  
## Unreleased 2021-05-26
### Tooling

- Added scripts to recompile the SCSS files
    - `app/base/static/assets/` - gulpfile.js
    - `app/base/static/assets/` - package.json
- `Update README` - [Recompile SCSS](https://github.com/app-generator/flask-dashboard-volt#recompile-css) (new section)

## [1.0.3] 2021-05-16
### Dependencies Update

- Bump Codebase: [Flask Dashboard](https://github.com/app-generator/boilerplate-code-flask-dashboard) v1.0.6
- Freeze used versions in `requirements.txt`
    - jinja2 = 2.11.3

## [1.0.2] 2021-03-30
### Improvements

- Bump UI: [Jinja Volt](https://github.com/app-generator/jinja-volt-dashboard/releases) v1.0.1
- [Volt Dashboard](https://github.com/themesberg/volt-bootstrap-5-dashboard/releases) v1.3.2

## [1.0.1] 2021-03-18
### Improvements

- Bump Codebase: [Flask Dashboard](https://github.com/app-generator/boilerplate-code-flask-dashboard) v1.0.5
- Freeze used versions in `requirements.txt`
    - flask_sqlalchemy = 2.4.4
    - sqlalchemy = 1.3.23

## [1.0.0] 2021-01-17

- Bump UI: [Jinja Volt](https://github.com/app-generator/jinja-volt-dashboard/releases) v1.0.0
- [Volt Dashboard](https://github.com/themesberg/volt-bootstrap-5-dashboard/releases/tag) v1.2.0 
- Codebase: [Flask Dashboard](https://github.com/app-generator/boilerplate-code-flask-dashboard/releases) v1.0.3


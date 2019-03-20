# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [Unreleased]
- Unrleased changes will go here.

## [1.2.0] - 2019-03-20
- Preserve quotes when using the `apiscrub` executable. This way you can format your document exactly how downstream consumers need it, e.g. quoting the strings `on` and `off` so a broken YAML 1.2 parser downstream doesn't parse them as booleans.
- Updated ruamel.yaml library with several fixes.

## [1.1.0] - 2018-10-09
- Properly remove references to items that have been removed. This is useful if you link to e.g. parameters that are only available to some audiences.

## [1.0.1] - 2018-09-05
- Dependency fix.

## [1.0.0] - 2018-09-05
- Initial release.

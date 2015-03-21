# Changelog

## 0.0.2 - 2015-03-21

### Fixed

-   `query` and `queryi` were incorrect. To get the same result as `querys`,
    the user had to subtract 1 from the start position. See:
    https://github.com/slowkow/pytabix/issues/5

-   The test for this module was not deterministic. A random test was
    generated, and the off-by-one bug in issue 5 was not caught because of
    this. Now I have a deterministic test that catches issue 5.

### Changed

-   The first version was called '0.1'. This does not follow semantic
    versioning standards. Now I've moved to '0.0.2' (MAJOR.MINOR.PATCH).
    See: http://semver.org/

## 0.1 - 2014-11-07

### Changed

-   Initial release.


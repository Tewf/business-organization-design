# Changelog

The releases this repository pins, newest first, in the form of [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
A pin move is recorded here, not in decisions/.

## 2026-11-12

### Changed

- The check `organisation-description` reads descriptions with markdown-it-py 4.2.0, a dependency the CI installs.
  Rule 6 of the shape asks for a GFM table at the top level of its section instead of the plain form
  ([record 0005](decisions/0005-read-descriptions-with-a-parser.md)).

## 2026-11-11

### Added

- Pinned reader-ergonomics v1.24.2 (`65e4247`), at the repository's start: the standard's pin, link, changelog and
  decision-record checks, which this skeleton is written to pass.
- Pinned reader-ergonomics-review v0.1.1 (`39d3b25`), at the same start: the shapes of the review's files and their
  headings in checks/config.toml.

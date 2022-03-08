# Migration flows explorer

The files in this folder are used to generate the `migration-flows` explorer.

## Building the explorer

You need Python 3.9 with `poetry` installed, then run `make`. It will generate the top-level explorer config `migration-flows.explorer.tsv`, if it's out of date.

## Input files

### `views-per-country.csv`

This file defines the different views (`graphers`) that should be available _per country_. You can use the placeholders `${country}` and `${country_slug}` in there.

### `column-defs.tsv`

In here, we define metadata for the columns used, including source information, units and the like.
Again, this is then expanded for all countries, and you can use the placeholders `${country}` and `${country_slug}`.

The "special" columns `entity` and `year` are added by default.

### `migration-flows-explorer.template.tsv`

In this template file, the boilerplate gluing the whole explorer spreadsheet together is defined. That includes, among others:

- The explorer title and subtitle
- The default country selection
- Three special placeholders: `$graphers_tsv`, `$column_defs`.
  It's probably best not to touch them unless you know exactly what you're doing :)

# `data/` — local-only data (not tracked)

This directory is intentionally **empty in version control**. Everything in it except this
README is git-ignored (see the root `.gitignore`).

## Why

EEG recordings and reports may be patient data and/or come from sources that do not permit
redistribution. Such files must **never** be committed to this repository.

Place any local EEG data you use for development or testing under `data/`; it will be ignored
by git.

## Tests

Automated tests do **not** depend on anything in this folder. They use small, synthetic,
non-real fixtures under `tests/fixtures/`.

## Rule of thumb

If a file under `data/` describes a real patient or comes from a restricted source, it must
**never** be committed. When in doubt, keep it out.

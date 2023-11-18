# Use pipenv to manage virtual environment and dependencies

Date: `2023-11-17`

## Status

Accepted

## Context

Managing and tracking dependencies using a `requirements.txt` file quickly becomes tedious and prone to errors,
especially in case of larger projects depending on many packages.

Also, separation between creating and managing project's virtual environment and installing and managing dependencies
is unnecessary and inconvenient.

## Decision

We will be using [`pipenv`](https://pipenv.pypa.io/en/latest/) for virtual environment and dependencies management.

## Consequences

There will be no further need to use `pip` and `virtualenv` tools separately.

Dependencies management and tracking will become automatic. `pipenv` will ensure deterministic builds by using `Pipfile.lock`.

Development workflow will become simplified thanks to the above.

## Keywords

- python
- pipenv
- virtual environment
- package
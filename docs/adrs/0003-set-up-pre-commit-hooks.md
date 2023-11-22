# Set up pre-commit hooks

Date: `2023-11-18`

## Status

Accepted

## Context

It is inconvenient to run ruff and black on the repository manually before each commit. There is a risk of forgetting
to do so, which may result in a commit containing improperly formatted changes.

It gets even riskier when we think about packages used for testing or type checking - it would be best to have a way
of automatic verification before each commit and push since it is much easier to fix mistakes before committing or worse,
pushing changes to the remote repository.

## Decision

We will be using [`pre-commit`](https://pre-commit.com) python package and a `.pre-commit-config.yaml`
configuration file.

## Consequences

Linting and formatting of our codebase, as well as launching tests, will be done automatically
with each commit and push.

## Keywords

- git
- pre-commit
- hook

# Use ruff & black to enforce Python codestyle

Date: `2023-11-14`

## Status

Accepted

## Context

In order to fulfill the `consistent code style` paragraph from `AMINI Coding Standards` we need to agree on a single code style.

The most convenient way is to define a set of tools that do the work **automatically**.

## Decision

We will use [ruff](https://github.com/charliermarsh/ruff) and [black](https://github.com/psf/black) to keep our codebase unified.

We will use the following config:
```toml
[tool.black]
line-length = 120
skip-string-normalization = 1

[tool.ruff]
line-length = 120
select = ["F", "E", "W", "I001"] # pyflakes, pycodestyle, isort
```


## Consequences


The code will be unified, which makes it easier for other developers to read/ work with.

In the long term, it might speed up development, onboarding, and offboarding processes.

## Keywords

- python
- ruff
- black
- formatter
- static analysis
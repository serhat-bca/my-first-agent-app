# Instructions for agents working in this repository

This repository starts empty on purpose. The person you work with decides what gets built. Your job is to build it inside the structure that is already here.

## Commands

| To | Run | Without make |
|---|---|---|
| Check that everything compiles and passes | `make check` | `python -m compileall -q src tests` then `python -m unittest discover -s tests -t .` |
| Run the tests | `make test` | `python -m unittest discover -s tests -t .` |
| Run the application | `make run` | `python -m src` |
| Turn on the commit checks | `make install-hooks` | `git config core.hooksPath .githooks` |

On Windows `make` is often missing, and `python` may be `py`. Use the third column.

The default language is Python 3 with the standard library only, so nothing needs installing. If the person asks for another language or a dependency, update the Makefile, `.githooks/pre-commit`, `.github/workflows/checks.yml` and this table in the same pull request.

## How work flows here

1. We work as a dual-agent team: the Primary Builder pairs with the person on features in `src/`, while the dedicated Test Engineer (`.agents/skills/test-engineer/`) focuses on `tests/`, `tests/scenarios/`, and verification.
2. Before writing code, read `tests/scenarios/`. If no scenario covers the request, write one with the person first (skill: `.agents/skills/write-scenarios/`).
3. Create a branch for every change. Never commit to `main`.
4. Build in `src/`. Read `src/AGENTS.md` and `conventions.md` first.
5. Write tests in `tests/` that prove each scenario.
6. Run `make check`. Fix what fails.
7. Open a pull request (skill: `.agents/skills/open-pull-request/`). Do not merge it yourself.

## Rules

- Do not edit a file in `tests/scenarios/` to make a test pass. A scenario changes only when the person changes what they want.
- Do not weaken, skip or delete a test to get a green check. Say what failed.
- Shared types live in `src/types/`. Look there before defining a new one.
- Report what you verified and what you did not.

## Where things are

- `conventions.md`: naming, structure, commit messages
- `src/AGENTS.md`: rules for application code
- `tests/scenarios/README.md`: the scenario format
- `.agents/skills/`: procedures

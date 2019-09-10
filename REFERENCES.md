# Reference Materials

## Documentation

### RISC

- [General Documentation](https://portal.riscnetworks.com/app/documentation/)
- [RESTful API Access](https://portal.riscnetworks.com/app/documentation/?path=/using-the-platform/restful-api-access/)
- [Swagger API Documentation](https://api.riscnetworks.com/docs.html)

## API References

### Errors

Some errors are not specifically written in every method since they may always return. Those are:

- 401 (Unauthorized) - Failed authentication.
- 500 (Internal Server Error) - Occurs anytime the RISC REST API receives malformed data or body.

## Package Related

### General Guidance

- [Python 3 - Type hints](https://docs.python.org/3/library/typing.html)
- [MyPy - Python 3 Cheat Sheet](https://mypy.readthedocs.io/en/latest/cheat_sheet_py3.html)

### Packages & Dependencies

#### Package Dependencies

- [Requests - Python HTTP module](https://github.com/kennethreitz/requests)
- [Python Fire - CLI module](https://github.com/google/python-fire)

#### Build/Dev/Testing Dependencies

- [black - Python linter]()
- [isort - Python import automatic sorting]()
- [pydocstyle - Python docstring/pep-257 linting]()
- [pycodestyle - Python code complexity / McCabe validation]()
- [yapf - Python linter / automatic styling]()
- [pylint - Python linter]()
- [flake8 - Python linter]()
- [bandit]()
- [autopep8 - Python automatic styling/linting]()
- [pytest - Python test module]()
- [pytest-sugar - PyTest plugin]()
- [pytest-isort - PyTest isort plugin]()
- [coverage - Python Coverage module]()
- [codecov - CodeCov.io coverage service]()
- [pytest-cov - PyTest coverage plugin]()
- [mock - Python test mocking module]()
- [responses - Python request response testing module]()
- [twine - Python package bundling]()
- [mypy - Python type validation]()

# Page loader

### Hexlet tests and linter status:
[![Actions Status](https://github.com/irisraine/python-project-51/workflows/hexlet-check/badge.svg)](https://github.com/irisraine/python-project-51/actions)
[![Actions Status](https://github.com/irisraine/python-project-51/workflows/pytest/badge.svg)](https://github.com/irisraine/python-project-51/actions/workflows/pytest.yml)
[![Actions Status](https://github.com/irisraine/python-project-51/workflows/flake8/badge.svg)](https://github.com/irisraine/python-project-51/actions/workflows/flake8.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/29b9cc7df151bf8cd176/maintainability)](https://codeclimate.com/github/irisraine/python-project-51/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/29b9cc7df151bf8cd176/test_coverage)](https://codeclimate.com/github/irisraine/python-project-51/test_coverage)

### Description

Educational project. The command line utility that provides the ability to save web pages on a local computer 
for later offline viewing. All of its local resources are saved with the page.

### Installation

1. Clone git repository to your local machine: `git clone git@github.com:irisraine/python-project-51.git`
2. Go to the utility directory: `cd python-project-51`
3. You must have Poetry to build the project. Use `make build` command for creating the package.
4. For installation use `python3 -m pip install --user dist/*.whl` command, or `make package-install`

### Run

Use command `page-loader -o [output] url` to download the desired web page to the specified location. 
By default, without specifying a save directory, the page will be saved to the current working directory.
Use optional key `-g` or `--globals` for saving all of page's resources, not only local ones.
Use `-l` or `--log` to enable logging.

If you need a help, use command `page-loader -h`

### Demonstration

*Downloading a web-page into a current working directory using default settings:*
[![asciicast](https://asciinema.org/a/539866.svg)](https://asciinema.org/a/539866)


*Downloading a web-page into a specified location:*
[![asciicast](https://asciinema.org/a/540086.svg)](https://asciinema.org/a/540086)


*Getting an errors:*
[![asciicast](https://asciinema.org/a/540092.svg)](https://asciinema.org/a/540092)
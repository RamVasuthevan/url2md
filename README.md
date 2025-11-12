# url2md

[![PyPI](https://img.shields.io/pypi/v/url2md.svg)](https://pypi.org/project/url2md/)
[![Changelog](https://img.shields.io/github/v/release/RamVasuthevan/url2md?include_prereleases&label=changelog)](https://github.com/RamVasuthevan/url2md/releases)
[![Tests](https://github.com/RamVasuthevan/url2md/actions/workflows/test.yml/badge.svg)](https://github.com/RamVasuthevan/url2md/actions/workflows/test.yml)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/RamVasuthevan/url2md/blob/master/LICENSE)

Get the markdown representation of the contents of a url

## Installation

Install this tool using `pip`:
```bash
pip install url2md
```
## Usage

For help, run:
```bash
url2md --help
```
You can also use:
```bash
python -m url2md --help
```
## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:
```bash
cd url2md
python -m venv venv
source venv/bin/activate
```
Now install the dependencies and test dependencies:
```bash
pip install -e '.[test]'
```
To run the tests:
```bash
python -m pytest
```

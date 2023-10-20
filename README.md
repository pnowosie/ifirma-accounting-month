# iFirma accounting month

This little tool helps me set the accounting month at the beginning of the calendar month to assert other systems work without disruptions.

## Version history

- 0.1.0 - First release

We'll follow best versioning scheme [ZeroVer](https://0ver.org) as this kind of stuff is never finished until it's not needed any more.

## Installation

**Requires**
- python >= 3.10

```bash
git clone --depth 1 --branch v0.1.0 \
    https://github.com/pnowosie/ifirma-accounting-month.git
cd ifirma-accounting-month
make install

```

:warning: To specify other than default python binary run
`make install PYBIN=<path to python binary>`


## Usage

```
> make
 
Usage:
  make <target>

iFirma API calls
  check            check current accounting month
  previous         move to previous accounting month than is actually set
  next             move to next accounting month than is actually set
  adjust           set accounting month to current calendar month (if it's not already set)

How-To
  help             display this helpful message
  clean            cleaning secrets & python virtual environment
  install          creates & install dependencies, prepares enviroment variables
```

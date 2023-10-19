# iFirma accounting month

This little tool helps me set the accounting month at the beginning of the calendar month to assert other systems work without disruptions.

## Installation

```bash
git clone https://github.com/pnowosie/ifirma-accounting-month.git
cd ifirma-accounting-month
make install
```

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

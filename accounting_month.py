"""
(CC) Edopi Corp. To Python 🐍 with ❤️
Part of a progressive migration away from Bash automation.


Example of changing accounting month in ifirma.pl service from
https://github.com/pnowosie/ifirma-api/blob/main/sample_invoice/check_accounting_month.py
with some modifications to be called from cron-job.

# IMPORTANT: This example requires that "abonent" API key is generated.
# See ifirma's "Podstawowe klucze autoryzacji" in the "Settings / API" section
Set env variable of name `IFIRMA_abonent_API_KEY` with the value
of the appropriate key.

USAGE: Follow the instructions in the Makefile.
Run `make` to check out your options.

"""
import datetime, json, os, re, requests, sys
import logging

from enum import Enum
from typing import Any
from ifirma.request import Request, API_URL

INFO_RE = re.compile(r"Zmieniono miesiąc księgowy na (\d+)-(\d{4}).")

# Possible actions. of `call_ifirma` function
Action = Enum('Action', ['GET', 'PREV', 'NEXT'])


def call_ifirma(what: Action) -> dict[str, int | Any]:
    """Gets or sets accounting month in ifirma service."""
    req = Request(api_key_name="abonent", api_key=os.environ.get("IFIRMA_abonent_API_KEY"))
    req.url = f"{API_URL}/abonent/miesiacksiegowy.json"

    if what != Action.GET:
        direction = "NAST" if what == Action.NEXT else "POPRZ"

        # Here the PUT request method is used.
        # Because `req.execute` only supports GET / POST requests
        # for PUT one shall directly use of `requests` library
        req.data = json.dumps(
            dict(MiesiacKsiegowy=direction, PrzeniesDaneZPoprzedniegoRoku=False)
        )
        headers = {**req.headers, "Authentication": req.auth_header}
        resp = requests.put(req.url, data=req.data, headers=headers)
    else:
        # Checking the current accounting month
        req.data = None
        resp = req.execute(requests)

    resp.raise_for_status()

    return parse_response(what, resp.json())


def parse_response(what: Action, json_resp: dict[str, int | Any]) -> dict[str, int | Any]:
    """
    Internal use. Parses response from ifirma service, see return of `call_ifirma` function.

    Example responses:
     - `{'response': {'RokKsiegowy': 2023, 'MiesiacKsiegowy': 10}}`
     - `{'response': {'Kod': 0, 'Informacja': 'Zmieniono miesiąc księgowy na 9-2023.'}}`
     - `{'response': {'Kod': 202, 'Informacja': 'Brak dostępu do następnego miesiąca księgowego.'}}`
    """

    resp = json_resp.get("response")
    if not resp:
        logging.error(f"Unsupported response: {json_resp}")
        raise ValueError("Invalid response")
    retcode = resp.get("Kod", 0)
    success = retcode == 0
    action = what
    if info := INFO_RE.match(resp.get("Informacja", "")):
        month, year = map(int, info.groups())
    else:
        month = resp.get("MiesiacKsiegowy", 0)
        year = resp.get("RokKsiegowy", 0)

    ret = dict(success=success, action=str(action), month=month, year=year, retcode=retcode)
    if info := resp.get("Informacja"):
        ret["info"] = info

    return ret


def parse_args() -> Action:
    """Parses command-line arguments passed to script."""
    match sys.argv[1] if len(sys.argv) > 1 else None:
        case "next" | "+1":
            direction = Action.NEXT
        case "prev" | "-1":
            direction = Action.PREV
        case "auto":
            # This will push month forward only of there is a need to do so
            now = datetime.datetime.now()
            actual = call_ifirma(Action.GET)
            if not actual["success"]:
                return Action.GET

            if actual["month"] == now.month and actual["year"] == now.year:
                logging.info(f"Current accounting month is correct {now.month}/{now.year}")
                direction = Action.GET
            else:
                logging.info(f"Auto-correcting actual accounting month from {actual['month']}/{actual['year']} to {now.month}/{now.year}")
                direction = Action.NEXT
        case _:
            direction = Action.GET

    return direction


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s]:\t%(message)s'
    )
    logging.info(call_ifirma(parse_args()))

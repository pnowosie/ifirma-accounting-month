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
Run `make` to check out you options.

"""
import datetime, json, os, re, requests, sys

from ifirma.request import Request, API_URL

INFO_RE = re.compile(r"Zmieniono miesiąc księgowy na (\d+)-(\d{4}).")

# Actions
GET = "GET"
PREV = "PREV"
NEXT = "NEXT"


def call_ifirma(what):
    req = Request(api_key_name="abonent", api_key=os.environ.get("IFIRMA_abonent_API_KEY"))
    req.url = f"{API_URL}/abonent/miesiacksiegowy.json"

    if what != GET:
        direction = "NAST" if what == NEXT else "POPRZ"

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


def parse_response(what, json_resp):
    """
    Example responses:
     - `{'response': {'RokKsiegowy': 2023, 'MiesiacKsiegowy': 10}}`
     - `{'response': {'Kod': 0, 'Informacja': 'Zmieniono miesiąc księgowy na 9-2023.'}}`
     - `{'response': {'Kod': 202, 'Informacja': 'Brak dostępu do następnego miesiąca księgowego.'}}`
    """

    resp = json_resp.get("response")
    if not resp:
        raise ValueError("Invalid response")
    retcode = resp.get("Kod", 0)
    success = retcode == 0
    action = what
    if info := INFO_RE.match(resp.get("Informacja", "")):
        month, year = map(int, info.groups())
    else:
        month = resp.get("MiesiacKsiegowy", 0)
        year = resp.get("RokKsiegowy", 0)

    ret = dict(success=success, action=action, month=month, year=year, retcode=retcode)
    if info := resp.get("Informacja"):
        ret["info"] = info

    return ret


def parse_args():
    match sys.argv[1] if len(sys.argv) > 1 else None:
        case "next" | "+1":
            direction = NEXT
        case "prev" | "-1":
            direction = PREV
        case "auto":
            # This will push month forward only of there is a need to do so
            now = datetime.datetime.now()
            actual = call_ifirma(GET)
            if not actual["success"]:
                raise ValueError("Failed to get current accounting month")

            if actual["month"] == now.month and actual["year"] == now.year:
                print(f"Current accounting month is correct {now.month}/{now.year}")
                direction = GET
            else:
                print(f"Auto-correcting actual accounting month from {actual['month']}/{actual['year']} to {now.month}/{now.year}")
                direction = NEXT
        case _:
            direction = GET

    return direction


if __name__ == "__main__":
    print(call_ifirma(parse_args()))

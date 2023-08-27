import urllib.request
import csv
from io import StringIO
import requests
import json
from pathlib import Path

SHEET = """https://docs.google.com/spreadsheets/d/e/2PACX-1vQQZRY5diISRR3rPmsoA6mg1SNmTXnFZJa3B4zDwxaAFtPjTvZifLKBc_lp4WnZaQ-h2A9UpOcadaiL/pub?gid=1870089332&single=true&output=csv"""

FILEPATH = Path("cache") / "sheet.csv"

def get_site(link):
    return urllib.request.urlopen(link).read().decode("utf8")

def nodeinfo(ott):
    print(f"Caching node #{ott}")
    return requests.post(
            "https://api.opentreeoflife.org/v3/tree_of_life/node_info",
            json = {
                "ott_id": ott,
                "include_lineage": True,
            },
        ).json()
#
# for common_name, count, link, scientific_name, ott in csv.reader(StringIO(get_site(SHEET))):
#     if not ott:
#         continue
#
#     with open(f"cache/opentree/{common_name}.json", "w") as f:
#         node = nodeinfo(ott)
#         json.dump(node, f, indent=4)

def get_sheet():
    if FILEPATH.exists():
        with open(FILEPATH) as f:
            return list(csv.reader(f))
    with open(FILEPATH, "w") as f:
        print(f"Caching sheet")
        data = get_site(SHEET)
        f.write(data)
        return list(csv.reader(StringIO(data)))

def check_sheet():
    for common_name, count, link, scientific_name, ott in get_sheet():
        if not ott:
            continue
        path = Path("cache") / "opentree" / f"{ott}.json"
        if not path.exists():
            with open(path, "w") as f:
                json.dump(nodeinfo(ott), f, indent=4)

import os
import requests
from base64 import b64encode
from bs4 import BeautifulSoup as BS

ROOT_IP = "http://" + os.environ.get("ROOT_IP", "192.168.1.1")


def _gen_base64header(user, password):
    bs64_uspd = b64encode(str.encode("{u}:{pd}".format(u=user, pd=password))).decode("ascii")
    return {"Authorization": "Basic %s" % bs64_uspd}

session = requests.session()

users = ["cht", "admin", "user"]
passwords = ["admin", "user",
             "chtnvdsl", "chtcvdsl", "chtsvdsl",
             "chtnadsl", "chtcadsl", "chtsadsl",
             "chtap"]
header_list = [_gen_base64header(u, p) for u in users for p in passwords]

for header in header_list:
    res = session.get(ROOT_IP, headers=header)
    soup = BS(res.text, "lxml")
    if soup.select("h4")[0].text[:3] != "401":
        print(header)
        print("Found it.")
        break
    print(soup.select("h4")[0].text[:3])
print("Not found.")

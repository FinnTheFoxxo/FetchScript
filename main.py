import os
import argparse
import requests
from bs4 import BeautifulSoup as BS
from urllib.parse import urlparse

parser = argparse.ArgumentParser()
parser.add_argument("domain", type=str, help="Please include the http URL scheme!")
args = parser.parse_args()
print(f"Initializing on {args.domain}")
directory = os.getcwd()
x = urlparse(args.domain); fix = x.hostname #bit of a hack
if not os.path.exists(f"{directory}/domains/{fix}"):
    os.system(f"mkdir {directory}/domains/{fix}")
elif not os.path.exists(f"{directory}/domains/{fix}/scripts"):
    os.system(f"mkdir {directory}/domains/{fix}/scripts")
url_dump = open(f"domains/{fix}/urls.txt", "w+")
script_dump = open(f"domains/{fix}/scripts.txt", "w+")

def main():
    url = [""]; script = [""]
    core = requests.get(args.domain)
    response = BS(core.text, "html.parser")
    for src in response.find_all("script"):
        fetch = src.get("src")
        if fetch == None:
            script.append(src)
        elif not "https://" in fetch:
            url.append(f"https://{fix}/{fetch}")
        else:
            url.append(fetch)
    if len(script) != 0:
        print(script)
        for line in script:
            print(f"\033[1;33m{line}\033[0m")
            script_dump.write(f"{str(line)}\n")
    if len(url) != 0:
        print(url)
        for line in url:
            print(f"\033[0;32m{line}\033[0m")
            url_dump.write(f"{str(line)}\n")
        for line in url:
            os.system(f"wget -P \"domains/{fix}/scripts\" -U \"Mozilla/5.0 (Windows NT 10.0; WOW64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.5666.197 Safari/537.36\" {line}")

main()


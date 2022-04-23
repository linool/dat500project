from urllib.parse import urlparse
import urllib.request
from os import path
import json
import subprocess

locations = set()
with open("index_no_domain") as file:
    for line in file:
        line = line.strip()
        tmp = line.find('{"url":')
        if tmp != -1:
            dict = json.loads(line[line.find('{"url":'):])
            locations.add(dict["filename"])
with open("filenames_no_domain", "w+") as w:
    w.write('\n'.join(locations))

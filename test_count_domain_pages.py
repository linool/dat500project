import json
from urllib.parse import urlparse

with open("index_no_domain") as file:
    for line in file:
        line = line.strip()
        if line:
            if line.find('{"url":') == -1:
                print(line)
            else:
                page_dict = json.loads(line[line.find('{"url":'):])
                link = urlparse(page_dict["url"])
                domain = link.hostname
                #if domain:
                    #if page_dict["status"] == "200":
                        #print(domain)

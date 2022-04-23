import subprocess
import urllib.request
from urllib.parse import urlparse
from os import path


with open("filenames_uis_no.txt") as file:
    for line in file:
        line = line.strip()
        line = line.replace(".warc.", ".warc.wet.")
        tmp = line.split('/')
        if  tmp[4] == 'crawldiagnostics' or tmp[4] == 'robotstxt':
            continue
        else:
            line = line.replace("/warc/", "/wet/")    
            print(line)
            file_name = tmp[-1]
            if not path.exists(file_name):
                url = 'https://commoncrawl.s3.amazonaws.com/' + line
                try:
                    urllib.request.urlretrieve(url, file_name)
                except: 
                    print("Couldn't download file "+url)

